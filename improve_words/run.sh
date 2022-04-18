#!/bin/bash

# Prepare a virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set environment variables from the .env file
set -a
source .env
set +a

# Run the program
python3 fix.py

# Deactivate the virtual environment
deactivate

echo "Finished :) The words are in 'fixed_words.txt'"