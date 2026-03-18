---
title: "Learning Knot Invariants with Neural Networks"
date: 2026-02-01
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

That makes the project more than a vision problem. Once a pipeline begins extracting Gauss codes, PD-like descriptions, or Reidemeister-style simplification candidates, the task changes from "label this image" to "recover the structure that makes the knot what it is."

Philosophically, topology has always asked a deep identity question: what remains the same when appearance changes? A knot diagram can be stretched, redrawn, projected, or simplified while still representing the same underlying object. In an Advaita-like interpretive language, the surface drawing is the changing appearance, while the invariant is closer to the stable object of knowledge.

Machine learning becomes interesting precisely at that boundary. A classifier sees patterns, but topology asks whether those patterns survive transformation. So the real problem is not only predictive accuracy. It is whether the model is anchored to the invariants that justify the classification.

This is why hybrid pipelines are attractive here. Neural models are good at perception, denoising, and robust pattern extraction. Symbolic topological tools are good at identity through deformation. Putting them together is not a compromise between old and new methods. It is a recognition that the task itself has both perceptual and structural layers.

The strongest version of knot learning, then, is not a network that replaces topology. It is a network disciplined by topology.
