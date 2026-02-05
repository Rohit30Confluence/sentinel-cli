package logstream

import (
	"encoding/json"
	"errors"
	"os"
	"time"

	"github.com/hpcloud/tail"
)

// Event is the canonical schema for all streamed data.
// Agents and downstream tools depend on this. Do not break casually.
type Event struct {
	Timestamp string `json:"timestamp"`
	Source    string `json:"source"`
	Message   string `json:"message"`
	Severity  string `json:"severity"`
}

// StreamFile tails a log file and emits structured JSON events to stdout.
// It has zero awareness of CLI flags, agents, or actions.
func StreamFile(path string) error {
	if path == "" {
		return errors.New("log path cannot be empty")
	}

	if _, err := os.Stat(path); err != nil {
		return err
	}

	t, err := tail.TailFile(path, tail.Config{
		Follow: true,
		ReOpen: true,
		Poll:   true,
	})
	if err != nil {
		return err
	}

	encoder := json.NewEncoder(os.Stdout)

	for line := range t.Lines {
		event := Event{
			Timestamp: time.Now().UTC().Format(time.RFC3339),
			Source:    path,
			Message:   line.Text,
			Severity:  "INFO",
		}

		// Stream. No buffering. No retries. No interpretation.
		if err := encoder.Encode(event); err != nil {
			return err
		}
	}

	return nil
}
