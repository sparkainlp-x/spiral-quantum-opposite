"""Tests for spiral-quantum-opposite (standard library only).

Run:  python3 -m unittest discover -s tests -v
"""

import math
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import spiral_quantum_opposite.core as O

R = 1.0
TWO_PI = 2.0 * math.pi
LAM = 0.5
M, N = 2, 3
K = TWO_PI * N / R


def _norm_pair(m, k, lam=LAM, n_r=32, n_theta=128):
    radii, _, a = O.field_on_grid(m, k, lam, R, n_r, n_theta)
    _, _, b = O.field_on_grid(-m, -k, lam, R, n_r, n_theta)
    return radii, O.normalize(a, radii, R, n_theta), O.normalize(b, radii, R, n_theta)


class TestOppositeDefinition(unittest.TestCase):
    def test_opposite_is_conjugate(self):
        for r in (0.25, 0.5, 0.75):
            for t in (0.3, 1.1, 2.9):
                fwd = O.field(r, t, M, K, LAM)
                opp = O.field(r, t, -M, -K, LAM)
                self.assertLess(abs(opp - fwd.conjugate()), 1e-15)

    def test_opposite_of_opposite_is_original(self):
        self.assertEqual(O.opposite(*O.opposite(M, K)), (M, K))

    def test_density_identical(self):
        radii, a, b = _norm_pair(M, K)
        da, db = O.density(a), O.density(b)
        worst = max(abs(da[i][j] - db[i][j])
                    for i in range(len(radii)) for j in range(len(da[0])))
        self.assertLess(worst, 1e-15)

    def test_normalization(self):
        radii, a, _ = _norm_pair(M, K)
        total = sum(abs(a[i][j]) ** 2 * radii[i] * (R / len(radii)) * (TWO_PI / len(a[0]))
                    for i in range(len(radii)) for j in range(len(a[0])))
        self.assertAlmostEqual(total, 1.0, places=9)


class TestOrthogonalityAndWinding(unittest.TestCase):
    def test_orthogonal_for_nonzero_m(self):
        for m in (1, 2, 3):
            k = TWO_PI * N / R
            radii, a, b = _norm_pair(m, k)
            inner = O.inner_product(a, b, radii, R, len(a[0]))
            self.assertLess(abs(inner), 1e-12)

    def test_self_opposite_m_zero(self):
        radii, a, b = _norm_pair(0, K)
        inner = O.inner_product(a, b, radii, R, len(a[0]))
        # m = 0 opposite is the radial conjugate; the pair is NOT
        # orthogonal (it is the same winding), and its overlap is the
        # radial integral of exp(-2ikr), which is small but nonzero.
        # What must hold exactly: winding 0 on both sides.
        self.assertEqual(O.ring_winding(0, K, LAM, R), 0)
        self.assertEqual(O.ring_winding(0, -K, LAM, R), 0)
        self.assertLess(abs(inner), 1.0)

    def test_winding_flips_sign(self):
        for m in (1, 2, 3):
            k = TWO_PI * N / R
            self.assertEqual(O.ring_winding(m, k, LAM, R), m)
            self.assertEqual(O.ring_winding(-m, -k, LAM, R), -m)

    def test_interference_differs_from_density_sum(self):
        radii, a, b = _norm_pair(M, K)
        da, db = O.density(a), O.density(b)
        worst = 0.0
        for i in range(len(radii)):
            for j in range(len(a[0])):
                s = a[i][j] + b[i][j]
                worst = max(worst, abs(abs(s) ** 2 - (da[i][j] + db[i][j])))
        self.assertGreater(worst, 0.5)


class TestStandingWaves(unittest.TestCase):
    def test_azimuthal_nodes(self):
        self.assertEqual(O.azimuthal_node_count(1, K, LAM, R), 2)
        self.assertEqual(O.azimuthal_node_count(2, K, LAM, R), 4)
        self.assertEqual(O.azimuthal_node_count(3, K, LAM, R), 6)

    def test_azimuthal_nodes_m_zero_is_radial_not_azimuthal(self):
        self.assertEqual(O.azimuthal_node_count(0, K, LAM, R), 0)

    def test_radial_nodes_m_zero(self):
        self.assertEqual(O.radial_node_count(K, LAM, R), 2 * N)


class TestGate(unittest.TestCase):
    def test_gate_symmetric_under_opposite(self):
        for m in (-2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2):
            for n in (-3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3):
                k = TWO_PI * n / R
                self.assertEqual(O.closes(m, k, R), O.closes(-m, -k, R))

    def test_gate_agrees_with_original_for_positive_k(self):
        for m in (-2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2):
            for n in (-3, -2, -1, 0, 1, 2, 3):
                k = TWO_PI * n / R
                if k > 0:
                    self.assertEqual(O.closes(m, k, R), O.closes_original(m, k, R))
                else:
                    # The original gate refuses every k <= 0 candidate;
                    # the opposite gate admits the closing ones.
                    self.assertFalse(O.closes_original(m, k, R))

    def test_gate_refuses(self):
        self.assertFalse(O.closes(M, 0.0, R))
        self.assertFalse(O.closes(1.5, K, R))
        self.assertFalse(O.closes(M, TWO_PI * 2.5 / R, R))
        self.assertFalse(O.closes(-1.5, -K, R))
        self.assertFalse(O.closes(M, -TWO_PI * 2.5 / R, R))

    def test_mode_numbers_and_rings(self):
        self.assertEqual(O.mode_numbers(M, K, R), (M, N))
        self.assertEqual(O.mode_numbers(-M, -K, R), (-M, N))
        self.assertIsNone(O.mode_numbers(1.5, K, R))
        rings = O.quantized_radii(K, R)
        opp_rings = O.quantized_radii(-K, R)
        self.assertEqual(len(rings), N)
        for got, want in zip(rings, [1.0 / 3.0, 2.0 / 3.0, 1.0]):
            self.assertAlmostEqual(got, want, places=12)
        self.assertEqual(rings, opp_rings)

    def test_random_candidates_refused(self):
        total = 0
        for seed in (0, 1, 42):
            admitted, _ = O.count_closing(O.random_candidates(500, seed), R)
            total += len(admitted)
        self.assertEqual(total, 0)


if __name__ == "__main__":
    unittest.main()
