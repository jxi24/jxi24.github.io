---
layout: page
title: Pepper
description: Portable Engine for the Production of Parton-level Event Records — an efficient parton-level event generator for high-energy collider physics.
img: assets/img/pepper.png
importance: 2
category: Collider
related_publications: true
---

[**Pepper**](https://gitlab.com/spice-mc/pepper) (Portable Engine for the Production of Parton-level Event Records) is a GPU-portable parton-level event generator aimed at LHC and HL-LHC precision simulations. It is built on [Kokkos](https://kokkos.org/), so the same code runs on CPU, NVIDIA, AMD, and Intel hardware without a separate rewrite per backend.

## Why it exists

The HL-LHC is projected to increase Monte Carlo CPU-hour demand by an order of magnitude. Traditional generators are single-threaded and CPU-only; Pepper targets the heterogeneous hardware that HPC centers actually deploy, so the simulation pipeline can scale with the experiments without a commensurate rise in computing cost.

## Highlights

- Cross-vendor GPU portability via Kokkos — one source, multiple accelerators
- Scales from a laptop to leadership-class HPC clusters
- Integrates with Sherpa for the remainder of the event-generation chain (parton shower, hadronisation, …)
- Used in the first published many-jet LHC simulations produced fully on GPUs

## Links

- Source: [gitlab.com/spice-mc/pepper](https://gitlab.com/spice-mc/pepper)
- Documentation: [spice-mc.gitlab.io/pepper](https://spice-mc.gitlab.io/pepper/intro.html)
- Key papers:
  - Bothmann et al., _A Portable Parton-Level Event Generator for the High-Luminosity LHC_, [_SciPost Phys._ **17**, 081 (2024)](https://arxiv.org/abs/2311.06198)
  - Bothmann et al., _Efficient precision simulation of processes with many-jet final states at the LHC_, [_Phys. Rev. D_ **109**, 014013 (2024)](https://arxiv.org/abs/2309.13154)
