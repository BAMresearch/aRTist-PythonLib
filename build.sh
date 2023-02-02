#!/bin/bash
rm -R dist
rm -R artistlib.egg-info
python -m build

# twine upload dist/*