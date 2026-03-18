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
This page describes a **group project** developed with **Manav Seksaria**, **Abhyuday Mishra**, and **Anil Prabhakar**. I want to state that clearly at the start because I do not want the site to turn collaborative work into an individual claim. The simulator and the publication belong to a shared research effort, and that matters to me both ethically and intellectually. In quantum computing especially, a lot of the interesting work sits at the intersection of physics, mathematics, and systems engineering, so it makes sense that the project itself emerged through collaboration.

The project centers on **qudit**, a high-performance simulator for $d$-dimensional quantum systems. The simplest way to explain why that matters is to say that most software ecosystems are still mentally organized around qubits. That is understandable because qubits are the dominant teaching language, and a lot of algorithmic intuition has been built there. But the moment one starts taking higher-dimensional local systems seriously, several assumptions stop being harmless. The gate set changes, the representation of local states changes, the cost model can change, and even the kinds of algorithms or encodings that feel natural begin to shift. A simulator that flattens those differences too early risks teaching the wrong habits.

That is why the central motivation here is not simply “more levels than two.” It is to give qudits the dignity of their own formal and computational treatment. A qudit state lives in a Hilbert space \( \mathcal{H}_d = \mathbb{C}^d \), and the local basis states, generalized Pauli operators, Fourier transforms, and decompositions should all be handled in a way that remains explicit about the dimension. I care about that because abstraction is never neutral. The abstractions a simulator chooses determine what a researcher can easily express, compare, or test.

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

Many physical systems naturally expose more than two useful levels. Trapped ions, photonic systems, and superconducting platforms all provide contexts in which higher-dimensional structure is not artificial. From that perspective, qudits are not an exotic twist added for style. They are often a more faithful description of what the hardware can in principle support. That can translate into higher information density, dimension-sensitive compilation strategies, reduced depth in some constructions, and different fault-tolerance tradeoffs. Of course, none of those benefits come for free. They make the simulation and software story more complicated. But the right response to that complication is better tooling, not conceptual retreat.

Mathematically, the project lives in a very clean framework. A qudit state can be written as

$$
|\psi\rangle = \sum_{k=0}^{d-1} \alpha_k |k\rangle,
\qquad
\sum_{k=0}^{d-1} |\alpha_k|^2 = 1.
$$

That is elementary, but it already highlights the shift. Once \(d\) is not fixed at 2, familiar gate language has to be generalized rather than copied. The shift operator and phase operator become

$$
X|k\rangle = |k+1 \bmod d\rangle,
\qquad
Z|k\rangle = \omega^k|k\rangle,
\qquad
\omega = e^{2\pi i / d}.
$$

These are not decorative generalizations. They define the algebraic atmosphere in which the circuit model lives. Once those operators are native rather than retrofitted, the rest of the software stack becomes more coherent. You can talk about generalized gate libraries, structured circuit representations, and qudit-native transforms without quietly translating everything back into binary language behind the scenes.

One of the most natural examples is the generalized quantum Fourier transform:

$$
\mathrm{QFT}_d |j\rangle =
\frac{1}{\sqrt{d}}
\sum_{k=0}^{d-1} e^{2\pi i jk/d}|k\rangle.
$$

This shows up for all the familiar reasons, including phase estimation and Shor-like structures, but in the qudit setting it also becomes a concrete test of whether the simulator truly understands the local dimension rather than merely tolerates it. If the API and the backend can express the generalized QFT naturally, that is a sign that the abstractions are heading in the right direction.

At the level of software design, I like small clear abstractions. That is why the project can be thought of in terms of objects like `Gate`, `Circuit`, and `StateVector`, with the dimension carried explicitly rather than implicitly assumed. Something like

$$
QuantumCircuit(dimension=d)
$$

is conceptually cleaner to me than a toolkit that treats higher-dimensional systems as an awkward special case inside a fundamentally qubit-first architecture. Good software makes the intended mathematical object easy to think with. Bad software makes the user constantly translate between what the theory says and what the library expects.

The performance side is important too. The title of the paper is **qudit: High-Performance Simulator for Qudit Systems**, and the venue is **2025 Supercomputing India (SCI)** with eCF paper ID `scindia2025__pap367`. I include that not just as a credential line, but because it signals the actual nature of the work. This is not only a conceptual exercise in generalized gates. It is also about making higher-dimensional quantum experiments computationally practical enough to study seriously. There is a big difference between a formalism one can write in a notebook and a simulator one can use to run meaningful tests at scale.

I also think this project sits in an interesting place relative to the rest of my site. The connection to topology is not superficial. Once you start thinking about braid-inspired constructions, generalized gate algebra, and high-dimensional encodings, the distance between algebraic topology and circuit design starts shrinking. The connection to machine learning is also real, though a bit more prospective. I am interested in the idea that neural or graph-based systems could eventually help with circuit simplification, decomposition, or search in qudit-native spaces. That feels much more compelling once the underlying simulator respects the dimension instead of hiding it.

Since this page is on a personal research site, I also want to be honest about how I think about its philosophical side. There is a very tempting habit in technical work to collapse richness into the most familiar special case. Binary language is powerful, convenient, and often beautiful. But convenience can become reduction if it begins to dictate what we regard as a legitimate description. That is where I find the Schrödinger-Vedanta connection suggestive, not as a historical gimmick, but as a reminder that plurality and depth should not be flattened prematurely. In an imagined conversation between Shankaracharya and Schrödinger, the relevant lesson for this project would not be mystical validation of quantum theory. It would be a methodological warning: do not confuse the simplest convenient representation with the full structure of the thing itself.

That is how I read qudit simulation. It is not merely about adding one more feature to a qubit simulator. It is about resisting a representation that has become so dominant that it can make other possibilities seem secondary by default. Once the simulator treats \(d\) as a first-class parameter, more interesting questions become easy to ask. How does compilation scale with dimension? Which algorithms become more natural? What circuit identities are genuinely high-dimensional rather than borrowed from qubit logic? What hardware assumptions become visible when the local space is not artificially compressed?

Because this is a collaborative project, I am careful not to present those questions as if they arise from a single person’s isolated insight. The group dimension matters. The work developed with Manav Seksaria and Anil Prabhakar, and the page is intentionally written to reflect that shared credit. If anything, the fact that this simulator sits at the boundary of theory, performance, and software design makes collaboration even more appropriate.

So if I had to summarize the project in one sentence, I would say this: it is a group effort to make higher-dimensional quantum systems computationally natural instead of conceptually awkward. That is what I find compelling about it. The simulator is useful not only because it computes, but because it teaches a better way to think.

## Related Note

For the shorter research essay version, see [Why Qudits Are Worth Building Tools For]({{ '/blog/2026/03/10/why-qudits-matter/' | relative_url }}).
