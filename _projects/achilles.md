---
layout: page
title: Achilles
description: A CHIcagoLand Lepton Event Simulator
img: assets/img/achilles.png
importance: 1
category: Neutrino
related_publications: true
notes_hash: 589595016e1c
---

Achilles (A CHIcago Land Lepton Event Simulator) is a modular, theory-driven event generator for electron-nucleus and neutrino-nucleus scattering. It is built for automated beyond-the-Standard-Model (BSM) calculations. Its aim is to provide theory uncertainties for DUNE and other experiments.

## Physics

Achilles factorizes the process into a leptonic current, a nuclear model, and final-state interactions.

- **Leptonic currents** are computed with Berends-Giele recursion through Sherpa/Comix. Arbitrary BSM models can therefore be brought in through UFO files.
- **Nuclear models** include a (global) Fermi gas, relativistic mean field (RMF) configurations, and chiral perturbation theory (ChiPT)-based calculations.
- **Final-state interactions** are described by an intranuclear cascade. It has options for potentials, Coulomb, Landau, Weyl and off-shell treatments.

## Current capabilities

- Lepton-nucleus scattering: charged-current quasielastic (CCQE) scattering and tau production for DUNE. Deep inelastic scattering (DIS) is in development.
- Phase-space sampling with VEGAS and multichannel mappers, plus a partial unweighter.
- Output as HepMC3 events following the NuHepMC convention, written by a plugin.
- A Python plugin interface and a Python package on PyPI, alongside the C++ core.

## Getting and building

Achilles is written in C++ and built with CMake. Build details are on the project's GitHub wiki.

```
mkdir build && cd build
cmake .. -DACHILLES_ENABLE_SHERPA=ON -DSHERPA_ROOT_DIR=/path/to/sherpa
make -jN
```

- HepMC3 (version 3.2.5 or later) is fetched automatically if it is not found. Disable this with `-DENABLE_HEPMC3=OFF`.
- Sherpa is required for BSM calculations. Disable them with `-DENABLE_BSM=OFF`.
- The executable is `build/bin/achilles`, driven by a YAML run card.

## Citing

If you use Achilles, please cite the generator papers:

- [Introducing a novel event generator for electron-nucleus and neutrino-nucleus scattering](https://arxiv.org/abs/2205.06378) (Phys. Rev. D)
- [Novel event generator for the automated simulation of neutrino scattering](https://arxiv.org/abs/2110.15319) (Phys. Rev. D)

Cite the pion paper below if you use the pion or cascade results.

## Key papers

- [Novel event generator for the automated simulation of neutrino scattering](https://arxiv.org/abs/2110.15319): the Berends-Giele leptonic currents in Sherpa/Comix, used for BSM and the leptonic part.
- [Introducing a novel event generator for electron-nucleus and neutrino-nucleus scattering](https://arxiv.org/abs/2205.06378): the generator itself.
- [Single pion production and pion propagation in achilles](https://arxiv.org/abs/2508.19213) (Phys. Rev. D): pion production and the cascade, with MicroBooNE, JSNS2 and JLab inclusive comparisons.
- [Final-state interactions in neutrino-induced proton knockout from argon in MicroBooNE](https://arxiv.org/abs/2406.09244) (Phys. Rev. C).
- [Tau polarization and correlated decays in neutrino experiments](https://arxiv.org/abs/2303.08104) (Phys. Rev. D).
- [New approach to intranuclear cascades with quantum Monte Carlo configurations](https://arxiv.org/abs/2007.15570) (Phys. Rev. C).
- [NuHepMC: A standardized event record format for neutrino event generators](https://arxiv.org/abs/2310.13211): the output standard ([specification](https://github.com/NuHepMC/Spec)).
- [HepMC3 event record](https://arxiv.org/abs/1912.08005): the underlying event record.
