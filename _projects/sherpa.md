---
layout: page
title: Sherpa
description: Simulation of High-Energy Reactions of PArticles in lepton-lepton, lepton-photon, photon-photon, lepton-hadron, and hadron-hadron collisions.
img: assets/img/sherpa-logo.png
importance: 3
category: Collider
giscus_comments: true
related_publications: true
---

[**Sherpa**](https://gitlab.com/sherpa-team/sherpa) (Simulation of High-Energy Reactions of PArticles) is a full-chain Monte Carlo event generator for collider physics — matrix elements, parton shower, matching and merging, hadronisation, underlying event, and decays. It is one of the workhorse generators for the LHC experiments.

## v3 contributions

Sherpa 3 was released in 2024. My contributions to the v3 series have focused on the parts of the chain most affected by the move to heterogeneous and GPU-accelerated hardware:

- Phase-space generation — improved adaptive and multi-channel sampling
- Tree-level amplitude evaluation on GPUs, in concert with the Pepper effort
- Infrastructure for portable event generation at HL-LHC scales

## Links

- Source: [gitlab.com/sherpa-team/sherpa](https://gitlab.com/sherpa-team/sherpa)
- User manual: [sherpa-team.gitlab.io](https://sherpa-team.gitlab.io/)
- Reference: Sherpa Collaboration, _Event generation with Sherpa 3_, [_JHEP_ **12**, 156 (2024)](https://arxiv.org/abs/2410.22148)
