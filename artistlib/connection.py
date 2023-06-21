# Copyright 2023 Simon Wittl (Deggendorf Institute of Technology)
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
from __future__ import annotations

import socket
from .common_types import SendTypes, CommandTypes




class Connection:
    """Main connection class for the aRTist API
    """
    def __init__(self, host: str = "localhost", port: int = 3658, buffer_size: int = 1024, timeout: float = 5., listen_timeout: float = 0.2, verbose: bool = True):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.timeout = timeout
        self.listen_timeout = listen_timeout
        self.verbose = verbose
        self.error = 0

        self.connect()
    
    def connect(self):
        """Establish connection to the aRTist remote console
        """
        self.socket = socket.socket()                        # Create socket (for TCP)
        self.socket.connect((self.host, self.port))          # Connect to aRTist
        self.socket.settimeout(self.timeout)
        self.listen(command_no=CommandTypes.CONNECTION)
    
    def send(self, commands: str | list, type: str = SendTypes.RESULT) -> str:
        """Send a command to the aRTist remote console.

        Args:
            commands (str | list): TCL / TK command.
            type (str, optional): Defines the send and result type. Defaults to SendTypes.RESULT.

        Returns:
            str: Result of the command. Dependend of the send type
        """
        if isinstance(commands, str):
            commands = [commands]
        answers = []
        for c in commands:
            self.socket.send(c.encode())
            answers.append(self.listen(type=type))
        return answers
    
    def listen(self, command_no: int = CommandTypes.SEND, type: str = SendTypes.RESULT):
        answer = ""
        stop = False
        if (command_no == CommandTypes.CONNECTION):
            self.socket.settimeout(0.2)
        while not stop:# and ("SUCCESS" not in total) and ("ERROR" not in total):     # Solange server antwortet und nicht "SUCCESS" enthält
            try:
                msg = self.socket.recv(self.buffer_size).decode()
            except BaseException as e:
                err = e.args[0]
                if err == SendTypes.TIME_OUT:
                    answer += "RESULT Timeout\n"
                    stop = True
                    continue
            else:
                if SendTypes.SUCCESS in msg:
                    answer += msg
                    stop = True
                    continue
                elif SendTypes.ERROR in msg:
                    answer += msg
                    stop = True
                    #global error
                    self.error = self.error + 1 
                    continue
                else:
                    if command_no == 0:
                        print(msg) if self.verbose else None
                    answer += msg
        self.socket.settimeout(self.timeout)
        if type != SendTypes.ALL:
            answer = self.result(answer, type)
        return answer
    
    def result(self, answer: str, res: str = SendTypes.RESULT):
        """_summary_

        Args:
            answer (str): _description_
            res (str, optional): _description_. Defaults to SendTypes.RESULT.

        Returns:
            _type_: _description_
        """
        start = answer.find(res+' ')
        if start == -1:
            return res + ' not found.'
        start += len(res) + 1
        end = answer.find('\n', start)  # one line per result
        if answer.find('\r', start) == end-1:  # care for Windows line endings
            end -= 1
        return answer[start:end]
    
    @staticmethod
    def extract_result(answer: str, res: str = SendTypes.RESULT):
        start = answer.find(res+' ')
        if start == -1:
            return res + ' not found.'
        start += len(res) + 1
        end = answer.find('\n', start)  # one line per result
        if answer.find('\r', start) == end-1:  # care for Windows line endings
            end -= 1
        return answer[start:end]
    
    @staticmethod
    def string_to_list(message: str, dtype: callable = float):
        return_list = list()
        for element in message.split(' '):
            return_list.append(dtype(element))
        return return_list
    
    
