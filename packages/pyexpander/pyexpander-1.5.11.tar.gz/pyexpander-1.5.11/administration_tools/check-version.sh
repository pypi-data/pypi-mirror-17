#!/bin/sh

cd ..

FILES="`ls [A-Za-z]*.py` setup.py"

grep "\"[^\"]\+\" \+\(#VERSION#\)" $FILES | column -t -s := | column -t
