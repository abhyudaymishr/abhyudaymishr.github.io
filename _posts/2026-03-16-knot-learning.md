---
title: "Learning Knot Invariants with Neural Networks"
date: 2026-03-16
---
Knot recognition can be viewed as a classification problem over topological embeddings, diagrams, and braid representations.

One practical route is to compute classical invariant features first, such as the Alexander polynomial

$$
\Delta_K(t)
$$

and the Jones polynomial

$$
V_K(q),
$$

then combine those features with a neural model that also sees the geometry or combinatorics of the knot.

The broader question is not only whether a model can classify knot type, but which parts of the topology should be provided explicitly and which can be learned from data.
