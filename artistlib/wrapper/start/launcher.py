import os
import subprocess
import platform
import socket
from pathlib import Path
from .file_utility import read_json, find_file, create_file, delete_file, write_json, find_file_del
from .find_installation import find_artist_installation, find_artist_manual
from .process_helper import (
    wait_to_start,
    is_port_open,
    check_running_Linux,
    check_running_win,
)
from .ui import hide_ui, show_ui
from ...junction import Junction
from ..artist_send import ArtistSend


def load_artist_json(jfile):
    if os.path.isfile(jfile):
        data = read_json(jfile)
        if data and "path" in data:
            path_std = data["path"]
            if os.path.exists(path_std):
                return path_std
    return None


def run_artist(cmd_str, tcl_file):
    if not os.path.isfile(cmd_str):
        raise FileNotFoundError(cmd_str)

    if not os.path.isfile(tcl_file):
        raise FileNotFoundError(tcl_file)
    # self.create_TCL_file(current_folder_file,"::RemoteControl::Enable")
    proc = subprocess.Popen([cmd_str, tcl_file])
    return proc


def find_and_start(
    path_specific_version,
    jfile,
    path_std_list,
    tcl_file,
    tcl_file_content,
    flag_path,
    name,
):
    current_folder = Path(__file__).absolute().parent
    path_artist = None
    if path_specific_version is None:
        path_artist = load_artist_json(jfile)

    if path_artist is None:
        path_artist = find_artist_installation(jfile, path_std_list, name)

    if path_artist is not None:
        delete_file(flag_path)
        #clean up if an older try failed
        find_file_del(current_folder,"artist_started",".txt")
        find_file_del(current_folder,"start_remote_artist",".tcl")
        create_file(tcl_file, tcl_file_content)
        run_artist(path_artist, tcl_file)
        wait_to_start(flag_path)
        delete_file(flag_path)
        delete_file(tcl_file)
    else:
        path_artist = find_artist_manual(name, jfile=jfile)
    return path_artist


def launch_artist(
    path_specific_version=None, start_UI=True, port=3658, multiple_starts=False
):
    system = platform.system()
    path_artist = None

    python_pid = os.getpid()
    current_folder = Path(__file__).absolute().parent
    tcl_file = (current_folder / f"start_remote_artist{python_pid}.tcl").as_posix()
    flag_path = (current_folder / f"artist_started{python_pid}.txt").as_posix()
    jfile = "artist_installation_place.json"

    tcl_file_content = f'''::RemoteControl::EnablePipe; ::RemoteControl::BindServer {port} ; set f [open "{flag_path}" w+] ; puts $f "READY" ; close $f'''

    if system == "Windows":
        name = "aRTist.exe"
        if path_specific_version is not None:
            if not Path(path_specific_version).is_file():
                raise FileNotFoundError(path_specific_version)
            path_std_list = [path_specific_version]
        else:
            path_std_list = ["C:/Program Files/BAM/aRTist 2.12/bin64/aRTist.exe"]

        if not multiple_starts:
            if not check_running_win():
                path_artist = find_and_start(
                    path_specific_version,
                    jfile,
                    path_std_list,
                    tcl_file,
                    tcl_file_content,
                    flag_path,
                    name,
                )
        else:
            if not is_port_open(host="localhost", port=port):
                path_artist = find_and_start(
                    path_specific_version,
                    jfile,
                    path_std_list,
                    tcl_file,
                    tcl_file_content,
                    flag_path,
                    name,
                )

        if not start_UI:
            hide_ui(name)

    elif system == "Linux":
        name = "aRTist"
        if path_specific_version is not None:
            path_std_list = [path_specific_version]
        else:
            path_std_list = ["/usr/bin"]
        if not check_running_Linux():
            path_artist = find_and_start(
                path_specific_version,
                jfile,
                path_std_list,
                tcl_file,
                tcl_file_content,
                flag_path,
                name,
            )

    elif system == "Darwin":
        return None
    return path_artist


def close_artist(port=3658):
    # if self.path_current_artist is not None:
    if is_port_open("localhost", port):
        jct = Junction(port=port)
        an = jct.send("aRTist::shutdown  -force")
        jct.disconnect()
    else:
        name = "aRTist.exe"
        os.system(f"taskkill /f /im {name}")  # sehr abruppt startet dann schlecht
        # return 0
    ArtistSend._jct = None
    return 0
