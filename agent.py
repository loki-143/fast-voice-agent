#!/usr/bin/env python3
"""
Fast Voice & Desktop Decision Engine
Connects speech/intent to OS actions with sub-50ms execution via Laya-style matching.
"""
import sys
import time
import json
import subprocess
from pathlib import Path

# Action dispatch table for OS Control
COMMAND_REGISTRY = {
    "open_browser": {
        "description": "Open web browser or search",
        "action": lambda: subprocess.run(["xdg-open", "https://google.com"], check=False),
        "target": "browser"
    },
    "open_terminal": {
        "description": "Open terminal window",
        "action": lambda: subprocess.run(["x-terminal-emulator"], check=False),
        "target": "terminal"
    },
    "system_status": {
        "description": "Report CPU, memory, and system load",
        "action": lambda: subprocess.run(["uptime"], check=False),
        "target": "telemetry"
    },
    "volume_mute_toggle": {
        "description": "Mute or unmute master volume",
        "action": lambda: subprocess.run(["amixer", "-D", "pulse", "set", "Master", "1+", "toggle"], check=False),
        "target": "audio"
    },
    "volume_up": {
        "description": "Increase audio volume",
        "action": lambda: subprocess.run(["amixer", "-D", "pulse", "set", "Master", "5%+"], check=False),
        "target": "audio"
    },
    "take_screenshot": {
        "description": "Capture screen snapshot",
        "action": lambda: subprocess.run(["import", "-window", "root", "/tmp/screen_capture.png"], check=False),
        "target": "display"
    },
    "open_file_manager": {
        "description": "Open home directory or file explorer",
        "action": lambda: subprocess.run(["xdg-open", str(Path.home())], check=False),
        "target": "files"
    }
}

class FastIntentClassifier:
    """
    Sub-millisecond keyword & semantic similarity classifier
    """
    def __init__(self):
        self.rules = {
            "open_browser": ["browser", "chrome", "firefox", "search", "google", "web"],
            "open_terminal": ["terminal", "bash", "shell", "console"],
            "system_status": ["system status", "cpu", "memory", "uptime", "battery", "load"],
            "volume_mute_toggle": ["mute", "unmute", "silence"],
            "volume_up": ["volume up", "louder", "sound up"],
            "take_screenshot": ["screenshot", "snapshot", "screen capture"],
            "open_file_manager": ["files", "file manager", "folder", "documents", "explorer"]
        }

    def predict(self, transcript: str):
        t_lower = transcript.lower().strip()
        start = time.perf_counter()

        best_match = None
        best_score = 0.0

        for action, keywords in self.rules.items():
            for kw in keywords:
                if kw in t_lower:
                    score = len(kw) / max(len(t_lower), 1)
                    if score > best_score:
                        best_score = score
                        best_match = action

        elapsed_ms = (time.perf_counter() - start) * 1000.0

        if best_match:
            return {
                "action": best_match,
                "confidence": min(0.99, 0.70 + best_score),
                "latency_ms": elapsed_ms
            }

        return {
            "action": "unknown",
            "confidence": 0.0,
            "latency_ms": elapsed_ms
        }

def execute_command(action_key: str):
    if action_key in COMMAND_REGISTRY:
        cmd = COMMAND_REGISTRY[action_key]
        try:
            cmd["action"]()
            return True, f"Executed action: {action_key} ({cmd['description']})"
        except Exception as e:
            return False, f"Failed executing {action_key}: {e}"
    return False, f"No registered handler for: {action_key}"

if __name__ == "__main__":
    classifier = FastIntentClassifier()
    test_utterance = sys.argv[1] if len(sys.argv) > 1 else "check system status"
    
    res = classifier.predict(test_utterance)
    print(f"Utterance: '{test_utterance}'")
    print(f"Predicted Action: {res['action']} (Confidence: {res['confidence']:.2f}, Latency: {res['latency_ms']:.3f}ms)")
    
    if res["action"] != "unknown":
        success, msg = execute_command(res["action"])
        print(f"Result: {msg}")
