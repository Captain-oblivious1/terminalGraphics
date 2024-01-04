#!/bin/sh

source python/bin/activate
TERM=xterm-1003 PYTHONPATH=src python src/main.py "$@"
deactivate
