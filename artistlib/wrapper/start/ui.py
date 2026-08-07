import subprocess
import ctypes
from ctypes import wintypes


def get_pid_by_name(process_name):
    result = subprocess.check_output("tasklist", text=True)

    for line in result.splitlines():
        parts = line.split()
        if not parts:
            continue
        if process_name.lower() == parts[0].lower():
            try:
                pid = int(parts[1])
                return pid
            except ValueError:
                pass
    return None


def get_hwnds_by_pid(pid):
    user32 = ctypes.windll.user32
    hwnds = []

    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)

    def callback(hwnd, lParam):
        lpdw_process_id = wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(lpdw_process_id))

        if lpdw_process_id.value == pid:
            hwnds.append(hwnd)

        return True

    user32.EnumWindows(EnumWindowsProc(callback), 0)

    return hwnds


def hide_window(hwnds):
    if hwnds:
        for hwnd in hwnds:
            ctypes.windll.user32.ShowWindow(hwnd, 0)


def show_window(hwnds):
    if hwnds:
        for hwnd in hwnds:
            ctypes.windll.user32.ShowWindow(hwnd, 5)


def hide_ui(name):
    pid = get_pid_by_name(name)
    hwnds = get_hwnds_by_pid(pid)
    hide_window(hwnds)


def show_ui(name):
    pid = get_pid_by_name(name)
    hwnds = get_hwnds_by_pid(pid)
    show_window(hwnds)
