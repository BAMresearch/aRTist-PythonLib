#!/bin/bash
# Builds the HTML documentation using pdoc3
# and moves it to the "docs" folder (instead of docs/artistlib).

find docs -mindepth 1   -path "docs/templates" -prune -o   \( ! -name "artistlib.png" ! -name "favicon.ico" ! -name "artistlib.pdf" \)   -exec rm -rf {} +
pdoc --force --html --template-dir "docs/templates" -o "docs/" artistlib
cp -R docs/artistlib/* docs/
rm -R docs/artistlib
###pdoc --logo "artistlib.png" --template-dir "docs/templates" -o "docs/" artistlib
###rm -R docs/artistlib