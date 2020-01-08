#!/usr/bin/env bash

echo "Run for $1"
python3 experiment.py -g -rc -d "$1" -p $1
