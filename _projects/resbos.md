---
layout: page
title: ResBos2
description: A tool for transverse momentum resummation for vector bosons at hadron-hadron colliders.
img:
importance: 1
category: Collider
notes_hash: 5dcf871b90e0
---

ResBos2 is a C++ Monte Carlo program that gives fully differential cross sections for W, Z/γ\*, and Higgs production at hadron colliders. It also covers diphoton and other processes. It includes Collins-Soper-Sterman (CSS) transverse-momentum resummation, with the alternative CFG scheme selectable as an option. It is used for precision electroweak work such as the W-boson mass.

## Physics

Resummation is done in impact-parameter (b) space. The A, B, C and H coefficients can each be set to a chosen perturbative order. Non-perturbative effects are included through the BLNY or SIYY parametrizations, with a b\* prescription that cuts off the b-space integral at a maximum value, bMax. The cross section can be split into pieces: resummed, asymptotic (the small-q<sub>T</sub> expansion of the fixed-order result), delta-sigma, fixed order, the Y term (fixed order minus asymptotic, which matters at large q<sub>T</sub>), and the total (resummed plus Y term). A W − A piece (resummed minus asymptotic) is also available for the interface to MCFM.

## Current capabilities

- **Processes:** Drell-Yan, Z, γ\*, W⁺, W⁻ and Higgs, with decays to γγ, ZZ and WW.
- **Accuracy (per the README):**
  - W/Z/γ\*: NNLO fixed order with NNLL resummation
  - Higgs: NNLO/NNLL
  - diphoton: NLO/NNLL
  - ZZ: NLO/NLL
- **Limitations:** Several processes (WW, ZZ, γγ and H+jet) are not yet fully implemented.
- **Inputs:** LHAPDF parton distributions, and the on-shell electroweak scheme with the G<sub>F</sub>, M<sub>W</sub>, M<sub>Z</sub> input set. The scale can be Q or M<sub>T</sub>.
- **Integration and grids:** VEGAS integration, and resummed grids in Q, p<sub>T</sub> and y, produced in a dedicated grid-generation mode.
- **Convolutions and interfaces:** HOPPET for splitting-function convolutions, and an MCFM interface for the fixed-order and Y-term pieces.
- **Output:** Les Houches Event Format (LHEF) events.
- **Non-perturbative fits:** A fitting code is included. It uses Drell-Yan p<sub>T</sub> data from E288, E605, R209, CDF, D0, ATLAS and CMS.

## Getting and running it

ResBos2 needs a C++11 compiler, LHAPDF and HOPPET. ROOT, YODA, gzip and MPI support are optional. A Python extension is built with SWIG.

```
mkdir build; cd build
cmake .. -DLHAPDF_ROOT_DIR=... -DHoppet_ROOT_DIR=...
make -jN && make install
resbos -i resbos.config -o outdir [-s seed] [-g gridGen] [-w write LHE] [-v level]
```

For access to the source and release details, please contact me.

## Citing

If you use ResBos2, please cite the two ResBos2 papers:

- [Improving resbos for the precision needs of the LHC](https://arxiv.org/abs/2311.09916), Phys. Rev. D
- [ResBos2 and the CDF W mass measurement](https://arxiv.org/abs/2205.02788), Phys. Rev. D

## Key papers behind the formalism

- Soft gluon effects on lepton pairs at hadron colliders (the original W/Z resummation)
- Effects of QCD resummation on distributions of leptons from the decay of electroweak vector bosons
- Higgs boson production at the LHC with soft gluon effects
- Photon pair production with soft gluon resummation in hadronic interactions
- The nonperturbative regime in QCD resummation for gauge boson production at hadron colliders (the BLNY form)
- Tevatron Run-1 Z boson data and Collins-Soper-Sterman resummation formalism
- Universality of the Collins-Soper-Sterman nonperturbative function in gauge boson production (the SIYY form)
