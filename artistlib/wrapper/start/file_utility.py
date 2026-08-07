import logging
import os
import json
import ctypes

logger = logging.getLogger(__name__)


def find_file(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
    return None


def read_json(file):
    try:
        with open(file) as f:
            d = json.load(f)
        return d
    except Exception as e:
        logger.exception("Something went wrong while reading %s", file)
        return None


def write_json(file, data):
    try:
        with open(file, "w") as f:
            json.dump(data, f)
    except Exception as e:
        logger.exception("Something went wrong while writing %s", file)


def create_file(file, cmd):
    with open(file, "w") as f:
        f.write(cmd)


def delete_file(file):
    if os.path.exists(file):
        os.remove(file)

 
def check_pid(pid):
    PROCESS_QUERY_INFROMATION = 0x1000
    processHandle = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_INFROMATION, 0,pid)
    if processHandle == 0:
        return False
    else:
        ctypes.windll.kernel32.CloseHandle(processHandle)
    return True

def find_file_del(path,start, end):
    files = os.listdir(path)
    for file in files:
        if file.startswith(start) and file.endswith(end):
            pid=int(file.split(start)[-1].split(end)[0])
            if not check_pid(pid):
                delete_file(file=os.path.join(path,file))
