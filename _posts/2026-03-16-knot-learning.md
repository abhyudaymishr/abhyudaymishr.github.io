---
title: "Learning Knot Invariants with Neural Networks"
date: 2026-02-01
---
Knot recognition becomes interesting the moment I stop treating it as a normal image-classification task. If the goal were merely to assign labels to line drawings, then a reasonable CNN and a decent dataset might already get me most of the way. But that is not really what the subject is asking for. Knot theory is not about recognizing a picture. It is about recognizing an object that stays the same across many changes of picture. The topological content of the problem begins exactly where surface appearance becomes unreliable.

That is why I think knot learning has to be framed around invariance from the beginning. A knot diagram can be stretched, redrawn, thickened, thinned, projected differently, simplified, or made noisy while still representing the same knot type. If a model only learns to associate certain visual textures or local motifs with labels, it may still perform well on a benchmark while learning the wrong notion of sameness. That is what makes the problem so appealing. It forces machine learning to confront a stricter standard of identity than ordinary pattern recognition usually demands.

One classical response is to compute invariant features explicitly. The Alexander polynomial

$$
\Delta_K(t)
$$

and the Jones polynomial

$$
V_K(q)
$$

are obvious examples. They are valuable because they are not merely descriptive features in the ML sense. They are mathematically motivated summaries of structure that survives legitimate deformation. Once these invariants enter the pipeline, the learning problem changes. The model is no longer being asked to conjure topology out of raw appearance all by itself. It is being asked to work in conversation with the topology.

I find that conversation more interesting than either extreme. A fully symbolic pipeline can become brittle in the face of noisy or imperfect inputs. A purely neural pipeline can become shallow because it never has to justify what kind of sameness it has learned. A hybrid approach, on the other hand, admits that the task contains both perceptual and structural difficulty. Images are messy. Topology is exacting. A serious system should account for both.

This is why I like approaches that begin from images but do not end there. Skeletonization, graph extraction, crossing analysis, Gauss-code recovery, PD-like symbolic descriptions, and candidate Reidemeister moves all push the task toward interpretability. They force the pipeline to surface the structure it believes it is using. Even if those steps are heuristic and imperfect, they change the style of reasoning. Instead of asking only “what label does the network predict?” I can also ask “what structural object did the system think it saw?” That is a much better research question.

The same logic becomes even more compelling when I step beyond clean diagrams and think about protein-knot settings or other projection-based problems. There the distinction between raw appearance and latent structure becomes unavoidable. A projected curve can hide or distort exactly the information the topology cares about. If the model can still extract useful symbolic traces or combine learned features with structured encodings, then the result feels more meaningful than a mere image prediction.

There is a philosophical question underneath all of this that topology has always carried: what remains identical when appearance changes? That is not only a technical question. It is almost a training ground for thinking clearly about representation itself. In many machine-learning tasks, the labels are treated as if they attach directly to the visible input. In topology, that assumption fails immediately. The same object can appear in many guises, and the surface can change a great deal without altering the underlying identity.

I sometimes find it helpful to think about this in an Advaita-like register, not as a mystical claim but as an interpretive aid. The visible diagram is the changing appearance. The invariant is closer to the stable object of knowledge. A model that attends only to the appearance may still become impressive at the level of prediction, but it has not necessarily learned what the problem considers essential. That distinction matters. A benchmark may reward visual regularities. The mathematics rewards invariance under deformation.

This is why I do not want neural networks to replace topology here. I want them to be disciplined by topology. The point is not to show that a network can classify knots without classical structure, as though leaving out the mathematics were a sign of strength. The point is to ask how learned systems can collaborate with topological structure in a way that remains both robust and interpretable. That seems like the more mature question.

There is also a practical benefit to this view. Once symbolic structure is part of the pipeline, errors become easier to inspect. If the crossing graph is wrong, I can see that. If the skeletonization breaks, I can see that. If the Gauss-code heuristic becomes unstable, I can inspect where it went off course. A pure classifier often collapses all these failure modes into a confidence score, which is far less informative for research. Hybrid systems may be messier, but they are often more legible.

Of course, the hybrid route has its own difficulties. Symbolic extraction from imperfect images is fragile. Over-under assignments can be ambiguous. Chirality can become subtle. Invariants are informative but not always complete. Projection-based pipelines approximate topological structure rather than capturing it with theorem-level certainty. I do not think any of these are reasons to avoid the problem. They are reasons to formulate the problem honestly. Knot learning becomes compelling exactly because it refuses to be reduced to a single clean methodological story.

There is another reason I care about the topic. Knot theory sits near several areas I already find compelling: geometry-aware learning, structured representation, and topological quantum computing. Once I treat knot recognition as a problem of learning under invariance constraints, it stops looking like a niche curiosity and starts looking like a general lesson. The lesson is that learning works better when it is forced to answer to the right notion of equivalence.

That idea reaches beyond knots. Many scientific problems are like this. Two objects can look different while belonging to the same structured class, or look similar while differing in the only way that matters. Knot theory simply makes the point sharply and elegantly. It gives machine learning no place to hide from the question of what counts as identity.

So when I think about learning knot invariants with neural networks, I do not primarily think about beating a classification baseline. I think about building systems that can see and reason at different levels at once: image level, graph level, symbolic level, invariant level. The stronger system is not the one that ignores topology most successfully. It is the one that uses learning to meet topology on its own ground.
