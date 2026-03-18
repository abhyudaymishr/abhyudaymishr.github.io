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
NanoTransformer is a stage-wise implementation of a tiny causal language model with context length `3` and roughly `2.1M` parameters. It includes the full experimental stack rather than only the model definition: tokenizer training, data preparation, training, evaluation, classical baselines, and latency measurement.

## System Design

The project is intentionally built as a complete small system:

- BPE tokenizer training from a raw UTF-8 corpus
- tokenized dataset creation and train-validation splits
- configurable causal LM training
- checkpointed evaluation
- add-k smoothed trigram baseline comparison
- end-to-end latency measurement for inference

The CLI structure reflects that design:

```bash
nanotransformer-train --config /path/to/config.json
nanotransformer-eval --config /path/to/config.json --checkpoint /path/to/checkpoint.pt
nanotransformer-baseline --config /path/to/config.json --k 0.1
nanotransformer-latency --config /path/to/config.json --checkpoint /path/to/checkpoint.pt
```

## Why Keep It Small

Large models can hide poor assumptions behind scale. A compact model cannot. The small size forces the training loop, data handling, evaluation, and benchmark comparison to stay legible. That makes the repository useful as a systems project even beyond the exact model size.

## Research Value

Although it sits outside the site's physics-heavy core, NanoTransformer expresses the same methodological principle as the rest of the portfolio: understanding improves when abstractions are inspectable, baselines are explicit, and experiments can be rerun without hidden infrastructure.

## Philosophical Lens

A Descartes-like methodological rule applies here: reduce the problem until the mechanism becomes inspectable. NanoTransformer is valuable precisely because it is too small to hide behind mystique. It turns language modeling back into something one can audit step by step: corpus, tokenizer, baseline, model, latency, failure mode.

That makes it a useful counterweight to black-box culture. The project asks not only whether a model can perform, but whether the experiment is intelligible enough to teach anything.

## Related Note

For the corresponding essay, see [Why Build a Small Language Model by Hand]({{ '/blog/2026/03/18/why-build-a-small-language-model-by-hand/' | relative_url }}).
