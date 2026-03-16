---
title: "GOLA: Geometric Neural Operator with Sparse Local Attention"
summary: "A formal operator-learning scaffold for one-step PDE time-advance operators using geometry-induced sparse attention and physics-aware losses."
status: "Active research"
timeline: "2026"
image: "/images/gola-attention.png"
image_alt: "Sparse geometric attention visualization from the GOLA project"
topics:
  - Neural Operators
  - Sparse Attention
  - PDE Learning
order: 1
---
GOLA is a formal implementation scaffold for learning one-step PDE time-advance operators:

$$
\mathcal{T}_{\Delta t}: u(\cdot, t) \mapsto u(\cdot, t + \Delta t)
$$

using geometry-induced sparse attention rather than dense global token mixing.

<figure class="image-card">
  <img src="/images/gola-attention.png" alt="Sparse geometric attention visualization from GOLA">
  <figcaption>The actual GOLA repository includes dataset-backed and synthetic visualizations showing why sparse geometric attention is a natural fit for local operator structure.</figcaption>
</figure>

## Dataset Formalization

The current implementation is built around one-step Navier-Stokes operator learning. The dataset returns:

- `u_t` and `u_t_next` as field values on the grid
- `x` as geometric coordinates
- `node_weight` as quadrature weights

This makes the model explicitly operator-centric rather than sequence-centric.

## Geometric Tokenization

Tokens are geometric objects of the form

$$
\tau_i^t = (x_i, u_i^t)
$$

with no positional encoding, no padding, and no causal mask. The geometry is already part of the token.

## Sparse Geometry Graph

The repository constructs a static geometry graph using either:

- `radius_graph(x, r)` for local neighborhoods
- `knn_graph(x, k)` for irregular or adaptive settings

Edges store relative position and distance, so attention is grounded in actual spatial structure.

## Sparse Attention as Local Quadrature

At the layer level, GOLA implements a learned local quadrature rule:

$$
u_i^{(l+1)} = u_i^{(l)} + \sum_{j \in N(i)} \alpha_{ij}^{(l)} W^{(l)}u_j^{(l)} w_j
$$

where attention is computed only over geometry-induced neighborhoods instead of the full dense set of tokens.

## Training and Losses

The real project already includes more than a single field MSE objective. It supports:

- `field_mse_loss`
- `divergence_penalty_2d`
- `kinetic_energy_consistency_loss`
- `enstrophy_error_2d`

That makes the project closer to a scientific ML training scaffold than a toy model demo.

## Practical Training Modes

The repository supports:

- local `.npy` or `.npz` PDE datasets
- direct Hugging Face dataset loading
- a low-memory profile targeting sub-8 GB RAM setups
- visualization scripts for sparse geometric attention and interactive 3D inspection

## Why This Version Matters

The main design claim is that operator learning for PDEs should scale like \(O(Nk)\) with local neighborhoods rather than \(O(N^2)\) dense attention, while still preserving the geometric inductive bias needed for physical systems.
