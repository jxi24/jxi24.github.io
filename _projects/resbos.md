---
layout: page
title: ResBos2
description: A tool for transverse momentum resummation for vector bosons at hadron-hadron colliders.
img:
importance: 1
category: Collider
notes_hash: 561c0d4286ea
---

**ResBos2** is a C++ Monte Carlo program that gives fully differential cross sections for W, Z, γ\*, Higgs and diphoton production, and for other processes, at hadron colliders. It includes transverse-momentum resummation in the Collins-Soper-Sterman (CSS) formalism and in the alternative CFG scheme. It is used for precision electroweak work such as W-mass measurements.

## Physics

ResBos2 resums large logarithms of q_T/Q in impact-parameter (b) space. The A, B, C and H coefficients are set order by order. Non-perturbative physics enters through the BLNY or SIYY forms, with a b\* prescription (bMax). The resummed result is matched to fixed order through the Y term. The Y term is the fixed-order result minus its small-q_T asymptotic expansion, and it matters at large q_T.

## Current capabilities

- **Processes:** Drell-Yan, Z (up and down quark channels), W⁺, W⁻, γ\*, and Higgs. Decays to AA, ZZ and WW are supported.
- **Accuracy (per the README):**
  - W/Z/γ\*: NNLO fixed order with NNLL resummation.
  - Higgs: NNLO/NNLL.
  - Diphoton: NLO/NNLL.
  - ZZ: NLO/NLL.
- **Not yet complete:** Several processes (WW, ZZ, AA, H+jet) are not yet fully implemented, so check the README for current status.
- **Cross-section components:** Resummed, asymptotic, delta-sigma, fixed-order, Y term, and total. A resummed-minus-asymptotic piece is provided for the MCFM interface.
- **Inputs and setup:**
  - LHAPDF PDFs.
  - On-shell electroweak scheme with the G_F, M_W, M_Z input set.
  - Scale choice of Q or M_T.
  - VEGAS integration.
  - Resummed grids in Q, q_T and y.
  - HOPPET for splitting-function convolutions.
  - MCFM interface for the fixed-order and Y-term pieces.
- **Output:** Les Houches (LHEF) event files.
- **Fitting:** A fitting framework for non-perturbative functions, using Drell-Yan q_T data from E288, E605, R209, CDF, D0, ATLAS and CMS.
- **Python:** A SWIG-based Python extension.

## Getting and building

The source is in a git repository. Please get in touch for access. The build requires a C++11 compiler, LHAPDF and HOPPET. Optional support for ROOT, YODA, gzip and MPI is enabled through CMake options.

```
mkdir build; cd build
cmake .. -DLHAPDF_ROOT_DIR=... -DHoppet_ROOT_DIR=...
make -jN && make install
```

Run it with:

```
resbos -i resbos.config -o outdir [-s seed] [-g gridGen] [-w write LHE] [-v level]
```

The `-g` option runs the grid-generation mode. Unit and integration tests use GoogleTest.

## Citing

If you use ResBos2, please cite the two ResBos2 papers below, plus the physics papers relevant to your process.

## Key papers

- [Improving resbos for the precision needs of the LHC](https://arxiv.org/abs/2311.09916), Phys. Rev. D
- [ResBos2 and the CDF W mass measurement](https://arxiv.org/abs/2205.02788), Phys. Rev. D

Foundational papers on which the formalism and its inputs are based:

- Soft gluon effects on lepton pairs at hadron colliders (the original W/Z resummation)
- Effects of QCD resummation on distributions of leptons from the decay of electroweak vector bosons
- The nonperturbative regime in QCD resummation for gauge boson production at hadron colliders (BLNY form)
- Universality of the Collins-Soper-Sterman nonperturbative function in gauge boson production (SIYY form)
- Tevatron Run-1 Z boson data and Collins-Soper-Sterman resummation formalism
- Higgs boson production at the LHC with soft gluon effects
- Photon pair production with soft gluon resummation in hadronic interactions
