#!/bin/bash
if [ ! -d .venv ]; then
    echo "No .venv found! Did you forget to run build.sh?"
    exit 1
fi

.venv/bin/python -m pytest
