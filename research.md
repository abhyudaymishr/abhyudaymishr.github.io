---
last_modified_at: "2026-11-16"
description: "Explore Abhyuday Mishra’s completed GOLA neural operator work, collaborative qudit simulation, and research in knot recognition and scientific ML."
seo_title: "Scientific ML & Quantum Computing Research | Abhyuday Mishra"
math: true
title: "Scientific machine learning & quantum computing research"
permalink: /research/
kicker: Research
intro: "Research centered on geometry-aware operator learning, with collaborative work in qudit simulation and topological machine learning."
---
## Completed Work

### GOLA and Operator Learning

I completed [GOLA, a geometric neural operator]({{ '/projects/gola/' | relative_url }}), a project for learning one-step PDE time-advance operators with sparse geometry-induced attention. The project explored whether local geometric structure should be encoded directly in the operator architecture instead of being approximated through dense global token mixing.

The work covered:

- geometry-aware sparse neighborhoods
- one-step operator learning for Navier-Stokes style systems
- physics-aware losses such as divergence, energy, and enstrophy penalties
- memory-bounded training setups that stay realistic on limited hardware

The project focused on making operator-learning systems more faithful to the geometry and numerical structure of the physical problems they model. Related work includes [neural operators for Navier–Stokes systems]({{ '/projects/navier-stokes-operators/' | relative_url }}) and the note on [geometry in operator learning]({{ '/blog/2026/03/16/geometry-and-operator-learning/' | relative_url }}).

## Collaborative and Adjacent Directions

### Qudit Simulation and Quantum Computing

My [qudit quantum circuit framework work]({{ '/projects/qudit-circuit-framework/' | relative_url }}) covers higher-dimensional circuit design and collaborative simulation software. This includes collaborative work on simulation frameworks, generalized QFT-style constructions, and questions about how to represent and optimize quantum circuits when the local Hilbert space is not restricted to qubits.

### Topological Learning and Knot Recognition

My [knot-type recognition project]({{ '/projects/knot-recognition/' | relative_url }}) studies a hybrid ML and topology problem. Here the goal is to combine geometric or diagrammatic representations with explicit topological structure such as Gauss or PD-like codes and classical invariants.

### Research Engineering

Projects such as [NanoTransformer]({{ '/projects/nanotransformer/' | relative_url }}) and [Oculon’s spatiotemporal forecasting and MCP tools]({{ '/projects/oculon/' | relative_url }}) reflect my interest in research systems as much as model ideas: reproducible training pipelines, interpretable baselines, clean dataset contracts, and tooling that can be extended into future experiments rather than discarded after a single run.

## Research Questions

- When does locality beat full attention in operator learning?
- How should geometry enter the attention mechanism instead of being treated as a post-hoc feature?
- What abstractions make general qudit circuit construction practical for experimentation?
- How can transformer-style models help optimize high-dimensional quantum circuits?
- Which combinations of knot invariants and learned representations best support knot-type classification?
- Which operator-learning benchmarks reveal failure modes rather than hiding them?

## Mathematical Lens

For incompressible flow and operator learning, a useful framing is

$$
\mathcal{G}: a(x) \mapsto u(x), \qquad \nabla \cdot u = 0
$$

where the key modeling decision is how architecture encodes the structure of the operator $\mathcal{G}$ rather than only fitting samples.

For knot learning, a parallel question is how much of the topology should be given to the model explicitly through invariants such as

$$
\Delta_K(t), \qquad V_K(q)
$$

versus learned from diagrams, braid words, or geometric embeddings.
