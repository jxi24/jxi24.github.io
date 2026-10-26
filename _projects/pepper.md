---
layout: page
title: Pepper
description: Portable Engine for the Production of Parton-level Event Records is an efficient parton-level event generator to simulate high-energy physics at colliders such as the LHC.
img: assets/img/pepper.png
importance: 2
category: Collider
notes_hash: 64114a599c5f
---

Pepper, the **P**ortable **E**ngine for the **P**roduction of **P**arton-level **E**vent **R**ecords, is a GPU-portable leading-order parton-level event generator written in C++ with Kokkos. It targets the cost of simulating high-multiplicity final states at the LHC, where large numbers of partonic subprocesses and expensive phase-space integration make billion-event samples, such as those needed for the High-Luminosity LHC, very costly.

## What it does

Pepper computes tree-level matrix elements and generates unweighted parton-level events on GPUs and CPUs from a single code base. Phase space is sampled with the Chili mappings plus adaptive Vegas grids. This is the baseline workflow, called Pepper+Vegas. Pyper, the Python bindings, exchange device-memory phase-space points and target densities with external code without copying them to the host.

## Normalizing-flow workflow

A new workflow, Pepper+Flow, replaces the Vegas proposal with helicity-conditioned rational-quadratic coupling normalizing flows. They are initialized from the Vegas grids and trained with a variance loss on online batches plus a replay buffer of earlier Pepper evaluations. There are two setups: one flow per subprocess, or grouped conditional flows with process embeddings, grouped by parton content.

The benchmarks are leading-order pp collisions at 13 TeV: Z+4j (134 subprocesses), Z+5j, tt̄+4j, and pure 4- and 5-jet production. They use unweighting thresholds of ε = 10⁻³ and 10⁻² and target samples of 10⁶ to 10⁹ events. On 4×H100 GPUs the flows reduce the cost of unweighted samples substantially:

- Speedups reach 109.3× end-to-end, including training, and 245.7× for generation alone.
- A billion unweighted Z+4j events take under a day.
- At the same sample size, Z+5j takes about 5.6 days and tt̄+4j about 2.9 days.

The Vegas baseline is measured at 10⁶ events and extrapolated linearly to larger samples. The paper also reports a single-GPU (RTX 4000 Ada) study. These speedups are not a direct comparison with our earlier flow studies, which used continuous flows and RegFlow.

## Getting Pepper

The source is at [gitlab.com/spice-mc/pepper](https://gitlab.com/spice-mc/pepper). It builds with CMake, and the flow paper uses version 1.10.0. Runs are configured with a runcard (`pepper.ini`), and the repository includes a manual and unit and system tests. The Python flow code for training, checkpoints and generation is in the public repository `pepper-flows`.

## How to cite

Please cite the Pepper reference paper below. If you use the flow workflow, also cite the flow paper. If you use the Chili phase-space sampler, also cite the many-jet paper.

## Key papers

- [A Portable Parton-Level Event Generator for the High-Luminosity LHC](https://arxiv.org/abs/2311.06198), SciPost Phys. 17, 081: the Pepper reference.
- [Efficient precision simulation of processes with many-jet final states at the LHC](https://arxiv.org/abs/2309.13154), Phys. Rev. D 109, 014013: the Chili phase-space sampler and many-jet benchmarks.
- [Efficient Event Generation for High-Multiplicity LHC Processes: An End-to-End GPU Workflow with Normalizing Flows](https://arxiv.org/abs/2608.21338), preprint: the flow workflow described above.
- [Many-gluon tree amplitudes on modern GPUs](https://arxiv.org/abs/2106.06507), SciPost Phys. Codebases: GPU amplitude evaluation for novel event generators.
- [Efficient phase-space generation for hadron collider event simulation](https://arxiv.org/abs/2302.10449), SciPost Phys.: phase-space generation for hadron colliders.
