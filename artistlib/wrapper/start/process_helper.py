import subprocess
import socket
import time
import os


def is_port_open(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex((host, port)) == 0


def wait_to_start(flag_path, timeout=100):
    sleeptime = 1
    i = 0
    while not os.path.isfile(flag_path):
        # flag_file = "flag_artist_run.txt"
        # print("In wait schleife")
        time.sleep(sleeptime)
        if i >= timeout:
            raise Exception("It took to long to start artist, something went wrong")
        i = i + 1


def check_running_win() -> bool:
    tasks = subprocess.check_output(["tasklist"], text=True)
    if "aRTist.exe" in tasks:
        return True
    else:
        return False


def check_running_Linux() -> bool:
    result = subprocess.run(["pgrep", "-x", "aRTist"], capture_output=True, text=True)
    return result.returncode == 0
