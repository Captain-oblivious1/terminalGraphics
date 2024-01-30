#!/bin/sh
me=$0
dir=$(dirname $me)
source $dir/python/bin/activate
TERM=xterm-1003 PYTHONPATH=$dir/src python $dir/src/main.py "$@"
deactivate
