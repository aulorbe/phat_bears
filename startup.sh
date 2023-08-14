#!/bin/bash

# This is a Bash script to create the Weaviate schema & data objs needed for this demo.

PYTHON_EXECUTABLE="python3"


# Check if the Python executable is defined
if [ -z "$PYTHON_EXECUTABLE" ]; then
    PYTHON_EXECUTABLE="python" # Default to 'python' if not specified
fi

# List of hardcoded Python file names
PYTHON_FILES=(
    "phat_bears/gen_schema.py"
    "phat_bears/web_scraper.py"
    "phat_bears/ingestion.py"
)

  # Loop through each Python script and run it
for PYTHON_SCRIPT in "${PYTHON_FILES[@]}"; do
    # Check if the Python script file exists
    if [ ! -f "$PYTHON_SCRIPT" ]; then
        echo "Error: Python script file '$PYTHON_SCRIPT' not found."
        exit 1
    fi

    # Run the Python script
    echo "Running $PYTHON_SCRIPT ..."
    $PYTHON_EXECUTABLE "$PYTHON_SCRIPT"
    echo "$PYTHON_SCRIPT finished with exit code: $?"
done

# Exit successfully
exit 0