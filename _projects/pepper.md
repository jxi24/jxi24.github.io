---
layout: page
title: Pepper
description: Portable Engine for the Production of Parton-level Event Records is an efficient parton-level event generator to simulate high-energy physics at colliders such as the LHC.
img: assets/img/pepper.png
importance: 2
category: Collider
notes_hash: 2b54c34ce46a
---

**Pepper** (Portable Engine for the Production of Parton-level Event Records) is a GPU-portable, leading-order parton-level event generator written in C++ with Kokkos. It is built for processes that are expensive on CPUs, especially high-multiplicity final states at the (High-Luminosity) LHC. The same code runs across GPU and CPU back ends.

## The physics problem

Many-jet samples need billions of unweighted events. The cost is set by the unweighting efficiency of the phase-space sampler. Pepper's baseline sampler, Chili, combines phase-space mappings with Vegas adaptive grids. This is called Pepper+Vegas. For processes with many subprocesses and helicity configurations, the weight distribution is broad and efficiency suffers.

## What it can do now

- **Parton-level generation** of leading-order pp processes at 13 TeV. These include Z+jets (for example pp→e⁺e⁻+4j with 134 subprocesses, and e⁺e⁻+5j), tt̄+jets, and pure 4-jet and 5-jet production.
- **Pepper+Flow**, a workflow that uses helicity-conditioned rational-quadratic coupling normalizing flows as phase-space proposals. The flows are initialized from the Vegas grids. They are trained with a variance loss on online batches, plus replay of earlier Pepper evaluations that needs no new matrix-element calls.
- **Two flow setups.** You can use one flow per partonic subprocess. Alternatively, you can use grouped conditional flows with trainable process embeddings, grouped by initial- and final-state parton content.
- **Pyper**, the Python bindings, which exchange device-memory phase-space points and target densities with the flow code. The flow training, checkpointing and generation code is in the public *pepper-flows* repository.
- **Benchmarks** on 4×H100 GPUs, and on a single RTX 4000 Ada. They compare the end-to-end cost, including training, of unweighted samples of 10⁶ to 10⁹ events at thresholds ε = 10⁻³ and 10⁻².

The flow study uses Pepper 1.10.0. It is not a direct comparison with our earlier flow studies of Drell–Yan and tt̄+jets channels, which used continuous flows and RegFlow. This work uses neither.

## Getting Pepper

The source is at [gitlab.com/spice-mc/pepper](https://gitlab.com/spice-mc/pepper). It builds with CMake. It reads a runcard, `pepper.ini`. PDFs are accessed through LHAPDF6. The repository includes unit and system tests and a manual.

## Citing

If you use Pepper, please cite the Pepper paper. If you use the Chili phase-space sampler, please also cite the many-jet paper. If you use the flow workflow, please cite the flow paper as well.

## Key papers

- J. Isaacson et al., *Efficient Event Generation for High-Multiplicity LHC Processes: An End-to-End GPU Workflow with Normalizing Flows*, [arXiv:2608.21338](https://arxiv.org/abs/2608.21338). This is the Pepper+Flow paper.
- E. Bothmann et al., *A Portable Parton-Level Event Generator for the High-Luminosity LHC*, SciPost Phys. 17, 081, [arXiv:2311.06198](https://arxiv.org/abs/2311.06198). This is the Pepper reference.
- E. Bothmann et al., *Efficient precision simulation of processes with many-jet final states at the LHC*, Phys. Rev. D 109, 014013, [arXiv:2309.13154](https://arxiv.org/abs/2309.13154). It describes the Chili sampler and the many-jet benchmarks.

## Related work

Learned phase-space sampling is also developed in MadNIS ([arXiv:2212.06172](https://arxiv.org/abs/2212.06172)) and its successors. The normalizing-flow integration methods build on i-flow and on rational-quadratic spline flows.
