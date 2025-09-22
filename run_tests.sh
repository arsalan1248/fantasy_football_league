#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Optional: clear old __pycache__ and .pytest_cache
echo "Cleaning caches..."
find . -type d -name "__pycache__" -exec rm -rf {} +
rm -rf .pytest_cache

# List of Django apps
apps=("core" "users" "league" "transactions")

# Run tests app-wise
for app in "${apps[@]}"
do
    echo ""
    echo "=============================="
    echo "Running tests for app: $app"
    echo "=============================="
    echo ""

    # Run pytest for specific app with verbose output
    pytest $app 
done

echo ""
echo "All tests completed!"
