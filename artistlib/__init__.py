# -*- coding: UTF-8 -*-
"""The aRTist Python library is designed to remotely control and automate the radiographic simulation software aRTist.

.. include:: ./documentation.md
"""

__pdoc__ = {
    "console": False,
    "remote_access": False,
    "ArtistStart.check_running_win": False,
    "ArtistStart.check_running_Linux": False,
    "ArtistStart.find_file": False,
    "ArtistStart.read_json": False,
    "ArtistStart.write_json": False,
    "ArtistStart.load_artist_json": False,
    "ArtistStart.find_artist_installation": False,
    "ArtistStart.is_port_open": False,
    "ArtistStart.find_artist_manual": False,
    "ArtistStart.create_file": False,
    "ArtistStart.delete_file": False,
    "ArtistStart.run_artist": False,
    "ArtistStart.wait_to_start": False,
    "ArtistStart.find_and_start": False,
    "ArtistStart.start_artist": False,
    "ArtistStart.close_artist": False,
    "ArtistStart.get_pid_by_name": False,
    "ArtistStart.get_hwnds_by_pid": False,
    "ArtistStart.hide_window": False,
    "ArtistStart.show_window": False,
    "ArtistStart.hide_ui": False,
    "ArtistStart.show_ui": False,
}


from .wrapper.artist_send import ArtistSend
from .wrapper.artist_project import ArtistProject
from .wrapper.artist_setup import ArtistSetup
from .wrapper.artist_detector import ArtistDetector
from .wrapper.artist_source import ArtistSource


from .wrapper.start.artist_start import close_artist, start_artist, show_ui, hide_ui
from .wrapper.artistwrapper_all import ArtistAll
from .wrapper.modules import CT
from .wrapper.part import Project, Part, Detector, Source

from .wrapper.material2 import MaterialService, Material
from .junction import Junction


from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions


__all__ = [
    "Junction",
    "ArtistStart",
    "start_artist",
    "close_artist",
    "hide_ui",
    "show_ui",
    "ArtistSend",
    "ArtistProject",
    "ArtistSetup",
    "ArtistDetector",
    "ArtistSource",
    "MaterialService",
    "Material",
    "Material",
    "ArtistAll",
    "CT",
    "Project",
    "Part",
    "Detector",
    "Source",
]
