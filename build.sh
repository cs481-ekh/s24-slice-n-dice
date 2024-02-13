#!/bin/bash
python -m venv .venv

.venv/bin/pip3 install jupyter ipython_genutils ipyvolume pytest

if [ "$ACTIONS_ENVIRONMENT" = true ]; then
    echo "Running in Github action. Will not start JupyterLab."
    exit 0
fi

.venv/bin/jupyter lab --notebook-dir=GoVizzy
