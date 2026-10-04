---
layout: page
title: ResBos2
description: A tool for transverse momentum resummation for vector bosons at hadron-hadron colliders.
img:
importance: 1
category: Collider
related_publications: true
---

[**ResBos2**](https://resbos2.gitlab.io/) is a program for resummed predictions of color-singlet production at hadron colliders, such as Drell–Yan, $W$, $Z$, and Higgs boson production. It is a modern rewrite of the original ResBos code, which was used for vector-boson measurements at the Tevatron and the LHC.

## Why resummation matters

At small transverse momentum, fixed-order perturbation theory breaks down because of large logarithms of $q_T/Q$. ResBos2 resums these logarithms in the Collins–Soper–Sterman (CSS) formalism and matches the result to fixed-order calculations at large $q_T$. This gives a single prediction across the whole spectrum. Precision measurements, including the $W$-boson mass and the weak mixing angle, rely on an accurate description of the vector-boson $q_T$ distribution.

## Highlights

- Higher-order resummation in impact-parameter space, matched to fixed-order perturbative QCD
- Fully differential in the leptonic decay products, so experimental fiducial cuts can be applied directly
- Modern C++ implementation, written for extensibility and for the precision needs of the LHC

## Links

- Documentation: [resbos2.gitlab.io](https://resbos2.gitlab.io/)
- Source: [gitlab.com/resbos2/resbos2](https://gitlab.com/resbos2/resbos2)
- Key papers:
  - Isaacson, Fu & Yuan, _Improving ResBos for the precision needs of the LHC_, [_Phys. Rev. D_ **110**, 073002 (2024)](https://arxiv.org/abs/2311.09916)
  - Isaacson, Fu & Yuan, _ResBos2 and the CDF W mass measurement_, [_Phys. Rev. D_ **110**, 094023 (2024)](https://arxiv.org/abs/2205.02788)
  - Ph.D. thesis: [_ResBos2: Precision Resummation for the LHC Era_](https://d.lib.msu.edu/etd/6889) (Michigan State University, 2017)
