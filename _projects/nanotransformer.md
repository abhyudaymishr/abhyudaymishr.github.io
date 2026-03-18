---
title: "NanoTransformer"
summary: "A compact causal language model project that reflects my broader interest in efficient learning systems and research-grade implementation."
status: "Built"
timeline: "2025-2026"
topics:
  - Language Models
  - Systems Engineering
  - Efficient Training
order: 5
---
NanoTransformer looks like an outlier on this site at first glance, and that is reasonable. Most of my work here sits much closer to scientific machine learning, quantum systems, topology, or structured operators. A small language model project seems like it belongs to a different world. But I keep it here because, in a less obvious way, it is driven by the same research instinct as the rest of the portfolio: I want systems that I can fully inspect. I want experiments whose internal structure I actually understand. And I want the implementation to be honest enough that success or failure teaches me something rather than just producing a nice-looking number.

NanoTransformer is a stage-wise implementation of a tiny causal language model with context length `3` and roughly `2.1M` parameters. The number itself is not the interesting part. What matters is that the project includes the whole experimental path, not merely the final network definition. The repository covers tokenizer training, corpus preparation, split generation, model training, evaluation, a trigram baseline with add-k smoothing, and latency measurement. That completeness is the point. I wanted a small system in which every stage of the pipeline remains visible and revisitable.

This matters because contemporary language-model discourse often collapses too many things into “the model.” In practice, the tokenizer, data pipeline, baseline choice, checkpoint evaluation logic, and inference latency can matter as much as the block diagram. A small project is a good place to remember that. When the system is compact, weak assumptions are harder to hide. If the tokenizer is poor, you feel it. If the baseline is too weak, it shows. If latency is ignored, deployment realism disappears. I like NanoTransformer because it puts those concerns back in the foreground.

The repository’s CLI reflects that full-stack perspective. There are separate entry points for training, evaluation, baseline comparison, and latency measurement:

```bash
nanotransformer-train --config /path/to/config.json
nanotransformer-eval --config /path/to/config.json --checkpoint /path/to/checkpoint.pt
nanotransformer-baseline --config /path/to/config.json --k 0.1
nanotransformer-latency --config /path/to/config.json --checkpoint /path/to/checkpoint.pt
```

I like this decomposition because it makes the experiment legible. The tokenizer can be trained from a raw UTF-8 corpus. Token IDs and splits can be built as explicit artifacts. The training loop can be run with a configuration file instead of hidden notebook state. The trigram baseline can be called on equal footing instead of mentioned abstractly and then ignored. Latency can be measured as part of the project rather than treated as a separate production concern that never arrives. None of this is flashy, but it makes the repository much more useful to me as a real research artifact.

The small size is a feature, not a limitation I reluctantly tolerate. Large models can hide a surprising amount of sloppiness behind scale. They can absorb imperfect tokenization, fuzzy evaluation, weak baselines, and vague engineering boundaries simply because the model is big enough to dominate the conversation. A compact model does not allow that kind of laziness. If something is wrong, the wrongness tends to become visible. That is very useful when the goal is understanding rather than prestige.

Another reason I keep this project around is that it acts as a methodological counterweight. In more conceptually loaded areas like quantum simulation or neural operators, it is easy to spend too much time at the level of ideas. A small language model project pulls me back into the discipline of implementation. How clean is the data path? How fair is the baseline? How reproducible is the training run? How much latency is introduced by a change that looks elegant on paper? Those questions are not glamorous, but they are the kinds of questions that keep research from floating away into abstraction.

The presence of a trigram baseline in particular is not accidental. I strongly prefer projects that include a simple classical baseline that can embarrass the fancy model if the fancy model does not deserve its complexity. It is easy to present a transformer as automatically more meaningful than a smoothed n-gram model. But if the evaluation setting is narrow or the implementation is careless, that assumption can become a kind of ritual rather than a result. Including the baseline forces the project to earn its claims.

I also value latency measurement for the same reason. Language modeling often splits into research and systems as if they were separate moral universes. In one, people optimize loss. In the other, they talk about performance. I do not think that divide is healthy. If a model is going to be part of an actual system, latency matters. Even when the model is tiny and the project is educational or exploratory, measuring latency keeps the work concrete. It prevents the repository from pretending that architecture and runtime are unrelated.

There is a philosophical angle here that I find genuinely clarifying. A Descartes-like methodological rule says that if a problem is too complex to understand as a whole, reduce it until the mechanism becomes inspectable. NanoTransformer is valuable to me precisely because it refuses mystique. The project is small enough that I can still see the moving parts: corpus, tokenizer, data preparation, training loop, baseline, evaluation, latency, failure mode. That visibility changes the character of the work. The question stops being “how large a model can I claim to have built?” and becomes “what exactly is this system doing, and how do I know?”

This is also why I reject the idea that small models are automatically just toys. A small model can be a far better teaching and research instrument than a giant opaque one if it preserves the causal structure of the experiment. If the pipeline is inspectable enough, a single bug fix, tokenizer change, or evaluation tweak can teach more than a much larger but less transparent run. NanoTransformer is built in that spirit.

At a more personal level, I think the project helps me maintain balance. Some research areas on this site naturally invite big conceptual language: operators, topology, Hilbert spaces, quantum abstraction. NanoTransformer keeps me responsible to ordinary software truths. Does the script run? Is the artifact path clean? Is the baseline explicit? Can the result be measured? Can another person follow the process from raw text to checkpoint? That discipline is part of good research, not a separate hobby.

So even though NanoTransformer is not the center of my research identity, it belongs here. It represents a mode of working I trust. Build a system small enough to understand, complete enough to test honestly, and structured enough that future work can grow from it without replacing everything. In a field crowded with scale-first narratives, that still feels valuable to me.

## Related Note

For the corresponding essay, see [Why Build a Small Language Model by Hand]({{ '/blog/2026/03/18/why-build-a-small-language-model-by-hand/' | relative_url }}).
