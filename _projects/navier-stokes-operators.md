---
title: "Neural Operators for Navier-Stokes Systems"
summary: "Operator-learning experiments for incompressible fluid systems with an emphasis on structure, locality, and reproducibility."
status: "Ongoing"
timeline: "2025-2026"
topics:
  - Scientific ML
  - Navier-Stokes
  - Reproducible Systems
order: 4
---
I keep this project page separate from GOLA because I do not want a single architecture to stand in for the whole research problem. GOLA is one concrete design inside a broader question that has been occupying me for a while: how should operator-learning systems for incompressible fluid dynamics actually be studied if the goal is scientific understanding rather than benchmark theater? That broader question deserves its own page because the model is only one part of the story. Datasets, rollout protocols, ablations, baselines, preprocessing decisions, and memory constraints all shape what kind of conclusion one is allowed to draw.

For Navier-Stokes style systems, the temptation is always to compress the problem into a clean score and move on. But fluid learning resists that simplification. A model can have excellent one-step accuracy and still drift badly over longer horizons. It can fit local statistics while violating conservation-sensitive structure. It can look good on a benchmark that has quietly encoded shortcuts in the sampling or preprocessing. So when I say this project studies neural operators for Navier-Stokes systems, I mean something more than trying architectures until one of them wins a leaderboard slot. I mean building a research setting in which the failure modes are visible.

That is why the system work matters as much as the model work. I care about benchmark construction, locality-aware architectures, rollout evaluation, geometry-aware preprocessing, and reproducibility in a very practical sense. If two operator models are compared under slightly different data contracts, different rollout lengths, different treatment of boundaries, or different normalization conventions, then the comparison may be rhetorically confident but scientifically weak. This page exists to insist that those surrounding details are not secondary.

In practice, this has meant thinking about how Navier-Stokes data is represented, what exactly the target operator should be, how to evaluate one-step versus multi-step behavior, and what losses actually reflect the things I care about. One-step forecasting is appealing because it simplifies the learning problem, but it also risks creating a false sense of success if the learned map compounds error destructively under rollout. Long-horizon evaluation is harder and often messier, but I trust it more. It asks whether the operator has learned something structurally useful rather than merely something locally predictive.

Locality is another recurring concern. Fluids are not arbitrary token collections. The geometry and the coupling structure matter, especially when the domain becomes irregular or when conservation-related quantities should not be treated as optional. That is one reason GOLA emerged as a concrete architecture within this larger project. But even beyond GOLA, I want the Navier-Stokes operator program to remain architecture-agnostic enough to compare different biases honestly. If I only build one model and one story around it, then I have not really studied the problem. I have only defended a preference.

The reproducibility question is not glamorous, but I take it seriously. Research code in scientific machine learning often inherits the bad habits of both science and software at once: implicit assumptions, underdocumented preprocessing, partial experiment capture, and unstable evaluation settings. I want this project to push against that. A benchmark should be rerunnable. A rollout metric should be defined clearly enough that someone else can reproduce it. A purported architectural improvement should survive a baseline that was implemented with equal care. Otherwise the whole exercise becomes too narrative-driven.

There is also an issue of scale and honesty here. Modern ML makes it very easy to hide weak methodology behind large experiments. Bigger models, more data, longer training, and prettier plots can create an aura of inevitability that the underlying comparison has not earned. Working on Navier-Stokes operators has made me more skeptical of that style. In these problems, the mathematics eventually pushes back. If the model has learned the wrong structure, rollout exposes it. If the preprocessing bakes in shortcuts, transfer breaks down. If locality is essential but treated as optional, generalization becomes brittle.

This is where I find a Galilean lens useful. Galileo did not make motion intelligible simply by collecting more examples of moving things. He insisted on the right mathematical description. In a small and contemporary way, I think learned operators should be judged similarly. Do they speak the mathematical language of flow, or do they merely imitate snapshots well enough to survive a narrow benchmark? I do not ask that question rhetorically. I think it should determine how the experiments are built.

That philosophical stake can be stated more plainly: are we discovering a computational form that respects something real about the physics, or are we just fitting a dataset with elegant vocabulary? I think scientific machine learning becomes interesting precisely when that question is hard. If the answer were obvious, benchmark wins would be enough. They are not enough here.

On the technical side, the project therefore stays focused on things that might look unromantic from the outside: baseline quality, ablation logic, data contracts, normalization choices, rollout metrics, and structure-preserving losses. But those are exactly the things that separate a stable research direction from a sequence of demos. When I say I care about operator learning for Navier-Stokes systems, this is what I mean. I care about the total experimental setting in which an operator can be said to have learned something meaningful.

I also think this page matters because it keeps my own work honest. If I only highlight GOLA, it becomes too easy to tell a clean architectural story. By keeping a broader Navier-Stokes operator page, I force the surrounding research questions to stay visible. What counts as a fair benchmark? Which architectures actually benefit from locality? When do physics-aware penalties help, and when do they simply move error around? How should long-horizon quality be measured? These are not footnotes. They are the research program.

So this project is best read as the wider laboratory around my operator-learning work on fluids. GOLA is one strong line inside it, but the larger ambition is methodological. I want operator learning for physical systems to be studied in a way that is computationally realistic, mathematically legible, and difficult to fake with superficial wins. If that sounds demanding, that is because the subject deserves it.

## Related Note

For the companion essay, see [Structure Before Scale in Fluid Operator Learning]({{ '/blog/2026/03/18/structure-before-scale-in-fluid-operator-learning/' | relative_url }}).
