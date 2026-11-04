"""Demo: the spiral quantum opposite (standard library only).

Prints the measured results:
  1. Density blindness + orthogonality (the opposite hides in density,
     shows in phase).
  2. Winding and angular momentum: +m vs -m.
  3. Standing waves: azimuthal nodes 2|m|, radial nodes 2n for m = 0.
  4. Gate symmetry: pairs admitted together, negative controls refused.
  5. Rings shared by a mode and its opposite.

Run:  python3 demo.py
Tests: python3 -m unittest discover -s tests -v
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import spiral_quantum_opposite.core as O

R = 1.0
TWO_PI = 2.0 * math.pi
LAM = 0.5
M, N = 2, 3
K = TWO_PI * N / R


def main():
    print("Spiral quantum opposite (SYNTHETIC toy, companion to")
    print("spiral-envelope-atoms)")
    print("Disk radius R = 1, field psi = exp(-r/lam) * exp(i*(m*theta + k*r))")
    print(f"Canonical case: lam = {LAM}, m = {M}, n = {N} (k = 6*pi)")
    print()

    # 1. Density blindness + orthogonality.
    radii, _, a = O.field_on_grid(M, K, LAM, R, 32, 128)
    radii, a = radii, O.normalize(a, radii, R, 128)
    _, _, b = O.field_on_grid(-M, -K, LAM, R, 32, 128)
    b = O.normalize(b, radii, R, 128)
    da, db = O.density(a), O.density(b)
    worst = max(abs(da[i][j] - db[i][j])
                for i in range(len(radii)) for j in range(len(da[0])))
    inner = O.inner_product(a, b, radii, R, 128)
    print("1. Density blindness and orthogonality:")
    print(f"   max |rho_opp - rho| = {worst:.3e} (exact: the opposite is")
    print("   invisible to any density-only measurement)")
    print(f"   |<psi_m | psi_-m>| = {abs(inner):.3e} (distinct states)")
    print()

    # 2. Winding and angular momentum.
    print("2. Measured winding and angular-momentum reading (hbar = 1):")
    for m in (-3, -2, -1, 0, 1, 2, 3):
        k = TWO_PI * N / R
        w = O.ring_winding(m, k, LAM, R)
        wo = O.ring_winding(-m, -k, LAM, R)
        print(f"   m = {m:+d}: winding {w:+d} (L_z = {w:+d} hbar)  |  "
              f"opposite winding {wo:+d} (L_z = {wo:+d} hbar)")
    print()

    # 3. Standing waves.
    print("3. Standing waves from a mode superposed with its opposite:")
    for m in (1, 2, 3):
        nodes = O.azimuthal_node_count(m, K, LAM, R)
        print(f"   m = {m}: azimuthal nodes = {nodes} (expected 2|m| = {2 * m})")
    radial = O.radial_node_count(K, LAM, R)
    print(f"   m = 0: radial nodes = {radial} (expected 2n = {2 * N})")
    print()

    # 4. Gate symmetry + negative controls.
    pairs = [(m, TWO_PI * n / R) for m in (-2, -1, 0, 1, 2) for n in (1, 2, 3, 4, 5, 6)]
    admitted, _ = O.count_closing(pairs, R)
    opp_admitted, _ = O.count_closing([(-m, -k) for (m, k) in pairs], R)
    opp_set = set(opp_admitted)
    alone = [p for p in admitted if (-p[0], -p[1]) not in opp_set]
    total = 0
    for seed in (0, 1, 42):
        ad, _ = O.count_closing(O.random_candidates(500, seed), R)
        total += len(ad)
    print("4. Gate symmetry (opposite gate: m integer, |n| positive integer):")
    print(f"   {len(admitted)}/{len(pairs)} modes admitted, "
          f"{len(opp_admitted)}/{len(pairs)} opposites admitted, "
          f"{len(alone)} admitted alone (expected 0)")
    print(f"   Negative control, random candidates: {total}/1500 admitted")
    print(f"   k = 0 refused: {not O.closes(M, 0.0, R)}, "
          f"half-integer m refused: {not O.closes(1.5, K, R)}, "
          f"half-integer |n| refused: {not O.closes(M, TWO_PI * 2.5 / R, R)}")
    print()

    # 5. Rings.
    print("5. Quantised ring radii (mode and opposite share them):")
    print(f"   rings = {[round(r, 4) for r in O.quantized_radii(K, R)]}")
    print(f"   opposite rings identical: "
          f"{O.quantized_radii(K, R) == O.quantized_radii(-K, R)}")
    print()
    print("Limits: toy reading, not a physical law. No Schrodinger equation,")
    print("no Maxwell solution, no spin, no Coulomb term, no real atom.")
    print("See README.md.")


if __name__ == "__main__":
    main()
