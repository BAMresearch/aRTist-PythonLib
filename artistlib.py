# -*- coding: UTF-8 -*-
"""The aRTist Python library is intended to remote control and automate the radiographic simulator aRTist.

.. include:: ./documentation.md
"""

from _version import get_versions
__version__ = get_versions()['version']
del get_versions

import numpy as np
from numpy import append
import socket
import base64
from PIL import Image


class Junction:
    """Remote control of aRTist simulator
    """
    def __init__(self, host="localhost", port=3658, bufferSize=1024, timeout=5):
        self.host = host
        self.port = port
        self.bufferSize = bufferSize
        self.timeout = timeout
        self.error = 0
        self.progress = 0
        self.answer = {}
        self.lst = []
        
        self.connect()
        

    def connect(self):
        self.S = socket.socket()                        # Create socket (for TCP)
        self.S.connect((self.host, self.port))          # Connect to aRTist
        self.S.settimeout(self.timeout)
        self.listen(0)
        return self

    def send(self, command, msgType="RESULT"):
        c = command + '\n'
        self.S.send(c.encode())
        return self.listen(msgType=msgType)

    def listen(self, command_no=1, msgType="RESULT"):
        answer = ""
        stop = False
        if (command_no == 0):
            self.S.settimeout(0.2)
        while (not stop):# and ("SUCCESS" not in total) and ("ERROR" not in total):     # Solange server antwortet und nicht "SUCCESS" enthält
            try:
                msg = self.S.recv(self.bufferSize).decode()
                
            except BaseException as e:
                err = e.args[0]
                if err == "timed out":
                    #print("Timeout\n")
                    answer += "RESULT Timeout\n"
                    stop = True
                    continue
            else:
                if ("SUCCESS" in msg):
                    answer += msg
                    stop = True
                    continue
                elif ("ERROR" in msg):
                    answer += msg
                    stop = True
                    #global error
                    self.error = self.error + 1 
                    continue
                elif ("PROGRESS" in msg):
                    try:
                        self.progress = float(msg.strip('PROGRESS '))
                    except:
                        self.progress = 0
                    continue
                else:
                    if (command_no == 0):
                        print(msg)
                    answer += msg
                    
        self.S.settimeout(self.timeout)
        if (msgType != "*"):
            answer = self.pick(answer, msgType)
        self.answer.update({"SUCCESS":self.pick(answer, "SUCCESS"), "RESULT":self.pick(answer, "RESULT"), "SDTOUT":self.pick(answer, "STDOUT"), "IMAGE":self.pick(answer, "IMAGE"), "BASE64":self.pick(answer, "BASE64")})
        return answer

    def pick(self, answer, res='RESULT'):
        picked = ""
        for a in answer.split('\n'):
            if a.find(res) == 0:
                picked += (a[1 + len(res):].strip('\r') + '\n')
        if len(picked) == 0:
        return picked

    def image(self):
        imageData = self.answer["BASE64"]
        decodedData = base64.b64decode((imageData))
        imageHeader = self.answer["IMAGE"]
        for i in imageHeader.split(" "):
            self.lst.append(i)
        if "LE" in self.lst[5]:
            dtype = np.uint16    
        #im = np.frombuffer(decodedData, np.uint16).reshape((10,10))
        im = np.frombuffer(decodedData, dtype).reshape((int(self.lst[1]),int(self.lst[2])))
        Image.fromarray(im).save("test2.png")

        
    
