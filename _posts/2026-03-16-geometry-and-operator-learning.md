---
title: "Why Geometry Matters in Operator Learning"
date: 2026-03-16
---
If an operator is local, structured, and tied to a domain geometry, then the model should not behave as though all positions are equally relevant all the time.

That is the motivation behind geometry-aware sparse attention. The point is not only to cut computation. The deeper claim is that architecture should express a hypothesis about the operator itself.

For many PDE settings, the challenge is not just approximation power. It is learning the right structure:

$$
\mathcal{G}_{\theta}: a(x) \mapsto u(x)
$$

with enough bias toward locality and conservation that the model generalizes beyond a convenient benchmark.

In GOLA, that hypothesis is made concrete by treating tokens as geometric objects, building neighborhoods from radius or k-NN graphs, and turning attention into a learned local quadrature rule instead of a dense all-to-all mixer. The engineering move is simple, but the methodological claim is stronger: locality should be built into the architecture when locality is built into the phenomenon.

A Newtonian philosophical reading helps here. Newtonian science does not explain motion by listing outcomes one by one. It explains motion through a structured law relating bodies, forces, and change. Operator learning should be held to a similar standard. If the PDE is local and geometry-bound, then a model that ignores geometry until the last minute is already making the wrong scientific bet.

This is why sparse attention in this setting should not be understood as mere optimization folklore. It is a statement about epistemic discipline. The form of the model says what the researcher believes about the world, or at least about the operator class under study.

That is also why benchmarking must go beyond one-step loss. A model can look impressive while learning the wrong computational habit. Long-horizon rollouts, conservation-sensitive penalties, and ablations on neighborhood structure are not cosmetic extras. They are tests of whether the learned map behaves like an operator or merely imitates one on an easy slice of the dataset.

The broader philosophical point is straightforward: in scientific machine learning, efficiency and realism need not be enemies. A local model can be cheaper because it is truer to the structure of the problem. That is the wager behind geometry-aware operator learning.
