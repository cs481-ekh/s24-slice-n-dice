#!/bin/bash

# Determnine OS type for venv directories
binDir="bin" # Default for linux / macos
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    binDir="Scripts"
fi

python -m venv --system-site-packages .venv

.venv/$binDir/pip3 install --user ./GoVizzy/cube
.venv/$binDir/pip3 install --ignore-installed -r requirements.txt

if [ "$ACTIONS_ENVIRONMENT" = true ]; then
    echo "Running in Github action. Will not start JupyterLab."
    exit 0
fi

.venv/$binDir/jupyter lab --notebook-dir=GoVizzy
