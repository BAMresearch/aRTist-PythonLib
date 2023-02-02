#!/bin/bash
# Builds the documentation as a PDF file,
# using pdoc3 to create a complete Markdown file,
# which is then passed to pandoc to create a LaTeX
# file and a PDF using XeLaTeX.
pdoc --force --pdf artistlib > docs/artistlib.md
pandoc --metadata=title:"aRTsit PythonLib Documentation" --from=markdown+abbreviations+tex_math_single_backslash --pdf-engine=xelatex --variable=mainfont:"DejaVu Sans" --toc --toc-depth=1 --output=docs/artistlib.pdf docs/artistlib.md
rm docs/artistlib.md