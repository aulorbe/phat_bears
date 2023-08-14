#!/bin/bash

# This is a Bash script to create the Weaviate schema & data objs needed for this demo.

PYTHON_EXECUTABLE="python3"

# Prompt the user for API Key
read -p "Please enter your API Key: " OPENAI_APIKEY

# Set the API Key as an environment variable
export OPENAI_APIKEY


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

# Install dependencies from requirements.txt
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if pip install was successful
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies."
    exit 1
fi

# Initialize progress variables
total_scripts=${#PYTHON_FILES[@]}
current_script=1

# Loop through each Python script and run it
for PYTHON_SCRIPT in "${PYTHON_FILES[@]}"; do
    # Check if the Python script file exists
    if [ ! -f "$PYTHON_SCRIPT" ]; then
        echo "Error: Python script file '$PYTHON_SCRIPT' not found."
        exit 1
    fi

    # Display progress bar
    echo -n -e "\n\n Running script $current_script of $total_scripts, $PYTHON_SCRIPT: \n["
    ( $PYTHON_EXECUTABLE "$PYTHON_SCRIPT" ) &

    # Print script completion message
    wait $!
    echo -en "\r["
    for ((i = 0; i < 20; i++)); do
        echo -en "="
    done
    echo -en "]"

    # Increment current script count
    current_script=$((current_script + 1))
done

# Clear progress bar
echo -e "\r\c"

# Exit successfully
exit 0
