# Volcanoes or Microbes? Modeling the End-Permian Carbon Crisis

An interactive carbon-cycle simulator for the 02-120 Programming for Scientists
final project (Fall 2026).

## Scientific question

What pushed so much carbon into the end-Permian ocean that it helped cause
Earth's largest mass extinction: volcanic eruptions, a microbial bloom, or both
working together?

Each source leaves a different fingerprint. Volcanoes and microbes add carbon at
different rates over time, and with different carbon isotope signatures (δ13C),
which are recorded in the rocks. This project asks how those fingerprints arise
and whether they can tell the culprits apart.

## Inspiration

The project is inspired by Rothman et al., "Methanogenic burst in the
end-Permian carbon cycle" (*PNAS* 111:5462–5467, 2014). The authors argue that
carbon in the ocean grew faster than exponentially at the extinction. That is
hard to explain with volcanoes alone but fits the explosive spread of a
methane-producing microbe, *Methanosarcina*. They propose that the microbe had
just gained a faster way to make methane, and that nickel from Siberian
volcanism removed the limit on its growth.

The project is a simulation and needs no external data. A copy of the paper is
in `sources/rothman2014.pdf`.

## What the paper says

**The argument is about shape, not amount.** Rothman et al. reconstruct `M`, the
carbon added to the ocean's dissolved inorganic carbon (DIC), as a fraction of
its starting size. Their constraints "derive only from the shape of M(t), not the
quantity of isotopically light carbon required" (p. 5463). This is why the
model can use arbitrary units.

- A single large eruption makes `M` grow sublinearly, because the ocean takes up
  less CO2 as it acidifies.
- Many scattered volcanic vents make `M` grow linearly.
- Methane hydrate release makes `M` grow no faster than linearly.
- The rock record shows `M` growing exponentially or faster.

**Their microbe model (Eqs. 2–6).** `A` is the total methane produced, and the
carbon added to the ocean grows in proportion to it (`M ∝ A`).

| Eq. | Equation | Meaning |
| --- | --- | --- |
| 3 | `dA/dt = β·K` | Methane production = metabolic rate `β` × population. The population is always at its carrying capacity `K`. |
| 2 | `K = k0 + k1·A` | Making methane uses up sulfate and O2, which enlarges the microbes' niche. |
| 4 | `β = β0 + β1·A` | Microbes become more efficient as the event goes on, for example through warming, adaptation, or better access to nutrients. |
| 5 | `dA/dt = a0 + a1·A + a2·A²` | Eqs. 2–4 combined, with `a0 = β0·k0`, `a1 = β1·k0 + β0·k1`, `a2 = β1·k1`. |
| 6 | `A(t) ≈ 1 / (a2·(tc − t))` | Near the critical time `tc`, `A` blows up (superexponential growth). |

With a constant `β` (`β1 = 0`), growth is exponential. With `β1 > 0`, it blows
up at `tc`, which matches the rock record. The paper gives no values for `k0`,
`k1`, `β0` or `β1`, because only the shape is fitted.

**Values from the paper:**

| Quantity | Value | Where |
| --- | --- | --- |
| δ13C of the added carbon (`δ′i`) | −28‰, representing remineralized organic carbon | p. 5463, Fig. 1B |
| Drop in carbonate δ13C at Meishan, China | about 7‰ over about 100 kyr, "first slowly, and subsequently rapidly" | p. 5462 |
| Peak extinction | about 252.28 million years ago, dates resolved within ±0.08 Myr | Fig. 1 |
| Most species lost within | 20,000 years | p. 5462 |
| Time scale `τ` | 100 kyr | Fig. 2 |
| Largest `M` reached | about 0.3–0.4 (DIC grew by 30–40%) | Figs. 1B, 2A |
| Growth law near the end | `M ∝ 1/(tc − t)`, slope −1 on log–log axes | Fig. 2C |
| Organic carbon required | 7,000–14,000 Gt C | p. 5464 |
| Nickel at Meishan | at least 2× higher before the δ13C spike than after, up to 7× just before the sharp drop | p. 5466, Fig. 4 |
| Age of the acetoclastic *Methanosarcina* ancestor | 240 ± 41 million years | Fig. 3 |
| Energy cost of the new pathway | 1 ATP per acetate, compared with 2 for the older pathway | p. 5464 |

## What it will do

The simulator tracks the ocean's store of dissolved carbon and its δ13C over
time, solving the model's equations step by step. It will run as a web app.

- **Carbon sources:** volcanic carbon added at a steady or pulsed rate, and a
  microbial source that follows Rothman's model (Eq. 5, below), where nickel
  controls how quickly the microbes speed up.
- **Carbon sink:** carbon removed by burial at a rate proportional to how much
  is in the ocean.
- **Controls and output:** users turn each source on or off and adjust its size
  and timing, then see plots of carbon amount, growth rate and δ13C over time.

## Progress

| Step | Status |
| --- | --- |
| 1. One ocean carbon reservoir with a steady volcanic source and burial | Done |
| 2. Automated checks (exact solution, time step, growth slows) | Done |
| 3. Carbon isotopes (δ13C) | Not started |
| 4. Microbial source (Rothman's Eq. 5), with nickel setting how fast the microbes speed up | Not started |
| 5. Compare volcanoes alone, microbes alone, and both | Not started |
| 6. Plots and web app | In progress: sliders and plots for the steady volcanic source |
| 7. Nickel → microbe → carbon chain | Not started |

The current model is:

```
dM/dt = F − k·M
```

| Symbol | Meaning |
| --- | --- |
| `M` | carbon in the ocean |
| `Mi` | carbon in the ocean at the start (t = 0) |
| `F` | rate at which volcanoes add carbon |
| `k` | burial rate constant (fraction of ocean carbon buried per unit time) |

Units are arbitrary for now.

## Files

| File | What it does |
| --- | --- |
| `carbon.py` | The model. `findrate` gives dM/dt, `simulate` steps the model forward with Euler's method, and `exact_solution` gives the exact answer for checking. |
| `main.py` | Runs one example and prints the exact and simulated carbon at t = 10. |
| `app.py` | The web app. Sliders set `Mi`, `k`, `F`, the run length and the time step, a checkbox turns volcanoes off, and plots show carbon (simulated and exact) and its growth rate over time. |
| `requirements.txt` | Python packages the app needs (Streamlit). |
| `test_carbon.py` | Checks. `test_matches_exact_solution` fails if any step of `simulate` is more than 0.001 from `exact_solution`. `test_halving_dt` fails if halving the time step changes the final carbon by 0.001 or more. `test_growth_slows` fails unless, with a steady source, carbon rises at every step and each increase is smaller than the last. |

## Running it

Requires Python 3.9 or later.

### The web app

The app needs Streamlit. From the repository root, set it up once:

```
python3 -m venv .venv
.venv/bin/pip install -r project/requirements.txt
```

Then start the app:

```
.venv/bin/streamlit run project/app.py
```

It opens in your browser at http://localhost:8501.

### Without the app

`main.py` and the checks need no extra packages. From the repository root:

```
python3 project/main.py
```

With `Mi = 1.0`, `F = 0.5`, `k = 0.1` and `dt = 0.01`, it prints the exact
carbon at t = 10, then the simulated value:

```
3.5284822353142307
3.5292183009161437
```

To run the checks:

```
python3 project/test_carbon.py
```

## How it is checked

The main check reproduces the core of Rothman's argument. A steady volcanic
source should make ocean carbon grow more and more slowly. Only a source that is
itself growing, like a spreading microbe, can make carbon grow faster and
faster. With a steady input `F` and burial at rate `k`, the model has an exact
solution that the simulation must match:

```
M(t) = F/k + (Mi − F/k)·e^(−kt)
```

The current simulation matches it to within 0.001 at every step with
`dt = 0.01`.

Further checks:

1. **Isotope mixing by hand:** adding carbon equal to 10% of the ocean's store
   at δ13C = −28‰ (remineralized organic carbon, as in Rothman et al.) to an
   ocean at 0‰ gives −280/110, about −2.5‰.
2. **Microbial growth, constant rate:** with `β1 = 0`, Eq. 5 becomes
   `dA/dt = a0 + a1·A`, which has an exact exponential solution that the
   simulation must match.
3. **Microbial growth, speeding up:** with `β1 > 0`, the simulation must blow
   up near `tc` like Eq. 6, `A ≈ 1/(a2·(tc − t))`, and each step's increase must
   be larger than the last. This mirrors the volcano check, where each increase
   is smaller.
4. **Numerical accuracy:** halving the time step should barely change the
   results. This already holds: making `dt` ten times smaller makes the error
   ten times smaller, as expected for Euler's method.

## Where it is going

After the core model, the project will model the chain Rothman proposes:
volcanism releases nickel, which lets the microbe grow, which releases carbon.
The paper names nickel as the trigger but leaves it out of its equations. This
project puts it in, by letting the nickel level set `β1`, how quickly the
microbes speed up. It will ask how much nickel, delivered how quickly, would be
needed to trigger a methanogenic burst, and whether the volcanic carbon alone
could have done the damage.

## Changes from the proposal

After reading Rothman et al. in full, two parts of the original proposal were
changed to follow the paper:

1. **Microbial growth uses Rothman's Eq. 5 instead of logistic growth.**
   Logistic growth speeds up and then levels off, so it cannot produce the
   faster-than-exponential growth the rock record shows. It would leave the
   microbe looking like another slowing source, much like the volcano. Eq. 5
   speeds up until it blows up at `tc`, which is what the record shows, and it
   gives exact results (Eqs. 5 and 6) to check the simulation against.
2. **The added carbon is −28‰, not −60‰.** −60‰ is typical of methane itself,
   but in Rothman's scenario all the methane is oxidized back to CO2. Carbon is
   conserved through that chain, so the added carbon carries the δ13C of the
   organic matter it came from, about −28‰. This changes how much carbon is
   needed for the 7‰ drop, but barely changes the shape of `M(t)`. The app will
   offer both values for comparison.
