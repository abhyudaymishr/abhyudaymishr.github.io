---
title: "Knot-Type Recognition"
permalink: /projects/knot-recognition/
summary: "A scientific knot-analysis pipeline that combines image classification, heuristic Gauss/PD extraction, and protein-knot experiments."
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
This project implements a scientific pipeline for knot recognition from images, pairing a learned classifier with explicit geometric and topological heuristics.

The actual repository goes beyond a simple classifier. It combines a ResNet-based CNN for knot-type prediction with a structured Gauss/PD extraction stack operating on skeletonized drawings, plus a second pipeline for protein-knot analysis from projected C-alpha backbones.

<div class="image-grid">
  <figure class="image-card">
    <img src="https://mathworld.wolfram.com/images/eps-svg/FigureEightKnot_700.svg" alt="Figure-eight knot illustration">
    <figcaption>The 2D drawing pipeline starts from knot images, where crossing structure and local geometry drive both classification and symbolic code extraction.</figcaption>
  </figure>
  <figure class="image-card">
    <img src="https://www.researchgate.net/publication/321279745/figure/fig1/AS%3A963465938235395%401606719588042/Selected-knot-and-link-diagrams.gif" alt="Selected knot and link diagrams">
    <figcaption>The project also treats knot analysis as a structural problem: simplify diagrams, propose moves, and recover symbolic codes rather than only predict labels.</figcaption>
  </figure>
</div>

## Objective

The repository is built around two related goals:

- classify knot drawings from images
- extract interpretable topological structure such as Gauss and PD-like codes

This makes the project useful both as a machine learning system and as a topological analysis tool.

## System Architecture

The current implementation is hybrid by design:

- **CNN classifier** for knot-type prediction from images
- **preprocessing and skeletonization** to convert drawings into tractable graph structure
- **heuristic Gauss/PD extraction** to recover symbolic knot information
- **Reidemeister move candidate detector** for local structural simplification analysis
- **diagram reducer / solver** that simplifies skeletons before optional classification
- **protein-knot pipeline** for projection-based surrogate knot typing from 3D backbones

## 2D Drawing Pipeline

For 2D knot drawings, the workflow is:

1. preprocess the image and generate a skeleton
2. build a graph over skeleton pixels
3. prune spurs and simplify junction structure
4. pair crossing edges heuristically
5. traverse the graph to recover Gauss and PD-like codes
6. optionally run classification, move detection, or reduction on top of that structure

This is important because the project does not treat knot recognition as a pure black-box vision task. It explicitly tries to recover interpretable structure from the image.

## Protein Knot Pipeline

The repository also includes a projection-based protein knot workflow:

- extract C-alpha backbones from KnotProt-style protein data
- project 3D curves into 2D from sampled viewpoints
- detect crossings in projection space
- assign over/under information using depth
- build signed Gauss-style event sequences
- train a hybrid classifier from projection images plus structural features

That makes the project broader than a synthetic drawing classifier. It also functions as an experimental topological ML pipeline for biological structure.

## Scientific Value

What makes the project interesting is the combination of:

- reproducible ML experiments
- symbolic topological code extraction
- diagram simplification heuristics
- structural features that can be audited rather than guessed

It sits at a useful boundary between topology, computer vision, and scientific machine learning, with clear relevance to topological quantum computing and geometry-aware representation learning.

## Current Limits and Extensions

The source project notes several limitations:

- Gauss/PD extraction is heuristic and sensitive to binarization artifacts
- chirality inference is still heuristic
- protein projection methods approximate topology rather than proving it exactly

That makes the next research steps clear: stronger invariant-level baselines, better uncertainty calibration, and tighter comparisons between exact topology and learned surrogates.

## Source Project

Repository: [github.com/abhyudaymishr/knot_recognition](https://github.com/abhyudaymishr/knot_recognition)
