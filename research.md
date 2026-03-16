---
title: Research
permalink: /research/
kicker: Research
intro: "Research centered on geometry-aware operator learning, with collaborative work in qudit simulation and topological machine learning."
---
## Current Focus

### GOLA and Operator Learning

My main active research direction is **GOLA**, a geometric neural operator for learning one-step PDE time-advance operators with sparse geometry-induced attention. The central design question is whether local geometric structure should be encoded directly in the operator architecture instead of being approximated through dense global token mixing.

In practical terms, this means working on:

- geometry-aware sparse neighborhoods
- one-step operator learning for Navier-Stokes style systems
- physics-aware losses such as divergence, energy, and enstrophy penalties
- memory-bounded training setups that stay realistic on limited hardware

The broader goal is to make operator-learning systems more faithful to the geometry and numerical structure of the physical problems they model.

## Collaborative and Adjacent Directions

### Qudit Simulation and Quantum Computing

I also work on qudit systems and higher-dimensional circuit design. This includes collaborative work on simulation frameworks, generalized QFT-style constructions, and questions about how to represent and optimize quantum circuits when the local Hilbert space is not restricted to qubits.

### Topological Learning and Knot Recognition

Another direction is knot-type recognition as a hybrid ML and topology problem. Here the goal is to combine geometric or diagrammatic representations with explicit topological structure such as Gauss or PD-like codes and classical invariants.

### Research Engineering

I care about research systems as much as model ideas: reproducible training pipelines, interpretable baselines, clean dataset contracts, and tooling that can be extended into future experiments rather than discarded after a single run.

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
