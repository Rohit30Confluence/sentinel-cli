#!/usr/bin/env bash

# --------------------------------------------------
# Sentinel-CLI :: Attack Simulator
# Purpose:
#   Generate controlled authentication-failure logs
#   for live demos and CI testing.
#
# This script NEVER touches real system logs.
# --------------------------------------------------

LOG_FILE="system_mock.log"
ATTACKER_IP=${1:-"10.0.0.5"}
ATTEMPTS=${2:-6}
DELAY=${3:-0.5}

if [ ! -f "$LOG_FILE" ]; then
  echo "[ERROR] $LOG_FILE not found. Run the Execution Plane first."
  exit 1
fi

echo "[SIMULATOR] Starting brute-force simulation"
echo "[SIMULATOR] Target log : $LOG_FILE"
echo "[SIMULATOR] Attacker IP: $ATTACKER_IP"
echo "[SIMULATOR] Attempts   : $ATTEMPTS"
echo "[SIMULATOR] Delay (s)  : $DELAY"
echo "----------------------------------------"

for ((i=1; i<=ATTEMPTS; i++)); do
  echo "Failed password for root from $ATTACKER_IP port 22 ssh2" >> "$LOG_FILE"
  echo "[SIMULATOR] Attempt $i injected"
  sleep "$DELAY"
done

echo "----------------------------------------"
echo "[SIMULATOR] Simulation complete"
