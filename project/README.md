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

The project is a simulation and needs no external data.

## What it will do

The simulator tracks the ocean's store of dissolved carbon and its δ13C over
time, solving the model's equations step by step. It will run as a web app.

- **Carbon sources:** volcanic carbon added at a steady or pulsed rate, and a
  microbial source whose population grows like a living thing, limited by a
  nutrient such as nickel.
- **Carbon sink:** carbon removed by burial at a rate proportional to how much
  is in the ocean.
- **Controls and output:** users turn each source on or off and adjust its size
  and timing, then see plots of carbon amount, growth rate and δ13C over time.

## Progress

| Step | Status |
| --- | --- |
| 1. One ocean carbon reservoir with a steady volcanic source and burial | Done |
| 2. Automated checks (exact solution, time step) | Next |
| 3. Carbon isotopes (δ13C) | Not started |
| 4. Microbial source, limited by nickel | Not started |
| 5. Compare volcanoes alone, microbes alone, and both | Not started |
| 6. Plots and web app | Not started |
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

## Running it

Requires Python 3.9 or later. No other packages are needed. From the repository
root:

```
python3 project/main.py
```

With `Mi = 1.0`, `F = 0.5`, `k = 0.1` and `dt = 0.01`, it prints the exact
carbon at t = 10, then the simulated value:

```
3.5284822353142307
3.5292183009161437
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
   at δ13C = −60‰ (typical of methane-derived carbon) to an ocean at 0‰ gives
   −600/110, about −5.5‰.
2. **Microbial growth:** with the carbon cycle switched off, the microbe
   population must follow the exact logistic growth curve.
3. **Numerical accuracy:** halving the time step should barely change the
   results. This already holds: making `dt` ten times smaller makes the error
   ten times smaller, as expected for Euler's method.

## Where it is going

After the core model, the project will model the chain Rothman proposes:
volcanism releases nickel, which lets the microbe grow, which releases carbon.
It will ask how much nickel, delivered how quickly, would be needed to trigger a
methanogenic burst, and whether the volcanic carbon alone could have done the
damage.
