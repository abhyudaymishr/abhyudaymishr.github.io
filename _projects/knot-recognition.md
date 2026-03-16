---
title: "Knot-Type Recognition"
permalink: /projects/knot-recognition/
summary: "A topological machine learning project for identifying knot types from diagrams, braid representations, and geometric embeddings."
status: "Early research"
timeline: "2026"
image: "https://mathworld.wolfram.com/images/eps-svg/FigureEightKnot_700.svg"
image_alt: "Figure-eight knot diagram"
topics:
  - Topological ML
  - Knot Theory
  - Geometric Learning
  - Quantum Topology
order: 3
---
Goal: automatically identify knot types from embeddings, diagrams, and braid descriptions.

This project treats knot recognition as a structured learning problem over topological objects. The intention is not only to classify knots accurately, but to understand which combinations of invariants and learned representations are actually informative.

<div class="image-grid">
  <figure class="image-card">
    <img src="https://mathworld.wolfram.com/images/eps-svg/FigureEightKnot_700.svg" alt="Figure-eight knot illustration">
    <figcaption>Diagrammatic structure matters: crossings, orientation, and local moves all influence how a model should encode a knot.</figcaption>
  </figure>
  <figure class="image-card">
    <img src="https://www.researchgate.net/publication/321279745/figure/fig1/AS%3A963465938235395%401606719588042/Selected-knot-and-link-diagrams.gif" alt="Selected knot and link diagrams">
    <figcaption>A useful dataset can mix knot diagrams, braid forms, and geometric embeddings rather than relying on a single representation.</figcaption>
  </figure>
</div>

## Representations

The work explores several ways to represent a knot computationally:

- planar knot diagrams
- braid representations
- geometric embeddings in three dimensions
- invariant feature vectors

## Classical Invariants

Some of the most useful classical quantities for this setting are polynomial invariants such as

$$
\Delta_K(t)
$$

for the Alexander polynomial, and

$$
V_K(q)
$$

for the Jones polynomial.

Other candidates include:

- HOMFLY polynomial
- signature and determinant
- knot group representations

## Learning Approaches

Possible model classes include:

- graph neural networks over diagram structure
- topological feature pipelines using invariant vectors
- geometric deep learning on embedded knot curves
- hybrid models that combine exact invariants with learned encoders

## Why This Matters

Knot-type recognition sits at a useful boundary between pure mathematics and machine learning. It also connects naturally to topological quantum computing, where braids and topological structures influence how information is processed.

## Research Direction

An especially interesting question is whether learned models can go beyond memorizing invariants and instead discover useful intermediate representations of knot complexity, symmetry, and equivalence.

