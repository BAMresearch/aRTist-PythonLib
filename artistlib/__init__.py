# -*- coding: UTF-8 -*-
"""The aRTist Python library is intended to remote control and automate the radiographic simulator aRTist.

.. include:: ./documentation.md
"""

__pdoc__ = {'console': False, 'remote_access': False}

from ._version import get_versions as __get_versions
from .remote_connection import Junction
from .api import API
from .common_types import SAVEMODES, SOURCETYPES


__version__ = __get_versions()['version']

