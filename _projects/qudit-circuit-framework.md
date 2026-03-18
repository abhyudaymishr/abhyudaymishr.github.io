---
title: "Qudit Quantum Circuit Framework"
permalink: /projects/qudit-circuit-framework/
summary: "A group project on high-performance simulation for qudit systems, developed with Manav Seksaria and Anil Prabhakar."
status: "Group project"
timeline: "2025-2026"
image: "https://scx2.b-cdn.net/gfx/news/2023/two-qudits-fully-entan.jpg"
image_alt: "High-dimensional entanglement image for a qudit circuit framework"
topics:
  - Quantum Computing
  - Qudits
  - Circuit Simulation
  - Generalized QFT
order: 2
---
This work is a **group project** developed with **Manav Seksaria**, **Abhyuday Mishra**, and **Anil Prabhakar**.

The project centers on **qudit**, a high-performance simulator for $d$-dimensional quantum systems. Unlike conventional simulators restricted to qubits with $d = 2$, it targets arbitrary local Hilbert-space dimensions and is motivated by practical simulation needs for higher-dimensional quantum computing.

<div class="image-grid">
  <figure class="image-card">
    <img src="https://scx2.b-cdn.net/gfx/news/2023/two-qudits-fully-entan.jpg" alt="Illustration of high-dimensional entanglement in a two-qudit system">
    <figcaption>High-dimensional entanglement is one reason qudit-native simulation tools matter in practice.</figcaption>
  </figure>
  <figure class="image-card">
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Quantum_Logic_Gates.png/500px-Quantum_Logic_Gates.png" alt="Diagram of quantum logic gates">
    <figcaption>Generalized gate libraries extend familiar circuit logic beyond the qubit-only case.</figcaption>
  </figure>
  <figure class="image-card">
    <img src="https://www.researchgate.net/publication/318729550/figure/fig3/AS%3A667647955972114%401536191085766/QFT-circuit-implemented-on-d-level-qudits.png" alt="QFT circuit implemented on d-level qudits">
    <figcaption>The qudit quantum Fourier transform is a key target for generalized circuit design and algorithmic testing.</figcaption>
  </figure>
  <figure class="image-card">
    <img src="https://miro.medium.com/v2/resize:fit:1200/1*DalQlJkwW9kijs8J6iLr0w.png" alt="Quantum circuit visualization">
    <figcaption>Simulator ergonomics matter: abstractions should make high-dimensional circuits easy to inspect, compose, and optimize.</figcaption>
  </figure>
</div>

## Motivation

Many physical quantum systems naturally expose more than two usable levels. Working with qudits can:

- increase information density per site
- reduce circuit depth in some constructions
- improve fault-tolerance tradeoffs on suitable hardware

## Collaboration and Publication

This simulator effort is not presented here as individual work. It is a collaborative project with:

- Manav Seksaria
- Abhyuday Mishra
- Anil Prabhakar

The corresponding publication on the site is:

- **qudit: High-Performance Simulator for Qudit Systems**
- Venue: **2025 Supercomputing India (SCI)**
- eCF Paper Id: `scindia2025__pap367`

## Mathematical Representation

A qudit state lives in the Hilbert space

$$
\mathcal{H}_d = \mathbb{C}^d
$$

with general state

$$
|\psi\rangle = \sum_{k=0}^{d-1} \alpha_k |k\rangle,
\qquad
\sum_{k=0}^{d-1} |\alpha_k|^2 = 1.
$$

## Generalized Gates

The framework is designed around generalized qudit operators such as the shift and phase operators:

$$
X|k\rangle = |k + 1 \bmod d\rangle
$$

and

$$
Z|k\rangle = \omega^k |k\rangle,
\qquad
\omega = e^{2\pi i / d}.
$$

These generate the Weyl-Heisenberg algebra for qudits and provide a natural basis for generalized gate design.

## Generalized Quantum Fourier Transform

One core target is the qudit quantum Fourier transform:

$$
\mathrm{QFT}_d |j\rangle =
\frac{1}{\sqrt{d}}
\sum_{k=0}^{d-1}
e^{2\pi i jk/d}|k\rangle.
$$

This matters for phase estimation, Shor-type algorithms, and high-dimensional quantum models.

## Framework Architecture

The intended simulator API is centered around a small number of clear abstractions:

```python
Gate
Circuit
StateVector
```

with capabilities such as:

- arbitrary local dimension `d`
- unitary evolution
- tensor-product circuit composition
- generalized gate decomposition

Example interface:

```python
QuantumCircuit(dimension=d)
Gate(dimension=d)
```

## Hardware Relevance

Qudit systems appear naturally in trapped ions, photonic systems, and superconducting circuits where higher excited states or multiple internal levels are accessible.

## Research Directions

This framework supports experiments in:

- high-dimensional quantum algorithms
- generalized QFT constructions
- qudit error correction
- topological quantum computation
- neural optimization of qudit circuits

## Connection to the Broader Research Agenda

This project connects directly to the rest of the site:

- **quantum computing** through generalized circuit simulation and compilation
- **topological methods** through braid- and algebra-inspired gate constructions
- **machine learning** through neural optimization and search over circuit structure

One especially interesting extension is a qudit-native transformer or graph model that proposes circuit simplifications or decompositions while respecting dimension-dependent gate algebra.

## Philosophical Lens

There is a useful intellectual bridge here between Schrödinger's openness to Vedantic thought and Shankaracharya's insistence that apparent multiplicity does not necessarily imply ultimate fragmentation. In an imagined Shankaracharya-meets-Schrödinger dialogue, the lesson for this project would be methodological rather than mystical: higher-dimensional structure should not be flattened too early simply because binary language is convenient.

A qudit simulator takes the formal richness of the Hilbert space seriously instead of reducing it immediately to qubit-first habits. The project is therefore not only about faster or broader simulation. It is also about resisting an impoverished representation of the problem.

## Related Note

For the shorter research essay version, see [Why Qudits Are Worth Building Tools For]({{ '/blog/2026/03/10/why-qudits-matter/' | relative_url }}).
