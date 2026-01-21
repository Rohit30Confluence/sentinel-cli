package cmd

import (
	"fmt"
	"os"

	"shield-cli/core/pkg/logstream"
)

func runMonitor() {
	// Default demo source
	logPath := "system_mock.log"

	// Allow override: shield monitor /path/to/log
	if len(os.Args) >= 3 {
		logPath = os.Args[2]
	}

	fmt.Println("shield-cli :: monitor")
	fmt.Println("source :", logPath)
	fmt.Println("--------------------------------")

	err := logstream.StreamFile(logPath)
	if err != nil {
		fmt.Println("monitor error:", err)
		os.Exit(1)
	}
}
