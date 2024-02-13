#!/bin/bash
if [ ! -d .venv ]; then
    echo "No .venv found! Did you forget to run build.sh?"
    exit 1
fi

source .venv/bin/activate

python -m pytest