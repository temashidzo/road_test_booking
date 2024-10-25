#!/bin/bash

# Maximum allowed number of vscode-server processes
MAX_ALLOWED_PROCESSES=10

echo "Searching for vscode-server processes..."

# Get the list of PIDs for vscode-server processes
VSCODE_PIDS=$(pgrep -f 'vscode-server/bin/.*node' || echo "No processes found.")

# If no processes are found, exit the script
if [ "$VSCODE_PIDS" == "No processes found." ]; then
    echo "No vscode-server processes detected."
    exit 0
fi

# Count the number of processes
VSCODE_PROCESSES_COUNT=$(echo "$VSCODE_PIDS" | wc -l)

echo "$VSCODE_PROCESSES_COUNT vscode-server processes found."

# If the number of processes exceeds the allowed maximum, terminate them
if [ "$VSCODE_PROCESSES_COUNT" -gt "$MAX_ALLOWED_PROCESSES" ]; then
    echo "The number of processes exceeds the allowed limit of $MAX_ALLOWED_PROCESSES."
    # Kill the excess processes
    TO_KILL=$(($VSCODE_PROCESSES_COUNT - $MAX_ALLOWED_PROCESSES))
    echo "Terminating $TO_KILL excess processes..."
    echo "$VSCODE_PIDS" | head -n "$TO_KILL" | xargs -r kill
    echo "Excess vscode-server processes have been terminated."
else
    echo "The number of vscode-server processes is within the allowed limit."
fi
