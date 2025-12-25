#!/bin/bash

while :
do
    python3 scrapetwitterfollowers.py
    exit_code=$?

    # Check the exit code
    if [ $exit_code -eq 1 ]; then
        echo "All followers scraped."
        break
    elif [ $exit_code -eq 0 ]; then
        echo "Script completed successfully."
        break
    else
        echo "An error occurred. Exit code: $exit_code"
        sleep 10
    fi
done
