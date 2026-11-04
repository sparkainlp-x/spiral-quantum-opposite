"""Spiral quantum opposite: the opposite-helicity partner of a spiral-envelope mode.

Companion to ``spiral-envelope-atoms`` (classical wave toy on a 2D disk)::

    psi(r, theta) = A(r) * exp(i * (m * theta + k * r)),
    A(r) = exp(-r / lam),  disk radius R (default 1).

The opposite
------------
The quantum opposite of a mode ``(m, k)`` is its reversed-winding partner
``(-m, -k)``: the same envelope, the opposite helicity.  For this field
form the opposite field is exactly the complex conjugate of the original
field, because the envelope is real::

    psi_opp(r, theta) = psi(r, theta)*   (conjugate)

This is the time-reversed partner in the same sense that conjugating a
travelling wave reverses its direction of travel.  It is a chosen toy
definition, not a derived physical law.

The quantum reading (what "quantum" means here, and what it does not)
--------------------------------------------------------------------
The original package reads the field as a classical wave amplitude.  This
package adds a quantum *reading* of the same field, nothing more:

1. Normalisation: the field is normalised on the polar grid with the area
   measure ``r dr dtheta``, so ``sum |psi|^2 r dr dtheta = 1`` and
   ``|psi|^2`` reads as a probability density.
2. Quantised winding: the field is an eigenfunction of ``-i d/dtheta``
   with eigenvalue ``m``, so the angular-momentum reading is
   ``L_z = m * hbar`` (units ``hbar = 1``).  The winding ``m`` is
   *measured* from the field's phase around a ring, not assumed.
3. Interference: superpositions are added as amplitudes, so densities
   do not add: ``|psi + psi_opp|^2`` differs from ``|psi|^2 + |psi_opp|^2``
   by an interference term.

What this is NOT: the field is not a solution of the Schrodinger
equation (there is no Hamiltonian, no potential, no Coulomb term, no
spin), not a solution of Maxwell's equations, and not a real atom.  The
word "quantum" here names the normalisation + eigenvalue + interference
reading, applied to a synthetic toy field.

The gate, generalised by one line
---------------------------------
The original gate admits ``(m, k)`` when ``m`` is an integer and
``k * R / (2*pi)`` is a *positive* integer ``n``.  Applied literally to
the opposite partner ``(-m, -k)``, the radial count would be ``-n`` and
the original gate would refuse it -- but a fit count cannot be negative:
the pitch ``p = 2*pi / |k|`` fits the radius ``|n|`` times regardless of
the winding direction.  So the opposite gate states the radial condition
in ``|k|``::

    admitted  <=>  m integer AND |k| * R / (2*pi) a positive integer.

For every ``k > 0`` mode this agrees exactly with the original gate; it
changes nothing for the original package.  It only makes the gate
symmetric under the opposite operation: a mode is admitted if and only
if its opposite is admitted.

Measured results (canonical case lam = 0.5, m = 2, n = 3, R = 1)
----------------------------------------------------------------
1. Density blindness: ``|psi_opp|^2`` equals ``|psi|^2`` exactly (max
   difference 0.0).  No density-only measurement can tell a mode from
   its opposite; the helicity sign lives in the phase alone.
2. Orthogonality: ``<psi_m | psi_{-m}>`` is 0 to within 1e-12 for
   ``m != 0``: a mode and its opposite are distinct quantum states.
3. Winding flips sign: measured winding ``+2`` vs ``-2``, so the
   angular-momentum reading is ``+2 hbar`` vs ``-2 hbar``.
4. Interference reveals the opposite: ``psi_m + psi_{-m}`` is an
   azimuthal STANDING wave proportional to ``cos(m theta)`` with
   exactly ``2|m|`` nodes (4 for m = 2, 6 for m = 3, 2 for m = 1).
5. Gate symmetry: all 30 pairs ``(m, n)`` with ``m`` in ``-2..2`` and
   ``n`` in ``1..6`` are admitted together; none is admitted alone.
   Negative controls: 0/1500 random candidates admitted; ``k = 0``,
   half-integer ``m``, and half-integer ``|n|`` all refused.
6. Rings unchanged: the opposite shares the original's quantised ring
   radii ``[p, 2p, ..., R]`` (for n = 3: ``[1/3, 2/3, 1]``).
7. Edge case ``m = 0``: the opposite of an ``m = 0`` mode is its own
   radial conjugate; the pair superposes into a RADIAL standing wave
   proportional to ``cos(k r)`` with ``2n`` nodes (6 for n = 3).  The
   azimuthal standing wave has no nodes because there is no winding
   to reverse.

Only the Python standard library is used.
"""

import cmath
import math
import random

TWO_PI = 2.0 * math.pi

# Frozen-gate tolerance, as in the original package: far above float64
# rounding for the values used here (order 1e-15) and far below any
# genuine near miss (order 1e-2).
GATE_TOL = 1e-9


def envelope(r, lam):
    """Decaying radial envelope ``exp(-r / lam)``."""
    if r < 0:
        raise ValueError("radius r must be >= 0")
    if lam <= 0:
        raise ValueError("decay length lam must be > 0")
    return math.exp(-r / lam)


def pitch(k):
    """Spiral pitch ``p = 2*pi / |k|`` (a length, so the magnitude)."""
    if k == 0:
        raise ValueError("k = 0 has no finite pitch (no radial cycle)")
    return TWO_PI / abs(k)


def radial_cycles(k, radius):
    """Signed radial phase cycles across the disk: ``k * R / (2*pi)``."""
    return k * radius / TWO_PI


def _is_integer(value, tol=GATE_TOL):
    """True when ``value`` is within ``tol`` of an integer."""
    return abs(value - round(value)) <= tol


def opposite(m, k):
    """The quantum opposite of mode ``(m, k)``: ``(-m, -k)``."""
    return (-m, -k)


def closes_original(m, k, radius):
    """The original gate: ``m`` integer and ``k * R / (2*pi)`` a positive
    integer.  Kept for comparison; it refuses every opposite partner
    with ``k < 0`` because its radial count is negative."""
    if not _is_integer(m):
        return False
    n = radial_cycles(k, radius)
    if not _is_integer(n):
        return False
    return round(n) >= 1


def closes(m, k, radius):
    """The opposite gate: ``m`` integer and ``|k| * R / (2*pi)`` a
    positive integer.  Symmetric: ``closes(m, k) == closes(-m, -k)``,
    and identical to the original gate for every ``k > 0``."""
    if not _is_integer(m):
        return False
    n = abs(radial_cycles(k, radius))
    if not _is_integer(n):
        return False
    return round(n) >= 1


def mode_numbers(m, k, radius):
    """``(m, |n|)`` for a mode admitted by the opposite gate, else ``None``.

    For ``k > 0`` this matches the original package's ``(m, n)``.
    """
    if not closes(m, k, radius):
        return None
    return (int(round(m)), int(round(abs(radial_cycles(k, radius)))))


def quantized_radii(k, radius):
    """Ring radii ``[p, 2p, ..., R]`` for an admitted mode, else ``None``.

    Identical for a mode and its opposite, since the pitch uses ``|k|``.
    """
    numbers = mode_numbers(0, k, radius)
    if numbers is None:
        return None
    n = numbers[1]
    p = pitch(k)
    return [j * p for j in range(1, n + 1)]


def field(r, theta, m, k, lam):
    """Complex field ``psi(r, theta)`` for one mode."""
    return envelope(r, lam) * cmath.exp(1j * (m * theta + k * r))


def field_on_grid(m, k, lam, radius, n_r=32, n_theta=128):
    """Field sampled on a polar grid (half-offset radii, so r = 0 is avoided).

    Returns ``(radii, thetas, values)`` where ``values[i][j]`` is
    ``psi(radii[i], thetas[j])``.
    """
    if n_r < 1 or n_theta < 1:
        raise ValueError("grid sizes must be >= 1")
    radii = [(i + 0.5) * radius / n_r for i in range(n_r)]
    thetas = [TWO_PI * j / n_theta for j in range(n_theta)]
    values = [[field(r, t, m, k, lam) for t in thetas] for r in radii]
    return radii, thetas, values


def _cell_area(radius, n_r, n_theta):
    """Polar cell area element ``dr * dtheta`` (the ``r`` factor is applied
    per row by the caller)."""
    return (radius / n_r) * (TWO_PI / n_theta)


def normalize(values, radii, radius, n_theta):
    """Normalise a grid field so ``sum |psi|^2 r dr dtheta = 1``."""
    n_r = len(radii)
    dcell = _cell_area(radius, n_r, n_theta)
    norm_sq = sum(
        abs(values[i][j]) ** 2 * radii[i] * dcell
        for i in range(n_r)
        for j in range(n_theta)
    )
    if norm_sq <= 0:
        raise ValueError("cannot normalise a zero field")
    inv = 1.0 / math.sqrt(norm_sq)
    return [[values[i][j] * inv for j in range(n_theta)] for i in range(n_r)]


def density(values):
    """Probability density ``|psi|^2`` on the same grid."""
    return [[abs(v) ** 2 for v in row] for row in values]


def inner_product(a, b, radii, radius, n_theta):
    """``<a | b> = sum conj(a) * b * r dr dtheta`` on the grid."""
    n_r = len(radii)
    dcell = _cell_area(radius, n_r, n_theta)
    total = 0.0j
    for i in range(n_r):
        for j in range(n_theta):
            total += a[i][j].conjugate() * b[i][j] * radii[i] * dcell
    return total


def _wrap_to_pi(angle):
    """Wrap an angle difference to ``(-pi, pi]``."""
    return (angle + math.pi) % TWO_PI - math.pi


def winding_number(row):
    """Winding measured from the field's phase around one ring.

    Sums the wrapped phase steps around the ring (closing the loop back
    to the first sample) and divides by ``2*pi``.  Returns the nearest
    integer; the raw value is within float rounding of it.
    """
    n = len(row)
    total = 0.0
    for j in range(n):
        cur = cmath.phase(row[j])
        nxt = cmath.phase(row[(j + 1) % n])
        total += _wrap_to_pi(nxt - cur)
    return int(round(total / TWO_PI))


def ring_winding(m, k, lam, radius, ring_index=0, n_r=32, n_theta=128):
    """Measured winding of mode ``(m, k)`` on one grid ring."""
    _, _, values = field_on_grid(m, k, lam, radius, n_r, n_theta)
    return winding_number(values[ring_index])


def _count_below_threshold_runs(profile, threshold):
    """Count maximal runs of samples below ``threshold * max(profile)``.

    Each run is one node (or nodal region) of the standing wave.
    """
    peak = max(profile)
    if peak <= 0:
        raise ValueError("profile has no positive peak")
    runs = 0
    inside = False
    for v in profile:
        if v < threshold * peak:
            if not inside:
                runs += 1
                inside = True
        else:
            inside = False
    return runs


def azimuthal_node_count(m, k, lam, radius, n_theta=128, threshold=0.10):
    """Nodes of the standing wave ``psi_m + psi_{-m}`` on one ring.

    The superposition density is proportional to ``cos^2(m theta)``
    times the (constant-on-a-ring) envelope squared, so its nodes are
    the ``2|m|`` zeros of the cosine.  Returns 0 for ``m = 0``: with no
    winding to reverse, the pair forms a radial standing wave instead.
    """
    if m == 0:
        return 0
    _, _, a = field_on_grid(m, k, lam, radius, 1, n_theta)
    _, _, b = field_on_grid(-m, -k, lam, radius, 1, n_theta)
    row = [a[0][j] + b[0][j] for j in range(n_theta)]
    profile = [abs(v) ** 2 for v in row]
    return _count_below_threshold_runs(profile, threshold)


def radial_node_count(k, lam, radius, n_r=256, threshold=0.10):
    """Nodes of the ``m = 0`` pair's radial standing wave.

    The pair ``psi_0 + psi_0-opp`` is proportional to ``cos(k r)`` times
    the envelope, so after dividing out the known envelope squared the
    profile is ``cos^2(k r)`` with ``2|n|`` nodes inside the disk
    (``|n| = |k| * R / (2*pi)``).
    """
    if k == 0:
        raise ValueError("k = 0 has no radial standing wave")
    radii = [(i + 0.5) * radius / n_r for i in range(n_r)]
    profile = []
    for r in radii:
        s = field(r, 0.0, 0, k, lam) + field(r, 0.0, 0, -k, lam)
        env_sq = envelope(r, lam) ** 2
        profile.append(abs(s) ** 2 / (4.0 * env_sq))
    return _count_below_threshold_runs(profile, threshold)


def count_closing(candidates, radius):
    """How many ``(m, k)`` candidates the opposite gate admits, and which."""
    admitted = [(m, k) for (m, k) in candidates if closes(m, k, radius)]
    refused = [(m, k) for (m, k) in candidates if not closes(m, k, radius)]
    return admitted, refused


def random_candidates(count, seed, m_range=(-4.0, 4.0), n_range=(-1.0, 5.0)):
    """Negative-control candidates: continuous random ``(m, k)`` pairs.

    ``m`` is uniform in ``m_range`` and ``k`` is drawn so that
    ``k * R / (2*pi)`` is uniform in ``n_range`` (radius fixed to 1
    here; rescale ``k`` by ``1 / radius`` for another disk).  With
    continuous draws, an exact integer hit has probability zero, so the
    gate is expected to refuse every one.
    """
    rng = random.Random(seed)
    out = []
    for _ in range(count):
        m = rng.uniform(*m_range)
        n = rng.uniform(*n_range)
        out.append((m, TWO_PI * n))
    return out
