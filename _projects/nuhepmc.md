---
layout: page
title: NuHepMC
description: A standardized event file format for neutrino-nucleus event generators.
importance: 2
category: Neutrino
related_publications: true
---

[**NuHepMC**](https://github.com/NuHepMC/Spec) is a standardized event-record format for neutrino event generators — a thin, neutrino-specific layer on top of [HepMC3](https://gitlab.cern.ch/hepmc/HepMC3) that adds conventions for flux, process labelling, vertex metadata, and generator bookkeeping so downstream experiment frameworks can treat any generator identically.

## Why it matters

Neutrino experiments typically consume output from several generators (GENIE, NuWro, NEUT, Achilles, GiBUU, MARLEY, …), which historically used incompatible native formats. Every analysis that compared predictions carried its own ad-hoc converter and subtle bookkeeping bugs. NuHepMC gives experimenters one format to read and gives generator authors one target to write.

## Status

Specification version **1.0.0**, published as [Gardiner, Isaacson & Pickering, arXiv:2310.13211](https://arxiv.org/abs/2310.13211).

- **Native support:** Achilles, GiBUU (2025), MARLEY (v2), NEUT v6+
- **Public converters available:** NuWro, NEUT v5
- **Private converter:** GENIE

## Links

- Specification: [github.com/NuHepMC/Spec](https://github.com/NuHepMC/Spec)
- Reference implementations and tooling: [github.com/NuHepMC](https://github.com/NuHepMC)
- Paper: [arXiv:2310.13211](https://arxiv.org/abs/2310.13211)
