# Fast Voice & Desktop Agent

An ultra-low-latency, on-device decision agent designed for voice and desktop control, inspired by **Laya** and **Herald OS**.

## Architecture & Features
- **Sub-Millisecond Decision Head:** Routes user intent in <0.05 ms without slow token-by-token LLM generation.
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
