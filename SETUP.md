# Setup & Agent Handover Guide

> **Target Audience:** Autonomous AI coding agents (Hermes, Claude Code, Codex, OpenCode, Cursor) and developers setting up the Fast Voice & Desktop Agent from scratch.

This guide provides an end-to-end environment blueprint, dependency resolution, execution contracts, and an unambiguous **Agent Handover Prompt** ensuring zero-friction setup and execution.

---

## 1. System Prerequisites

The agent interacts directly with OS-level audio devices, window managers, and X11/Wayland display layers.

### Linux / Debian / Ubuntu Packages
Ensure native display and audio libraries are present:

```bash
sudo apt update && sudo apt install -y \
  python3-dev \
  python3-venv \
  libasound2-dev \
  portaudio19-dev \
  libx11-dev \
  libxtst-dev \
  libpng-dev \
  alsa-utils \
  pulseaudio-utils \
  imagemagick \
  x11-utils
```

### Python Runtime
- **Recommended Version:** Python 3.10 to 3.12 (Tested on Python 3.11).

---

## 2. Virtual Environment & Python Dependencies

Create and isolate the Python environment:

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate
source venv/bin/activate

# 3. Upgrade pip tooling
pip install --upgrade pip setuptools wheel

# 4. Install Core Agent & OS Automation Dependencies
pip install sounddevice pyautogui python-xlib pillow

# 5. (Optional) High-Throughput Scrapling & Web Tooling
pip install "scrapling[all]"
playwright install chromium
```

---

## 3. Project Architecture & File Contracts

```
fast-voice-agent/
├── agent.py            # Core engine: sub-millisecond intent routing & OS dispatch table
├── test_runner.py      # Automated simulation suite executing real-user multi-turn flows
├── run_state.json      # Dynamic telemetry, cumulative run counter, and auto-stop state
├── logs/cron.log       # Background cron execution log
├── README.md           # Architecture overview
└── SETUP.md            # Zero-error agent handover & prerequisites
```

### Dispatch Table (`agent.py`)
Maps classified voice transcripts to OS subprocess calls:
- `open_browser` $\to$ Launches default web browser via `xdg-open`
- `open_terminal` $\to$ Opens terminal emulator via `x-terminal-emulator`
- `system_status` $\to$ Returns CPU, memory, uptime diagnostics
- `volume_mute_toggle` $\to$ Audio mute toggle via ALSA / PulseAudio
- `volume_up` $\to$ Increments audio output volume by 5%
- `take_screenshot` $\to$ Captures full screen via ImageMagick `import`
- `open_file_manager` $\to$ Opens user directory via `xdg-open`

---

## 4. Verification & Testing

### Run a Single Manual Voice Intent
```bash
./venv/bin/python agent.py "check system status"
```
*Expected Output:*
```text
Utterance: 'check system status'
Predicted Action: system_status (Confidence: 0.85, Latency: 0.007ms)
Result: Executed action: system_status (Report CPU, memory, and system load)
```

### Run an Automated User Simulation Pass
```bash
./venv/bin/python test_runner.py
```

### Configure Background Testing (Cron with Auto-Termination)
To run automated testing every 10 minutes that auto-terminates after 18 cycles:
```bash
crontab -l 2>/dev/null > /tmp/crontab.tmp || touch /tmp/crontab.tmp
echo "*/10 * * * * $(pwd)/venv/bin/python $(pwd)/test_runner.py >> $(pwd)/logs/cron.log 2>&1" >> /tmp/crontab.tmp
crontab /tmp/crontab.tmp
```

---

## 5. 🤖 Autonomous Agent Handover Prompt

Copy and paste the exact text block below to any new AI agent to continue development without prior context:

```text
[AGENT HANDOVER DIRECTIVE: FAST VOICE & DESKTOP AGENT]

You are tasked with maintaining, verifying, or extending the 'fast-voice-agent' repository.
Repository Root: $(git rev-parse --show-toplevel 2>/dev/null || pwd)

Context & Architecture:
- Purpose: Sub-millisecond on-device intent routing and native OS automation for voice agents.
- Core Engine: 'agent.py' contains FastIntentClassifier and COMMAND_REGISTRY.
- Decision Latency Contract: Must maintain single-pass routing under 0.05 ms without invoking autoregressive LLM text generation for fast-path actions.
- OS Control: Interacts with OS via subprocess calls (xdg-open, amixer, import, x-terminal-emulator) and PyAutoGUI.
- Simulation Suite: 'test_runner.py' executes randomized real-user scenario batches, validates predictions, and tracks lifecycle in 'run_state.json'.

Standard Operating Procedures:
1. Verify Environment:
   Ensure Python virtual environment is active and contains: sounddevice, pyautogui, pillow, python-xlib.
2. Run Smoke Test:
   Execute: python agent.py "open browser"
   Assert that latency is <0.05ms and status returns successful execution.
3. Check Cron & Telemetry:
   Read 'run_state.json' to inspect runs_completed, accuracy, and average latency.
4. Adding New Voice Commands:
   - Add new action to COMMAND_REGISTRY in 'agent.py' with explicit execution lambda.
   - Add keyword trigger patterns to FastIntentClassifier.rules.
   - Add verification test cases to TEST_SCENARIOS in 'test_runner.py'.
   - Test locally before committing.
5. Invariants:
   - Never introduce dependencies on external cloud APIs for fast-path routing.
   - Always catch execution exceptions gracefully in execute_command.
   - Preserve self-terminating behavior in test_runner.py.
```
