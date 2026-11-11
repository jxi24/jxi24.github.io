---
layout: page
title: ResBos2
description: A tool for transverse momentum resummation for vector bosons at hadron-hadron colliders.
img: assets/img/publication_preview/Isaacson_2017hgb.png
importance: 1
category: Collider
---

**ResBos2** is a resummation code for single vector boson ($W$, $Z$, $\gamma^*$) production at hadron colliders. It resums the large logarithms that appear at small boson transverse momentum, giving accurate predictions for the $q_T$ spectrum and the lepton kinematics behind precision electroweak measurements such as the $W$-boson mass. ResBos2 is a rewrite of the original ResBos code, which the Tevatron and LHC experiments used widely. I started the rewrite during my PhD at Michigan State University.

## Highlights

- Accuracy raised from NNLL+NLO in the original ResBos to **N$^3$LL+NNLO**
- **IFY**, a new non-perturbative function that depends on the boson's rapidity, fitted to fixed-target, Tevatron, and LHC data. The fit finds only mild rapidity dependence.
- Applied to the CDF $W$-mass measurement, which used the older NNLL+NLO ResBos. CDF's data-driven techniques capture most of the higher-order corrections, and including them would lower the reported mass by at most 10 MeV. That is far too small to explain the $7\sigma$ tension with the Standard Model.
- Studies of what this extra precision means for future $W$-mass and electroweak measurements at the LHC

## Links

- Thesis: J. Isaacson, _ResBos2: Precision Resummation for the LHC Era_, PhD thesis, Michigan State University (2017), [doi:10.25335/M5DG44](https://doi.org/10.25335/M5DG44)
- Isaacson, Fu & Yuan, _ResBos2 and the CDF W mass measurement_, [_Phys. Rev. D_ **110**, 094023 (2024)](https://arxiv.org/abs/2205.02788)
- Isaacson, Fu & Yuan, _Improving ResBos for the precision needs of the LHC_, [_Phys. Rev. D_ **110**, 073002 (2024)](https://arxiv.org/abs/2311.09916)
