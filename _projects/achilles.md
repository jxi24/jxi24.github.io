---
layout: page
title: Achilles
description: A CHIcagoLand Lepton Event Simulator
img: assets/img/achilles.png
importance: 1
category: Neutrino
related_publications: true
---

[**Achilles**](https://github.com/AchillesGen/Achilles) ("A CHIcago-Land Lepton Event Simulator") is a modern, theory-driven event generator for neutrino–nucleus and electron–nucleus scattering. It is designed to close the gap between the nuclear-theory community and the precision-era neutrino programs (DUNE, Hyper-K, SBN) that need accurate event simulation with quantifiable uncertainties.

## Physics scope

- Quasielastic scattering and single pion production, with intranuclear cascade transport of the produced hadrons
- Coherent scattering and electron-scattering channels, enabling theory-vs.-data benchmarking on the same footing as neutrino predictions
- Multiple nuclear models — spectral-function based (`QESpectral`, `HyperonSpectral`), a coherent form-factor model, and an interface to external Fortran models — so modeling systematics can be studied consistently

## Implementation highlights

- Phase-space sampling with Vegas-adaptive and multi-channel integration
- Switchable form-factor parametrizations and current-conservation schemes (Coulomb / Weyl / Landau)
- Configurable nuclear densities and Fermi-gas parameters
- Output in [NuHepMC](https://github.com/NuHepMC/Spec) (recommended), legacy HepMC, or native Achilles format; compatible with the NUISANCE analysis framework
- Docker image for reproducible runs

## Links

- Source: [github.com/AchillesGen/Achilles](https://github.com/AchillesGen/Achilles)
- Documentation: [achillesgen.github.io/Achilles](https://achillesgen.github.io/Achilles/)
- Foundational release: [Isaacson et al., _Phys. Rev. D_ **107**, 033007 (2023)](https://arxiv.org/abs/2205.06378)
- Pion production & propagation: [Isaacson et al., _Phys. Rev. D_ **113**, 036005 (2026)](https://arxiv.org/abs/2508.19213)
