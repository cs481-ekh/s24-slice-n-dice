#!/bin/bash

python -m venv .venv

.venv/bin/pip3 install jupyter ipython_genutils ipyvolume pytest

.venv/bin/jupyter lab --notebook-dir=GoVizzy
