# spiral-quantum-opposite

The quantum opposite of a spiral-envelope mode. Companion to
`spiral-envelope-atoms` (classical wave toy on a 2D disk).

## Model

Same disk, same field:

```
psi(r, theta) = exp(-r/lam) * exp(i*(m*theta + k*r)),  disk radius R = 1
```

The **quantum opposite** of a mode `(m, k)` is its reversed-winding
partner `(-m, -k)`: same envelope, opposite helicity. For this field form
the opposite field is exactly the complex conjugate of the original,
because the envelope is real. This is a chosen toy definition, not a
derived physical law.

## What "quantum" means here

The original package reads the field as a classical wave amplitude. This
package adds a quantum *reading* of the same field, nothing more:

1. **Normalisation** on the polar grid with the area measure `r dr dtheta`,
   so the total is 1 and `|psi|^2` reads as a probability density.
2. **Quantised winding**: the field is an eigenfunction of `-i d/dtheta`
   with eigenvalue `m`, so the angular-momentum reading is `L_z = m*hbar`
   (units `hbar = 1`). The winding is *measured* from the field's phase
   around a ring, not assumed.
3. **Interference**: superpositions add as amplitudes, so densities do
   not add: `|psi + psi_opp|^2` differs from `|psi|^2 + |psi_opp|^2` by an
   interference term.

## The gate, generalised by one line

The original gate admits `(m, k)` when `m` is an integer and `k*R/(2*pi)`
is a *positive* integer `n`. Applied literally to the opposite partner,
the radial count would be `-n` and the original gate would refuse it —
but a fit count cannot be negative: the pitch `p = 2*pi/|k|` fits the
radius `|n|` times regardless of winding direction. So the opposite gate
states the radial condition in `|k|`:

```
admitted  <=>  m integer AND |k|*R/(2*pi) a positive integer
```

For every `k > 0` mode this agrees exactly with the original gate. It
only makes the gate symmetric: a mode is admitted if and only if its
opposite is admitted.

## Measured results

Canonical case: `lam = 0.5, m = 2, n = 3, R = 1`. Run `python3 demo.py`
to reproduce.

| Result | Measured |
|---|---|
| Density difference, mode vs opposite | exactly `0.0` — no density-only measurement can tell them apart; the helicity sign lives in the phase alone |
| Overlap `<psi_m \| psi_-m>` | `7.754e-18` — distinct quantum states |
| Measured winding, mode vs opposite | `+2` vs `-2`, so `L_z = +2 hbar` vs `-2 hbar` |
| Standing wave, `psi_m + psi_-m` | azimuthal nodes `2` (m=1), `4` (m=2), `6` (m=3) = `2\|m\|` |
| Standing wave, `m = 0` pair | radial nodes `6` = `2n` (a `cos(k r)` wave, not azimuthal) |
| Gate symmetry | `30/30` modes and `30/30` opposites admitted (`m` in `-2..2`, `n` in `1..6`), `0` admitted alone |
| Negative controls | `0/1500` random candidates admitted; `k = 0`, half-integer `m`, half-integer `\|n\|` all refused |
| Ring radii | `[1/3, 2/3, 1]`, identical for mode and opposite |

Edge case: for `m = 0` the opposite is its own radial conjugate
(winding `0` both sides). The pair superposes into a radial standing
wave instead of an azimuthal one.

## Honest limits

- Synthetic toy only. No claim about real atoms, real electromagnetism,
  or quantum mechanics.
- The field is **not** a solution of the Schrodinger equation (no
  Hamiltonian, no potential, no Coulomb term, no spin) and **not** a
  solution of Maxwell's equations.
- The closure rule and the opposite definition are chosen toy rules,
  not physical laws.
- The polar grid avoids `r = 0` (half-offset radii).
- Standard library only; no third-party dependencies.

## Usage

```
python3 demo.py
python3 -m unittest discover -s tests -v
```

## Authorship and licence

Author: Jean-Francois Brisson (Spark AI NLP). AGPL-3.0-only.
Companion to `spiral-envelope-atoms`; it contains no code from any
other author.
