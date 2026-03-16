---
title: "GOLA: Geometric Neural Operator with Sparse Local Attention"
summary: "A neural operator architecture that uses geometry-constrained sparse attention instead of dense global mixing."
status: "Active research"
timeline: "2026"
image_alt: "Abstract geometric field visualization for GOLA"
topics:
  - Neural Operators
  - Sparse Attention
  - PDE Learning
order: 1
---
GOLA is motivated by a simple question: if PDE operators are local and structured, why should the model behave as if every token must attend to every other token?

The project explores sparse attention patterns tied to geometry and neighborhood structure. The goal is to improve both computational efficiency and inductive bias for operator learning on physical systems.

Current lines of work:

- encode spatial locality directly into attention masks
- compare sparse attention against Fourier and message-passing baselines
- study stability on fluid and transport benchmarks
