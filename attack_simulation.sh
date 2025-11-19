#!/bin/bash

# This script simulates Falco alerts by writing JSON logs to alerts.log
# Usage: ./attack_simulation.sh

LOG_FILE="alerts.log"

echo "--- Starting Attack Simulation ---"
echo "Target Log File: $LOG_FILE"

# Scenario 1: High Severity - Shell in Container
echo "[1] Simulating: Terminal Shell in Container (High Severity)..."
echo '{"rule":"Terminal shell in container","priority":"Notice","output":"A shell was spawned in a container with an attached terminal (user=root k8s.pod.name=nginx)","time":"2025-11-19T14:00:00Z"}' >> $LOG_FILE
sleep 2

# Scenario 2: Critical Severity - Container Escape
echo "[2] Simulating: Container Escape Attempt (Critical Severity)..."
echo '{"rule":"Write below binary dir","priority":"Critical","output":"File opened for writing (user=root command=cp /bin/sh /host/etc/cron.d/backdoor)","time":"2025-11-19T14:45:00Z"}' >> $LOG_FILE

echo "--- Simulation Complete ---"
echo "Check the Triage Console for AI Analysis."
