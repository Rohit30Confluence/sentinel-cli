package cmd

import (
	"fmt"
	"os"
)

// Execute is the single entrypoint called by main.go
func Execute() {
	if len(os.Args) < 2 {
		printUsage()
		os.Exit(1)
	}

	switch os.Args[1] {
	case "monitor":
		runMonitor()
	case "version":
		printVersion()
	default:
		fmt.Println("Unknown command:", os.Args[1])
		printUsage()
		os.Exit(1)
	}
}

func printUsage() {
	fmt.Println(`shield-cli

Usage:
  shield <command>

Available Commands:
  monitor     Start system log monitoring
  version     Show version information
`)
}

func printVersion() {
	fmt.Println("shield-cli v0.1.0 (execution-plane)")
}
