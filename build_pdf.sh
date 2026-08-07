#!/bin/bash
# Builds the documentation as a PDF file,
# using pdoc3 to create a complete Markdown file,
# which is then passed to pandoc to create a LaTeX
# file and a PDF using XeLaTeX.
export PYTHONUTF8="1"
export PYTHONIOENCODING="utf-8"
pdoc --force --pdf --template-dir "docs/templates" artistlib > docs/artistlib.md
pandoc --metadata=title:"aRTsit PythonLib Documentation" --from=markdown+abbreviations+tex_math_single_backslash --pdf-engine=xelatex --variable=mainfont:"Times New Roman" --toc --toc-depth=1 --output=docs/artistlib.pdf docs/artistlib.md
rm docs/artistlib.md