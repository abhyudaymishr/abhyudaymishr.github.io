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
This project grew out of a question I find more interesting than the standard “can a neural network classify images?” version of the problem. In knot theory, the real issue is not simply recognizing a picture. The issue is identifying what stays invariant when the picture changes. A knot diagram can be stretched, redrawn, simplified, projected differently, or drawn with a different hand, while still representing the same topological object. So if I only train a model to classify images by visual pattern, I have not actually met the problem on its own terms. I may have built a competent image classifier, but not a serious knot-analysis system.

That is why the repository is deliberately hybrid. It does contain a ResNet-based CNN for knot-type prediction, because perception still matters. Real images are noisy, line thickness varies, crossings are imperfect, and there is genuine value in a robust learned front end. But the system does not stop at the classifier. It also includes a structured extraction stack operating on skeletonized drawings, with heuristic recovery of Gauss and PD-like information, candidate Reidemeister moves, diagram simplification, and a separate protein-knot workflow based on projected C-alpha backbones. I like that combination because it refuses the false choice between black-box learning and explicit topological structure.

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

The 2D drawing pipeline is where this philosophy becomes concrete. The system begins by preprocessing the image and skeletonizing it so that the drawing can be treated as an analyzable graph rather than a mere bitmap. Once I have a skeleton, I can build a graph over the pixels, prune spurs, simplify junctions, and start reasoning about crossings and connectivity. That step may sound routine if described too fast, but it is actually where the project changes character. A purely image-first pipeline would remain in the world of pattern recognition all the way through. This project instead turns the image into an intermediate structural object that can be traversed, reduced, and interpreted.

From there, the extractor attempts to pair crossing edges heuristically and recover Gauss and PD-like codes. I want to be careful about the language here. The extractor is not magic, and I do not present it as a theorem prover. It is heuristic, sensitive to preprocessing quality, and vulnerable to artifacts introduced by binarization, broken lines, or ambiguous crossings. But that is precisely why I like having it in the loop. It makes the uncertainty visible. When the extractor fails, it usually fails in a way that teaches me something about the relationship between geometry, drawing quality, and symbolic topology. A plain classifier often fails more opaquely.

The repository also includes a Reidemeister move candidate detector and a reducer or solver that simplifies the skeleton before optional classification. That part of the project matters to me because it pushes the pipeline beyond label prediction into something closer to topological reasoning. Even when the move proposals are heuristic, the system begins to ask a recognizably mathematical question: can the diagram be simplified while preserving the knot type? Once that question is active, the model is no longer just reading images. It is working in the neighborhood of diagrammatic topology.

The protein-knot pipeline adds another dimension that I find especially exciting. Instead of starting from synthetic or hand-drawn diagrams, the system can work from projected C-alpha backbones extracted from protein data. The workflow samples viewpoints, projects 3D curves into 2D, detects crossings, assigns over-under information using depth, builds signed Gauss-style event sequences, and then trains a hybrid classifier using both projection imagery and structural features. I do not think of this as a side feature. It is one of the reasons the project feels scientifically alive rather than merely pedagogical. Biological structure introduces noise, ambiguity, and partial observability in a much more interesting way than clean benchmark images do.

What I like most about the project is that it lives on a boundary. It is part computer vision, part topology, part scientific software. The machine-learning component helps with robustness, perception, and pattern extraction. The symbolic component helps with interpretability and with preserving the logic of the underlying mathematical object. The systems component matters because all of this needs to be reproducible, testable, and extendable. The repository reflects that with a package structure, CLI commands, synthetic tests for extraction, documentation, training scripts, and a clear attempt to keep the work inspectable.

In the implementation, that means I can use commands for inference, optional symmetry-invariant feature extraction, move overlays, diagram solving, and training. I can treat the project as a normal ML repository when I want to train a classifier, but I can also use it as a topological analysis environment when I want to inspect extracted structures or experiment with heuristic simplification. That dual use is important. I do not want the project to collapse into either extreme: not just a polished classifier, and not just a symbolic toy disconnected from real image data.

I also appreciate that the source repository documents its own limitations. Chirality detection remains heuristic. Gauss and PD extraction assume reasonably clean high-contrast drawings. Over-under sign inference from skeletons alone is not always reliable. Protein projection methods approximate topology rather than proving it exactly. To me, acknowledging those limits is a strength, not a weakness. It keeps the project honest. A lot of research pages become less interesting when they read as though every hard part has already been solved. Here the open problems are part of the project’s identity.

Those open problems also point to what I would most want to improve next. One direction is stronger invariant-level baselines, so that learned components can be compared more directly against classical topological signals. Another is uncertainty calibration, because a pipeline that mixes heuristics and learned classification should not pretend its confidence is simpler than it really is. A third is tighter comparison between exact topology, approximate symbolic extraction, and learned surrogates. In other words, I want to know not only whether the system works, but which part of it is doing the intellectual heavy lifting in different regimes.

There is also a deep reason I enjoy working on this problem. Topology asks a philosophical question that I think machine learning often forgets to ask: what remains the same when appearance changes? A knot diagram can vary wildly at the visual level while preserving the underlying topological type. That makes knot recognition a good antidote to shallow pattern-matching habits. It forces me to ask whether the model is responding to the right kind of sameness.

If I borrow an Advaita-like metaphor, the visible drawing is the changing appearance and the invariant is closer to the stable object of knowledge. I do not mean that in a mystical way. I mean that the distinction is methodologically useful. The point is not to replace topology with a neural network, but to make learning answer to topology. A model should not be trusted just because it predicts the right label on nearby examples. It should be trusted because its behavior remains anchored to what is actually invariant under legitimate transformations of the object.

That is why I describe this as a scientific knot-analysis pipeline rather than only a knot classifier. The project tries to recover interpretable structure, not just successful outputs. It tries to combine visual robustness with symbolic accountability. And because it reaches into protein data as well, it also asks how topological reasoning might operate in less idealized settings, where the object is not drawn for the model’s convenience.

I think that makes the project genuinely relevant to broader themes in my work. There is a clear connection to topological quantum computing, where braids, invariants, and structured equivalences matter. There is also a connection to geometry-aware learning more generally, because the question is always how much of the structure should be built into the representation rather than left to be inferred from raw signals. Knot recognition is simply a particularly sharp place where that question becomes unavoidable.

## Source Project

Repository: [github.com/abhyudaymishr/knot_recognition](https://github.com/abhyudaymishr/knot_recognition)

## Related Note

For the corresponding essay, see [Learning Knot Invariants with Neural Networks]({{ '/blog/2026/02/01/knot-learning/' | relative_url }}).
