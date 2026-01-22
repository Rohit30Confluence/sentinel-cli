import sys
import json
from collections import deque
from datetime import datetime, timedelta
from analyzers.bruteforce import BruteForceAnalyzer


# ---- Agent Configuration ----
WINDOW_SECONDS = 60
BRUTE_FORCE_THRESHOLD = 5

class SentinelAgent:
    """
    This agent reasons over event streams.
    It does NOT execute system commands yet.
    That boundary is intentional and non-negotiable.
    """

    def __init__(self):
        self.bruteforce = BruteForceAnalyzer()
        self.event_window = deque()
        self.start_time = datetime.utcnow()
        self._announce()
        

    def _announce(self):
        print("Sentinel Agent :: Intelligence Plane online", flush=True)
        print(f"Policy :: window={WINDOW_SECONDS}s threshold={BRUTE_FORCE_THRESHOLD}", flush=True)

    def _prune_window(self, now):
        cutoff = now - timedelta(seconds=WINDOW_SECONDS)
        while self.event_window and self.event_window[0] < cutoff:
            self.event_window.popleft()

    def analyze(self, event):
        """
        Returns a decision dict.
        Decisions are explicit. No vibes, no guesses.
        """
        msg = event.get("message", "").lower()
        now = datetime.utcnow()

        suspicious = any(
            keyword in msg
            for keyword in ["failed password", "invalid user", "authentication failure"]
        )

        if suspicious:
            self.event_window.append(now)
            self._prune_window(now)

            count = len(self.event_window)

            if count >= BRUTE_FORCE_THRESHOLD:
                return {
                    "verdict": "CRITICAL",
                    "reason": "probable_bruteforce",
                    "evidence_count": count,
                }

            return {
                "verdict": "WARNING",
                "reason": "suspicious_auth_activity",
                "evidence_count": count,
            }

        return {
            "verdict": "CLEAR",
            "reason": "benign_activity",
            "evidence_count": 0,
        }

    def emit(self, event, decision):
        """
        Single-line output.
        Humans read it. Machines parse it.
        """
        output = {
            "timestamp": event.get("timestamp"),
            "source": event.get("source"),
            "verdict": decision["verdict"],
            "reason": decision["reason"],
            "window_hits": decision["evidence_count"],
            "raw": event.get("message"),
        }
        print(json.dumps(output), flush=True)

    def run(self):
        for line in sys.stdin:
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue

            decision = self.analyze(event)
            if decision:
            self.emit(event, decision)

            # Future hook: Action Plane
            if decision["verdict"] == "CRITICAL":
                self.handle_critical(event, decision)

    def handle_critical(self, event, decision):
        """
        Placeholder for Action Plane integration.
        Today: log intent.
        Tomorrow: firewall, isolate, snapshot.
        """
        print(
            f"INTENT :: isolate_source :: reason={decision['reason']}",
            file=sys.stderr,
            flush=True,
        )


if __name__ == "__main__":
    agent = SentinelAgent()
    agent.run()
