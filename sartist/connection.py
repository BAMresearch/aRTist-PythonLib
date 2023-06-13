# Copyright 2023 TH DEGGENDORF (contact simon.wittl@th-deg.de)
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import socket
import warnings
import time
from threading import Thread
from .version import __send__, __receive__, __local__
from typing import Union
from pathlib import Path



class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None, args=()):
        Thread.__init__(self, group, target, name, args=args)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args) -> str:
        Thread.join(self, *args)
        return self._return


def receive_callback():
    s_recv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_recv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s_recv.bind(__receive__)

    s_recv.listen()

    connection, _ = s_recv.accept()
    data = connection.recv(2048)

    s_recv.close()

    return data.strip().decode("utf8")


def send_command(command: str):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(__local__)

    try:
        s.connect_ex(__send__)
        _ = s.recv(1024)
        _ = s.recv(1024)
    except socket.error:
        warnings.warn("No connection to artist possible. Is aRTist running?"
                      "Try to reconnect.")
        try:
            s.connect(__send__)
            _ = s.recv(1024)
            _ = s.recv(1024)
            time.sleep(1)
        except socket.error:
            return True

    command += f"; ::RemoteControl::CloseConnection [::RemoteControl::GetCurrentChannel] {__send__[0]} {__send__[1]}; "
    s.sendall(command.encode("utf-8"))

    s.close()
    return False


def send(command: str):
    error = True
    while error:
        send_connection = ThreadWithReturnValue(target=send_command, args=(command,))
        send_connection.start()
        error = send_connection.join()


def send_with_return(command: str):
    receive_connection = ThreadWithReturnValue(target=receive_callback)
    output = receive_connection.start()

    error = True
    while error:
        send_connection = ThreadWithReturnValue(target=send_command, args=(command,))
        send_connection.start()
        error = send_connection.join()

    output = receive_connection.join()

    return output

def _call_command(command: str, get_return=False, verbose=False) -> Union[None, str, list]:
    """
    Calls the aRTist command via socket remote connection.

    :param command: Command as string
    :param get_return: (bool) If set, a return value of teh command is expected
    :param verbose: (bool) Print some information
    :return:
    """

    if verbose:
        print(command)

    if get_return:
        return send_with_return(command)
    else:
        send(command)
        return None

def get_data_from_artist(command: str, verbose=False) -> Path:
    return _call_command("SaRTist::SendToPython {%s};" % command, get_return=True, verbose=verbose)



__aRTistPath__ = lambda: Path(get_data_from_artist('file nativename $::Xray(ProgramDir)', False))
__aRTistVersion__ = lambda: __aRTistPath__().name
__detectors__ = lambda: __aRTistPath__() / "Data" / "Detectors"
__sources__ = lambda: __aRTistPath__() / "Data" / "Library" / "Spectra"
