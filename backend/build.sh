#!/usr/bin/env bash
# Exit on error
set -e

# Install python dependencies
pip install -r requirements.txt

# Download required spaCy models
python -m spacy download en_core_web_sm
