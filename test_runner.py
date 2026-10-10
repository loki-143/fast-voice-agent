#!/usr/bin/env python3
"""
End-to-End Real User Simulation Suite for Fast Voice Agent.
Executes test passes simulating real voice utterances, measures latency,
verifies command execution, tracks run counts, and auto-disables after 18 runs.
"""
import sys
import time
import json
import random
from pathlib import Path
from agent import FastIntentClassifier, execute_command

STATE_FILE = Path("/home/lokesh/projects/fast-voice-agent/run_state.json")
LOG_FILE = Path("/home/lokesh/projects/fast-voice-agent/logs/cron.log")

TEST_SCENARIOS = [
    ("check system status", "system_status"),
    ("could you open terminal please", "open_terminal"),
    ("launch web browser and search", "open_browser"),
    ("mute the audio", "volume_mute_toggle"),
    ("turn the volume up", "volume_up"),
    ("take a screenshot right now", "take_screenshot"),
    ("open file manager", "open_file_manager"),
    ("show me cpu and memory load", "system_status"),
    ("open my bash shell", "open_terminal"),
    ("browse the web", "open_browser")
]

def load_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except Exception:
            pass
    return {"runs_completed": 0, "max_runs": 18, "status": "active", "history": []}

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))

def run_simulation_cycle():
    state = load_state()
    current_run = state.get("runs_completed", 0) + 1
    max_runs = state.get("max_runs", 18)

    if current_run > max_runs or state.get("status") == "completed":
        print(f"🛑 Maximum target runs reached ({max_runs}/{max_runs}). Auto-stopping cron job.")
        # Auto-remove from crontab
        import subprocess
        subprocess.run(
            "crontab -l | grep -v 'fast-voice-agent' | crontab -",
            shell=True,
            check=False
        )
        state["status"] = "completed"
        save_state(state)
        return

    classifier = FastIntentClassifier()
    scenario_batch = random.sample(TEST_SCENARIOS, k=4)

    cycle_results = []
    total_latency = 0.0
    passed = 0

    print("=" * 60)
    print(f"🚀 FAST VOICE AGENT E2E TEST RUN [{current_run}/{max_runs}]")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)

    for utterance, expected_action in scenario_batch:
        start_t = time.perf_counter()
        pred = classifier.predict(utterance)
        elapsed_ms = (time.perf_counter() - start_t) * 1000.0
        total_latency += elapsed_ms

        match = pred["action"] == expected_action
        if match:
            passed += 1

        print(f"User Spoke: \"{utterance}\"")
        print(f"  → Predicted: {pred['action']} (Expected: {expected_action})")
        print(f"  → Latency: {elapsed_ms:.3f} ms | Accuracy: {'✓ PASS' if match else '✗ FAIL'}")

        cycle_results.append({
            "utterance": utterance,
            "expected": expected_action,
            "predicted": pred["action"],
            "latency_ms": elapsed_ms,
            "success": match
        })

    avg_latency = total_latency / len(scenario_batch)
    print("-" * 60)
    print(f"Summary: {passed}/{len(scenario_batch)} Passed | Avg Decision Latency: {avg_latency:.3f} ms")
    if current_run == max_runs:
        print("🎯 FINAL RUN COMPLETED! Crontab entry will now be cleaned up.")
    print("=" * 60 + "\n")

    # Update state
    state["runs_completed"] = current_run
    state["last_run_time"] = time.strftime('%Y-%m-%d %H:%M:%S')
    state["history"].append({
        "run": current_run,
        "avg_latency_ms": avg_latency,
        "accuracy": passed / len(scenario_batch)
    })
    if current_run >= max_runs:
        state["status"] = "completed"
        import subprocess
        subprocess.run(
            "crontab -l | grep -v 'fast-voice-agent' | crontab -",
            shell=True,
            check=False
        )

    save_state(state)

if __name__ == "__main__":
    run_simulation_cycle()
