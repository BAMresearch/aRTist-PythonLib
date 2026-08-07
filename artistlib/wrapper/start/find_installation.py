import logging
import os
import time
from pathlib import Path

from .file_utility import write_json, find_file
from .process_helper import is_port_open
from ...junction import Junction

logger = logging.getLogger(__name__)


def find_artist_installation(jfile, path_std_list, name="aRTist.exe"):

    for path in path_std_list:
        if name in path and os.path.isfile(path):
            jdict = {"path": path}
            write_json(jfile, jdict)
            return path
        path_artist = find_file(name, path)
        if path_artist is not None and os.path.isfile(path_artist):
            jdict = {"path": path_artist}
            write_json(jfile, jdict)
            return path_artist

    logger.warning("Artist not found in standard installation path.")
    return None


def find_artist_manual(name, jfile, port=3658):
    logger.info("Open Artist and enable Remote Access")
    timeout = 100
    i = 0
    while True:
        if is_port_open("localhost", port):
            logger.info("The port was opened.")
            break
        time.sleep(1)
        if i >= timeout:
            raise Exception("Artist or the remote Access was not started, timeout")
        i = i + 1
    jct = Junction()
    path = jct.send("pwd").strip()
    time.sleep(1)
    logger.debug(path)
    path_artist = Path(path)
    path_artist_file = find_file(name, path_artist)
    if path_artist_file is not None and os.path.isfile(path_artist_file):
        jdict = {"path": path_artist_file}
        write_json(jfile, jdict)
        return path_artist_file
    raise Exception(
        "Something went wrong, ther was no way to find an installation of Artist. Make sure Artist is installed and specify the correct path"
    )
