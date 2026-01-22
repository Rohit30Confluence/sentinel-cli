from collections import deque
from datetime import datetime, timedelta

class BruteForceAnalyzer:
    """
    Detects brute-force authentication attempts using
    sliding-window behavioral analysis.
    """

    def __init__(self, threshold=5, window_seconds=60):
        self.threshold = threshold
        self.window_seconds = window_seconds
        self.events = deque()

    def _prune(self, now):
        cutoff = now - timedelta(seconds=self.window_seconds)
        while self.events and self.events[0] < cutoff:
            self.events.popleft()

    def analyze(self, event):
        """
        Returns:
          None              -> not relevant
          dict(decision)    -> WARNING or CRITICAL
        """
        msg = event.get("message", "").lower()
        now = datetime.utcnow()

        if not any(k in msg for k in [
            "failed password",
            "invalid user",
            "authentication failure",
        ]):
            return None

        self.events.append(now)
        self._prune(now)

        count = len(self.events)

        if count >= self.threshold:
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
