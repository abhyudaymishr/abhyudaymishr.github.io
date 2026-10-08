---
title: "Oculon: Spatiotemporal Hotspot Forecasting & MCP Server"
permalink: /projects/oculon/
summary: "An end-to-end spatiotemporal machine learning forecasting engine and Model Context Protocol (MCP) server for 240k+ public safety records in Delhi, evaluated with expanding-window rolling-origin protocols and Wasserstein transport distances."
status: "Built & Deployed"
timeline: "2025-2026"
topics:
  - Spatiotemporal ML
  - Model Context Protocol
  - Spatial Statistics
  - Public Safety AI
order: 2
---
Most predictive policing and spatial risk prototypes fall into one of two traps: either they treat space as arbitrary tabular coordinates with random cross-validation—ignoring future-time leakage—or they report inflated accuracy metrics on aggregated grids that disguise severe spatial transport errors. When predicting events such as missing persons, unidentified deceased individuals, or vehicle thefts across a massive urban territory like the National Capital Territory of Delhi, predictive integrity is not a cosmetic concern. Spatial points have physical meaning, temporal events have causality, and victim privacy must remain inviolable.

**Oculon** is a production-grade spatiotemporal machine learning forecasting system, interactive map explorer, and standard **Model Context Protocol (MCP)** server built to address these exact constraints. It unifies four heterogeneous public safety datasets comprising over **240,000 source events** across Delhi, trains calibrated spatial risk classifiers, and subjects them to rigorous forward-time rolling-origin evaluation.

<div class="cards" style="margin: 1.5rem 0;">
  <a class="card-link" href="https://abhyudaymishr-oculon.hf.space" target="_blank" rel="noopener">
    <strong>Live Interactive App ↗</strong>
    <span>Hosted on Hugging Face Spaces (Gradio 5 + FastAPI)</span>
  </a>
  <a class="card-link" href="https://github.com/abhyudaymishr/bob-ai-hackathon-oculon" target="_blank" rel="noopener">
    <strong>GitHub Repository ↗</strong>
    <span>Full open-source codebase & pipeline (BoB AI Hackathon)</span>
  </a>
  <a class="card-link" href="https://pypi.org/project/oculon/" target="_blank" rel="noopener">
    <strong>PyPI Package: oculon ↗</strong>
    <span>pip-installable library with stdio & SSE MCP server</span>
  </a>
</div>

---

## 1. Multi-Dataset Coverage & Spatial Anchoring

The system ingests and standardizes four operational public safety datasets spanning several years of historical records:

1. **Missing Persons (112,516 records, 104,235 mapped)**: Mapped using normalized police station reporting-area proxies across 193 distinct reference jurisdictions.
2. **Unidentified Dead Bodies (13,334 records, 9,892 mapped)**: Mapped to 177 reference police station proxy centroids.
3. **Stolen Vehicles (114,753 records, 26,352 spatially resolved)**: Evaluated through dual spatial approximations: postal PIN code centroids and nearest Delhi Metro station units (210 reference nodes).
4. **Missing Mobiles (1,602 records)**: Analyzed for temporal incident trends (non-spatial, as source records lack physical event coordinates).

### Privacy by Design
A core engineering principle of Oculon is that public risk forecasting must never compromise individual privacy:
- **Zero Person-Level Identifiers**: All names, contact details, FIR numbers, and personal victim attributes are stripped at ingestion.
- **Proxy Coordinates Only**: Geospatial anchors represent official institutional entities (police stations, transit stations, postal centroids), strictly avoiding pinpoint recovery locations or residential addresses.

---

## 2. Methodology: Rolling-Origin Forward-Time Evaluation

Standard machine learning pipelines frequently evaluate spatial event prediction with random $80/20$ train/test splits. In temporal domains, this is catastrophic: training on events from October 2025 to predict events in March 2025 smuggles future temporal correlations into the model weights, fabricating artificially optimistic performance numbers.

Oculon implements a strict **Expanding-Window Rolling Origin (Forward-Time)** validation protocol:

$$
\mathcal{D}_{\text{train}}^{(t)} = \{ (x_\tau, y_\tau) \mid \tau < t \}, \qquad \mathcal{D}_{\text{eval}}^{(t)} = \{ (x_t, y_t) \}
$$

The latest $20\%$ of complete calendar months are reserved sequentially as test horizons. For each evaluated target month, model predictions are scored exclusively using information available prior to that month.

### Optimal Transport & Metric Suite
Rather than relying solely on classification accuracy, Oculon scores predictions across multiple complementary statistical dimensions:

- **Mean Wasserstein $W_1$ Distance**: Measures the earth-mover transport distance (in kilometers) required to move the predicted spatial probability mass to match the observed distribution of events:
  - **Missing Persons**: **1.22 km** mean Wasserstein distance across 27 evaluation months ($2024\text{--}06$ to $2026\text{--}08$).
  - **Stolen Vehicles (Metro Units)**: **1.68 km** mean Wasserstein distance.
  - **Unidentified Bodies**: **2.09 km** mean Wasserstein distance.
- **Mean Monthly Average Precision (mAP)**: Reaches **0.643** for vehicle thefts and **0.549** for unidentified bodies under strict forward testing.
- **Multiclass Brier Score Sum**: Assesses probability calibration ($0.0028$ for missing persons).

---

## 3. Architecture & Model Context Protocol (MCP) Integration

Oculon is architected as both an interactive human tool and an autonomous agent resource via the **Model Context Protocol (MCP)**:

```text
                  Agent Client (Claude Desktop / Cursor)
                                    │
                                    │  MCP Protocol (JSON-RPC 2.0 / SSE)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                          Oculon MCP Server                             │
│                                                                        │
│   • query_hotspots(dataset, month, top_k)                              │
│   • get_hotspot_map(map_type)                                          │
│   • get_model_metrics(dataset, evaluation_type)                        │
│   • list_datasets_and_months()                                         │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        FastAPI + Gradio Core                           │
│                                                                        │
│   • Interactive Leaflet / SVG Maps (Metro, Rail, Admin Boundaries)    │
│   • Spatiotemporal Feature Extraction & Rolling Inference              │
│   • Direct Fullscreen Browser Launch via Stdio Bridge                  │
└────────────────────────────────────────────────────────────────────────┘
```

### Native Agent Usability
By implementing the MCP specification, any AI assistant or developer agent can query hotspot probabilities directly inside their context:
```json
{
  "mcpServers": {
    "oculon_delhi_hotspots": {
      "url": "https://abhyudaymishr-oculon.hf.space/sse"
    }
  }
}
```
When invoked locally via `python -m oculon.mcp_server`, querying a map automatically launches the default system browser to display full-resolution SVG administrative boundaries, metro lines, and predicted density overlays without iframe limitations.

---

## 4. Key Takeaways

Oculon demonstrates that domain-informed scientific machine learning principles apply just as strongly to civil data as they do to physical systems:
1. **Respect Temporal Causality**: Random cross-validation on time-stamped human records creates benchmark illusion; forward-time rolling origins reveal true generalization.
2. **Measure Spatial Errors Spatially**: F1 scores collapse spatial proximity into binary hits and misses. Optimal transport ($W_1$) distance ensures that a near-miss is recognized as mathematically closer than an arbitrary spatial error.
3. **Bridge Models to Agent Ecosystems**: Exposing predictive systems via the Model Context Protocol transforms static dashboards into dynamic reasoning components for modern autonomous workflows.
