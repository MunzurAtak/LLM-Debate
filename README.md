# LLM Debate Framework

A modular, research-grade multi-agent debate framework built in Python.
Developed as preparation for a bachelor thesis on ideologically conditioned LLM agents and structured inter-agent debate.

---

## Research Goal

This framework studies how LLM agents conditioned with distinct ideological or normative stances (e.g. utilitarian, libertarian, morality-focused, legality-focused) interact in structured debates, and how their behavior can be measured with reproducible metrics.

---

## Project Structure

```
LLM-Debate/
│
├── config/
│   ├── experiments/        # YAML files defining debate runs
│   └── personas/           # YAML files defining agent stances
│
├── src/
│   ├── llm/                # LLM backend abstraction layer
│   ├── agents/             # Agent abstraction and persona conditioning
│   ├── controller/         # Debate orchestration (Phase 3)
│   ├── evaluation/         # Metrics (Phase 5)
│   ├── logging/            # Structured JSON output (Phase 4)
│   └── utils/              # Config loader, seed control
│
├── experiments/            # Runnable experiment entry points
├── outputs/                # Generated debate logs (gitignored)
├── tests/                  # Unit tests
└── notebooks/              # Post-hoc analysis only
```

---

## Status

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | Foundation — LLM abstraction, config, seed control | Done |
| 2 | Agents — BaseAgent, PersonaAgent, persona YAML format | Done |
| 3 | Debate Controller — round management, turn orchestration | Pending |
| 4 | Logging — structured JSON debate logs | Pending |
| 5 | Evaluation — stance consistency, sentiment, lexical metrics | Pending |
| 6 | Experiments — end-to-end runnable experiment scripts | Pending |

---

## Setup

Requires Python 3.10+ and [Ollama](https://ollama.com) running locally.

```bash
# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Linux / macOS

# Install dependencies
pip install -r requirements.txt

# Pull a model via Ollama
ollama pull llama3.2:3b
```

---

## Architecture

### LLM Abstraction (`src/llm/`)

All model backends implement `BaseLLM`, which exposes a single `generate(messages, config) -> str` method.
Swapping from Llama to Qwen is a one-line change in the experiment config — no source code changes required.

Currently implemented:
- `OllamaLLM` — calls a local Ollama instance via its REST API. Works with AMD and NVIDIA GPUs.

### Agents (`src/agents/`)

An agent is an LLM paired with a persona. The persona is a YAML file that defines:
- `name` — human-readable label
- `stance` — short identifier used in logs and evaluation
- `system_prompt` — the full ideological conditioning prompt

`PersonaAgent` prepends the system prompt on every generation call, ensuring the conditioning is always active and cannot drift or be overridden by conversation history.

### Config System (`src/utils/`)

All experiment parameters (model, topic, rounds, agents, seed) are defined in YAML files under `config/experiments/`. No hardcoded values in source code.

### Reproducibility

Two-layer seed control:
- `set_seed(seed)` — sets Python and NumPy seeds for all non-LLM randomness
- `GenerationConfig.seed` — passed directly to Ollama for model-level reproducibility

---

## Personas

Personas are defined in `config/personas/`. Two are included:

| File | Stance | Framework |
|------|--------|-----------|
| `utilitarian.yaml` | Utilitarian | Evaluates arguments by aggregate welfare outcomes |
| `libertarian.yaml` | Libertarian | Evaluates arguments by individual rights and autonomy |

New stances for thesis experiments (morality, legality, left, right) are added by creating new YAML files — no code changes needed.

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| requests | >=2.31.0 | Ollama REST API calls |
| pyyaml | >=6.0.1 | Config and persona file loading |
| numpy | >=1.26.0 | Seed control and evaluation utilities |
