**Hint:** This project is in its early stages and may change significantly over time.

Getting started
===============

Requirements
------------
A **Python 3** environment (Python 3.8 or higher) is required. The following Python packages are required as well. They usually come with a Python environment, or can be installed there easily:

* none so far.


Installation
------------

If you want to **install** the package in your Python environment, you can use [pip]. For example, you can run the following command to make the toolbox available:

	pip install artistlib

[pip]: https://pip.pypa.io

To use the package **without installation**, you need to download the package manually. You have the following three options:

* Download the package [from PyPi]. You will get a zipped file called `artistlib-X.X.X.tar.gz` (where X.X.X is the current version number). Open or unpack this file to get to its contents.
* Download the repository [from GitHub]: press the *clone* button to download a ZIP file. Unpack it or open it to see its contents.
* You can also clone the repository from GitHub via the terminal:

	`git clone https://github.com/BAMresearch/aRTist-PythonLib.git`

From any of these three options, you will get the complete package source code. It contains a folder called `artistlib`. If you want to use the library from your Python scripts without installing it, you need to copy the folder `artistlib` to the location of your Python scripts to make the package available.


[from GitHub]: https://github.com/BAMresearch/aRTist-PythonLib
[from PyPi]: https://pypi.org/project/artistlib/

Usage
-----

Please make sure that aRTist is running and waiting for remote connection (menu: Tools>Enable remote access).

The following example code shows the basic usage:

```python
.. include:: ../example_artistlib.py
```

About
=====

The aRTist library was developed for utilize the Python scripting of the radiographic simulator [aRTist].

The software is released under the **Apache 2.0 license,** its source code is available [on GitHub].

[aRTist]: https://artist.bam.de
[on GitHub]: https://github.com/BAMresearch/aRTist-PythonLib

Contributors
------------
The following people contributed to code and documentation of the package:

* Alexander Funke
* David Schumacher
* Carsten Bellon
* David Plotzki
* David Denkler