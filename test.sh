#!/bin/bash
# Determnine OS type for venv directories
binDir="bin" # Default for linux / macos
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    binDir="Scripts"
fi

if [ ! -d .venv ]; then
    echo "No .venv found! Did you forget to run build.sh?"
    exit 1
fi

.venv/$binDir/python -m pytest
