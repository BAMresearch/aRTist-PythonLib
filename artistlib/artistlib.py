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
import sys
import os
from PIL import Image


class Junction:
    """Remote control of aRTist simulator
    """
    def __init__(self, host="localhost", port=3658, bufferSize=1024, timeout=10):
        self.host = host
        self.port = port
        self.bufferSize = bufferSize
        self.timeout = timeout
        self.error = 0
        self.progress = 0
        self.answer = {}
        self.lst = []
        self.lst2 = []
        self.splitter = "\n{}\n"
        
        self.connect()
        

    def connect(self):
        self.S = socket.socket()                        # Create socket (for TCP)
        self.S.connect((self.host, self.port))          # Connect to aRTist
        self.S.settimeout(self.timeout)
        self.listen(0)
        return self

    def send(self, command, msgType="*"):
        c = command + '\n'
        self.S.sendall(c.encode())
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
        self.answer.update({"SUCCESS":self.pick(answer, "SUCCESS"), "RESULT":self.pick(answer, "RESULT"), "SDTOUT":self.pick(answer, "STDOUT"), "BASE64":self.pick(answer, "BASE64"), "IMAGE":self.pick(answer, "IMAGE"), "FILE":self.pick(answer, "FILE")})
        return answer

    def pick(self, answer, res='RESULT'):
        picked = ""
        for a in answer.split('\n'):
            if a.find(res) == 0:
                picked += (a[1 + len(res):].strip('\r') + '\n')
        if len(picked) == 0:
                return res + ' not found.'
        return picked

    def image(self, imageName):
        self.lst.clear()
        cTypes = ["bit", "char", "signed char", "unsigned char", "short", "unsigned short", "int", "unsigned int", "long", "unsigned long", "float", "double"]
        npTypes = [np.bool_, np.ubyte, np.byte, np.ubyte, np.short, np.ushort, np.intc, np.uintc, np.int_, np.uint, np.single, np.double]
        imageData = self.answer["BASE64"]
        decodedData = base64.b64decode((imageData))
        imageHeader = self.answer["IMAGE"]
        for i in imageHeader.split(","):
            self.lst.append(i)
        imType = self.lst[4]
        if imType in cTypes:
            dtype = npTypes[cTypes.index(imType)]
        im = np.frombuffer(decodedData, dtype).reshape((int(self.lst[1]),int(self.lst[2])))
        Image.fromarray(im).save(imageName)


    def send_file(self, fileName):
        fileData = self.answer["BASE64"]
        decodedFile = base64.b64decode((fileData))
        artistFile = open(fileName, "wb")
        artistFile.write(decodedFile)
        artistFile.close()
        

    def receive_file(self, filePath):
        directory = os.getcwd()
        with open(filePath, "rb") as file:
            fileSize = os.path.getsize(f"{directory}\\{filePath}")
            i = 0
            while True:
                chunk = file.read(2048)
                i = i+1
                if len(chunk) == 2048 and i%10 == 0:
                    percent = round(100*(i*len(chunk))/fileSize)
                    print(percent, "% completed...")
                if not chunk:
                    break
                encChunk = base64.b64encode((chunk)).decode('utf-8')
                com = f"RemoteControl::ReceiveFile {encChunk} .aRTist"
                self.send(com, "RESULT")
        finalMessage = 'RemoteControl::ReceiveFile Stop .aRTist'
        recFinal = self.send(finalMessage, "RESULT")
        return recFinal
    
    def receive_image(self, imagePath, imageType):
        directory = f"{imagePath}.{imageType}"
        directory2 = os.getcwd()
        with open(directory, "rb") as imageFile:
            imageSize = os.path.getsize(f"{directory2}\\{directory}")
            i = 0
            while True:
                chunk = imageFile.read(2048)
                i = i+1
                if len(chunk) == 2048 and i%10 == 0:
                    percent = round(100*(i*len(chunk))/imageSize)
                    print(percent, "% completed...")
                if not chunk:
                    break
                encChunk = base64.b64encode((chunk)).decode('utf-8')
                com = f"RemoteControl::ReceiveFile {encChunk} .{imageType}"
                self.send(com, "RESULT")
            finalMessage = f"RemoteControl::ReceiveFile Stop .{imageType}"
            recFinal = self.send(finalMessage, "RESULT")
            openImage = recFinal.replace("\n", "")
            self.send(f'::FileIO::OpenAny "{openImage}"')
            return recFinal
        
 
    
        
    
