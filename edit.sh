#!/bin/sh

source python/bin/activate
TERM=xterm-1003 python main.py "$@"
deactivate
