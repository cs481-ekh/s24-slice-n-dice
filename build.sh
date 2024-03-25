#!/bin/bash

# Determnine OS type for venv directories
binDir="bin" # Default for linux / macos
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    binDir="Scripts"
fi

install()
{
    python -m venv --system-site-packages .venv

    .venv/$binDir/pip3 install --ignore-installed -r requirements.txt
    .venv/$binDir/pip3 install --user ./GoVizzy/cube
    .venv/$binDir/pip3 install --user ./GoVizzy/gv_ui
}

launch()
{
    .venv/$binDir/jupyter lab --notebook-dir=GoVizzy
}

if [ -f .venv/$binDir/jupyter ]; then
    echo "GoVizzy already installed, to reinstall run ./clean.sh then ./build.sh"
else
    install
fi

# Determine if we are in Github Actions
if [ "$ACTIONS_ENVIRONMENT" = true ]; then
    echo "Running in Github action. Will not start JupyterLab."
    exit 0
fi

echo "Launching GoVizzy"
launch
