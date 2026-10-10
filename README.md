# Fast Voice & Desktop Agent

An ultra-low-latency, on-device decision agent designed for voice and desktop control, inspired by **Laya** and **Herald OS**.

## Architecture & Features
- **Laya Integration:** Powered by **Laya v0.4.2** (`laya.Router`), performing typed single-forward-pass System 1 decisions over typed criteria questions without slow token-by-token LLM generation.
- **Dual-Path Routing:**
  - `laya-neural`: Multilingual non-autoregressive decision head across 100+ languages.
  - `laya-fastpath`: Sub-millisecond instant keyword decision table (<0.01ms).
- **OS Control & Dispatch:** Native bindings for browser, terminal, system telemetry, volume/audio toggles, screenshot capture, and file explorer.
- **Automated Real-User E2E Suite:** Multi-turn simulation runner with self-terminating bounded testing.

## Files
- `agent.py`: Fast intent classifier and action dispatch registry.
- `test_runner.py`: End-to-end simulated user testing suite.
- `run_state.json`: Lifecycle and telemetry logs.

## Quick Start
```bash
/home/lokesh/venv_ctc/bin/python agent.py "check system status"
```
