import sys
import json
import yaml
from pathlib import Path

from analyzers.bruteforce import BruteForceAnalyzer


class SentinelBrain:
    """
    Orchestrates analyzers under explicit policy control.
    This file must stay boring and predictable.
    """

    def __init__(self, policy_path="agents/policies.yaml"):
        self.policies = self._load_policies(policy_path)
        self.analyzers = self._init_analyzers()
        self._announce()

    def _load_policies(self, path):
        policy_file = Path(path)
        if not policy_file.exists():
            raise RuntimeError(f"Policy file not found: {path}")

        with open(policy_file, "r") as f:
            return yaml.safe_load(f)

    def _init_analyzers(self):
        analyzers = {}

        for policy in self.policies.get("policies", []):
            if not policy.get("enabled", False):
                continue

            if policy["id"] == "AUTH_BRUTE_FORCE":
                threshold = policy["threshold"]["count"]
                window = policy["threshold"]["within_seconds"]

                analyzers["AUTH_BRUTE_FORCE"] = BruteForceAnalyzer(
                    threshold=threshold,
                    window_seconds=window,
                )

        return analyzers

    def _announce(self):
        print("Sentinel Agent :: Intelligence Plane online", flush=True)
        print(
            f"Loaded policies: {list(self.analyzers.keys())}",
            flush=True,
        )

    def emit(self, event, policy_id, decision):
        output = {
            "timestamp": event.get("timestamp"),
            "source": event.get("source"),
            "policy": policy_id,
            "verdict": decision["verdict"],
            "reason": decision["reason"],
            "evidence_count": decision["evidence_count"],
            "raw": event.get("message"),
        }
        print(json.dumps(output), flush=True)

    def emit_intent(self, policy_id, verdict):
        intent = {
            "intent": "action_request",
            "policy": policy_id,
            "verdict": verdict,
        }
        print(json.dumps(intent), file=sys.stderr, flush=True)

    def run(self):
        for line in sys.stdin:
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue

            for policy_id, analyzer in self.analyzers.items():
                decision = analyzer.analyze(event)
                if not decision:
                    continue

                self.emit(event, policy_id, decision)

                if decision["verdict"] == "CRITICAL":
                    self.emit_intent(policy_id, "CRITICAL")


if __name__ == "__main__":
    brain = SentinelBrain()
    brain.run()
