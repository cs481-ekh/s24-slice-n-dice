#!/bin/bash
python -m venv --system-site-packages .venv

.venv/bin/pip3 install jupyter ipython_genutils ipyvolume pytest ase
.venv/bin/pip3 install --user ./GoVizzy/cube

if [ "$ACTIONS_ENVIRONMENT" = true ]; then
    echo "Running in Github action. Will not start JupyterLab."
    exit 0
fi

.venv/bin/jupyter lab --notebook-dir=GoVizzy
