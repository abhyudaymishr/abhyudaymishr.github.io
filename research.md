---
title: Research
permalink: /research/
kicker: Research
intro: "Current directions across operator learning, sparse geometric modeling, and quantum system design."
---
## Research Areas

### Neural Operators

I am interested in architectures that learn maps between function spaces rather than pointwise predictions. In practice, this means studying when inductive bias, locality, and geometry produce better behavior than generic dense attention.

### Geometric Deep Learning for PDEs

Many operator-learning problems inherit mesh structure, locality, and conservation constraints. My work here focuses on sparse neighborhoods, geometry-constrained attention, and architectures that remain computationally realistic.

### Quantum Computing Beyond Qubits

Qudit systems create different tradeoffs in expressivity, synthesis, and hardware assumptions. I am exploring circuit frameworks and algorithmic tooling that make higher-dimensional quantum reasoning easier to test and compare.

### Quantum ML for Circuit Optimization

I am also interested in using neural architectures to optimize or compile quantum circuits, especially in the qudit setting where the search space is richer and the standard qubit-first abstractions become limiting.

### Scientific Machine Learning Systems

The research goal is not only to propose ideas but to build robust experimental systems around them: reproducible pipelines, interpretable baselines, and clean interfaces for future work.

## Research Questions

- When does locality beat full attention in operator learning?
- How should geometry enter the attention mechanism instead of remaining a post-hoc feature?
- What abstractions make general qudit circuit construction usable for experimentation?
- How can transformer-style models help optimize high-dimensional quantum circuits?
- Which operator-learning benchmarks reveal failure modes rather than hiding them?

## Mathematical Lens

For incompressible flow and operator learning, a useful framing is

$$
\mathcal{G}: a(x) \mapsto u(x), \qquad \nabla \cdot u = 0
$$

where the key modeling decision is how architecture encodes the structure of the operator $\mathcal{G}$ rather than only fitting samples.
