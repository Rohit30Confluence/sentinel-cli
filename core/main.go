package main

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/hpcloud/tail"
)

// LogEntry is the contract between the Execution Plane and the Agentic Brain.
// This schema MUST remain stable. Agents depend on it.
type LogEntry struct {
	Timestamp string `json:"timestamp"`
	Source    string `json:"source"`
	Message   string `json:"message"`
	Severity  string `json:"severity"`
}

// bootstrap ensures demo readiness without touching real system logs.
// In production, this disappears.
func bootstrapMockLog(path string) {
	if _, err := os.Stat(path); os.IsNotExist(err) {
		err := os.WriteFile(path, []byte(""), 0644)
		if err != nil {
			log.Fatalf("failed to create mock log file: %v", err)
		}
	}
}

func main() {
	log.SetFlags(log.LstdFlags | log.Lshortfile)

	fmt.Println("Sentinel-CLI :: Execution Plane online")

	// Demo-first, safety-first.
	// Replace with /var/log/auth.log or journald reader in production.
	logPath := "system_mock.log"
	bootstrapMockLog(logPath)

	tailer, err := tail.TailFile(logPath, tail.Config{
		Follow: true,
		ReOpen: true,
		Poll:   true,
	})
	if err != nil {
		log.Fatalf("failed to start log tailer: %v", err)
	}

	encoder := json.NewEncoder(os.Stdout)

	for line := range tailer.Lines {
		entry := LogEntry{
			Timestamp: time.Now().UTC().Format(time.RFC3339),
			Source:    "auth-log",
			Message:   line.Text,
			Severity:  "INFO",
		}

		// Execution Plane does not interpret.
		// It observes and reports. Period.
		if err := encoder.Encode(entry); err != nil {
			log.Printf("json encode error: %v", err)
		}
	}
}
