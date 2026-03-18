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
GOLA started from a frustration I kept coming back to when reading and building operator-learning models for PDEs. A lot of them were clearly powerful, but the way they handled space often felt too generic for the actual structure of the problem. If I am dealing with Navier-Stokes style systems, then locality is not an optional aesthetic preference. Geometry is not metadata. The domain, the relative positions of points, and the local coupling structure all belong to the object I am trying to learn. So I did not want a model that first flattened everything into a sequence and only later tried to remember that the points lived somewhere. I wanted the geometry to appear at the beginning, in the construction of the token, in the graph, and in the attention rule itself.

That is the point of GOLA. At the most direct level, it is a scaffold for learning one-step PDE time-advance operators of the form

$$
\mathcal{T}_{\Delta t}: u(\cdot, t) \mapsto u(\cdot, t + \Delta t)
$$

using geometry-induced sparse attention rather than dense global token mixing. But if I say only that, it sounds like a mild engineering variation. For me the project is more serious than that. It is an attempt to encode a scientific claim into the model itself: if the operator is local, then the architecture should be local in a meaningful geometric sense, not merely sparse because sparse happens to be cheaper.

<figure class="image-card">
  <img src="/images/gola-attention.png" alt="Sparse geometric attention visualization from GOLA">
  <figcaption>The actual GOLA repository includes dataset-backed and synthetic visualizations showing why sparse geometric attention is a natural fit for local operator structure.</figcaption>
</figure>

The actual repository is grounded in a fairly concrete setup. The current implementation centers on one-step Navier-Stokes operator learning. The dataset class expects data shaped like `[num_trajectories, time_steps, H, W, channels]`, with the usual incompressible-flow interpretation where the channels can correspond to velocity components and pressure. Each sample returns `u_t`, `u_t_next`, `x`, and `node_weight`. That choice matters. I did not want to treat the dataset as an arbitrary tensor pipeline where coordinates are an afterthought. Returning coordinates and quadrature weights explicitly forces the operator perspective. The sample is not just “an image at one time and another image later.” It is a discretized field on a geometric domain, and the model is supposed to learn the map between fields.

Once I committed to that perspective, tokenization also became straightforward. The token is not a word-like unit and not a patch in the vision-transformer sense. The token is a geometric state attached to a location:

$$
\tau_i^t = (x_i, u_i^t).
$$

That is one of the cleanest ideas in the whole project. No positional encoding is necessary, because the position is already part of the token. No causal mask is necessary, because this is not language generation. No padding logic is fundamental to the formulation. The model is being asked to learn an operator over geometric states, so the representation should admit that openly. I like this because it removes a lot of decorative machinery that would otherwise make the code look modern while actually obscuring what problem is being solved.

From there, the next step is the graph. GOLA builds a static geometry graph using either `radius_graph(x, r)` or `knn_graph(x, k)`. I prefer thinking about this as a declaration of admissible interaction rather than just a data structure. A point can attend only to points that are meaningfully near it according to the geometry I decided to trust. The graph stores relative positions and pairwise distances, so attention is conditioned not only on features but on the spatial relation itself. This is where the model stops behaving like a generic sparse transformer and starts behaving like a physically motivated operator learner.

The layer rule reflects that:

$$
u_i^{(l+1)} = u_i^{(l)} + \sum_{j \in N(i)} \alpha_{ij}^{(l)} W^{(l)}u_j^{(l)} w_j.
$$

I find it helpful to read this as a learned local quadrature rule. The model is not simply “passing messages.” It is approximating a nonlinear integral operator over a restricted neighborhood that comes from geometry. The attention weights are learned, yes, but they are learned inside a structure that already says something about the operator class I believe I am dealing with. That distinction matters to me. A lot of machine-learning language tends to collapse every architecture into some version of feature mixing. Here I want the mathematics to remain visible.

Training follows the same logic. The code does include the ordinary field loss, but I did not want to stop there because PDE learning becomes misleading if one only reports a single MSE number. So the project also exposes physics-aware penalties such as `divergence_penalty_2d`, `kinetic_energy_consistency_loss`, and `enstrophy_error_2d`. I do not claim that these solve everything. They do not. But they force the training loop to acknowledge that physical structure is part of the target, not an optional decoration to mention in the abstract and ignore in the implementation.

Another part of GOLA that I care about a lot is the mundane engineering. The repository supports local `.npy` and `.npz` datasets, direct Hugging Face dataset loading, bounded-neighbor graph construction, memory-aware execution, and a low-memory profile aimed at machines with limited RAM. This may sound secondary next to the model idea, but for research code it really is not. A beautiful method that only works on an idealized hardware setup is not a serious scaffold. I wanted the project to be usable under constraints, because that is the environment in which most actual research iteration happens.

I also spent time on visualization because sparse geometric attention is easier to understand when you can actually see the neighborhood structure. The repository includes scripts that produce both static and interactive visualizations, and I think that is important for two reasons. First, it makes debugging easier. Second, it gives the project a kind of scientific legibility. When I look at a visualization of the sparse neighborhood pattern on a domain with geometry, I can ask whether the pattern even makes sense before I ask whether the validation number improved.

One thing I do not want to overclaim is that GOLA is already the final answer. It is not. There are open questions I still care about. How robust are the neighborhoods when the mesh becomes irregular in more extreme ways? How should local attention behave across obstacles, boundaries, or domains with more complicated topology? Can the learned local quadrature view be made more explicit theoretically, rather than only implicitly suggested by the implementation? And perhaps most importantly, what evaluation protocol best reveals whether the model has actually learned a useful operator rather than a shallow surrogate that looks good on a limited split?

Those questions are part of why this project remains active research for me rather than a completed artifact. GOLA is not just a codebase I want to showcase. It is a place where several of my research instincts meet: geometry-aware learning, scientific machine learning, structured sparsity, and the demand that architecture reflect the mathematical character of the system rather than merely fit the data.

There is also a philosophical reason I keep returning to it. If I borrow a Newtonian sensibility, what matters in a scientific model is not that it reproduces outcomes case by case, but that it expresses a lawlike form through which the outcomes become intelligible. Newton did not make mechanics powerful by listing positions of bodies. He proposed a structured relation between force, motion, and time. In a much humbler and modern computational setting, I think operator learning should aspire to something similar. Not a table of successful predictions, but an architecture whose form says why those predictions should generalize.

That is why I resist the temptation to treat sparse attention here as merely an efficiency trick. Efficiency matters, obviously. Going from dense \(O(N^2)\) interaction to neighborhood-based \(O(Nk)\) interaction is not trivial. But the more important point is that sparsity comes from a claim about what should interact. It is justified by the geometry and by the locality of the operator, not by a late-stage optimization pass.

So when I describe GOLA, I do not think of it first as “my transformer-style PDE project.” I think of it as an attempt to keep operator learning honest. The data structure, the token, the graph, the layer rule, the losses, and even the resource constraints all point in the same direction: build a model that remembers what kind of mathematical object it is trying to learn.

## Related Note

For a shorter essay on the same idea, see [Why Geometry Matters in Operator Learning]({{ '/blog/2026/03/16/geometry-and-operator-learning/' | relative_url }}).
