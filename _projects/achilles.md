---
layout: page
title: Achilles
description: A CHIcagoLand Lepton Event Simulator
img: assets/img/achilles.png
importance: 1
category: Neutrino
related_publications: true
notes_hash: 32bc67b46959
---

Achilles (A CHIcago Land Lepton Event Simulator) is a modular, theory-driven event generator for electron-nucleus and neutrino-nucleus scattering. It automates BSM calculations. It is built to provide theory uncertainties for DUNE and other experiments.

## Physics

Achilles factorizes an event into a leptonic current, a nuclear response and a final-state cascade.

- **Leptonic currents** are built with Berends-Giele recursion through Sherpa/Comix. Any BSM model that can be written as a UFO ([UFO 2.0](https://arxiv.org/abs/2304.09883)) can therefore be used without hand-coding new currents ([arXiv:2110.15319](https://arxiv.org/abs/2110.15319)).
- **Nuclear models** include a (global) Fermi gas, relativistic mean-field (RMF) configurations and chiral-perturbation-theory-based calculations.
- **The intranuclear cascade** (final-state interactions) has options for potentials, Coulomb, Landau, Weyl and off-shell treatments.
- **Phase space** is sampled with VEGAS/multichannel mappers and a partial unweighter.

## Current capabilities

- Lepton-nucleus scattering: charged-current quasielastic (CCQE) and tau production for DUNE. DIS is in development.
- Automated BSM scattering through Sherpa.
- Pion production and pion propagation in the cascade. The pion paper compares with MicroBooNE, JSNS2 and JLab inclusive data.
- Output as HepMC3 events following the [NuHepMC](https://github.com/NuHepMC/Spec) conventions ([arXiv:2310.13211](https://arxiv.org/abs/2310.13211)), via a writer plugin. [HepMC3](https://arxiv.org/abs/1912.08005) is the underlying event record.

The longer-term plan extends the generator from QE to DIS. It also aims to add transport and parton-shower-inspired cascade ideas and on-the-fly reweighting for systematics.

## Getting and building

Achilles is written in C++ and built with CMake. A Python plugin and a Python package on PyPI also exist.

```
mkdir build && cd build
cmake .. -DACHILLES_ENABLE_SHERPA=ON -DSHERPA_ROOT_DIR=/path/to/sherpa
make -jN
```

- HepMC3 (≥ 3.2.5) is fetched automatically if it is not found. Disable this with `-DENABLE_HEPMC3=OFF`.
- Sherpa is required for BSM. Disable BSM with `-DENABLE_BSM=OFF`.
- The `achilles` binary (`build/bin/achilles`) is driven by a YAML run card.
- The GitHub wiki, linked from the README, has further build details.

## Citing

Please cite the generator paper, and the other papers below when you use the corresponding features:

- Introducing the generator: [arXiv:2205.06378](https://arxiv.org/abs/2205.06378) (Phys. Rev. D)
- Automated BSM and the leptonic part: [arXiv:2110.15319](https://arxiv.org/abs/2110.15319) (Phys. Rev. D)
- Single pion production and pion propagation: [arXiv:2508.19213](https://arxiv.org/abs/2508.19213) (Phys. Rev. D)

## Key papers

- [Introducing a novel event generator for electron-nucleus and neutrino-nucleus scattering](https://arxiv.org/abs/2205.06378)
- [Novel event generator for the automated simulation of neutrino scattering](https://arxiv.org/abs/2110.15319)
- [Single pion production and pion propagation in Achilles](https://arxiv.org/abs/2508.19213)
- [Final-state interactions in neutrino-induced proton knockout from argon in MicroBooNE](https://arxiv.org/abs/2406.09244)
- [Tau polarization and correlated decays in neutrino experiments](https://arxiv.org/abs/2303.08104)
- [NuHepMC: A standardized event record format for neutrino event generators](https://arxiv.org/abs/2310.13211)
- [New approach to intranuclear cascades with quantum Monte Carlo configurations](https://arxiv.org/abs/2007.15570)
