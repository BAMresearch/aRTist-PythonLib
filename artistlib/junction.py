"""Creates the remote control."""

# -*- coding: UTF-8 -*-
import logging
import numpy as np

# from numpy import append
import socket
import base64
import pathlib
from PIL import Image

logger = logging.getLogger(__name__)


class Junction:
    """Provides remote control functionality for the aRTist simulator."""

    def __init__(self, host="localhost", port=3658, bufferSize=1024, timeout=5):

        self.host = host
        self.port = port
        self.bufferSize = bufferSize
        self.timeout = timeout
        self.error = 0
        self.progress = 0
        self.answer = {}

        self.connect()

    def connect(self):
        self.S = socket.socket()  # Create socket (for TCP)
        self.S.connect((self.host, self.port))  # Connect to aRTist
        self.S.settimeout(self.timeout)
        self.listen(0)
        return self

    def send(self, command, msgType="RESULT"):
        c = command + "\n"
        self.S.send(c.encode())
        return self.listen(msgType=msgType)

    def listen(self, command_no=1, msgType="RESULT"):
        answer = ""
        stop = False
        if command_no == 0:
            self.S.settimeout(0.2)
        while not stop:  # and ("SUCCESS" not in total) and ("ERROR" not in total):     # Solange server antwortet und nicht "SUCCESS" enthält
            try:
                msg = self.S.recv(self.bufferSize).decode()

            except socket.timeout:
                answer += "RESULT Timeout\n"
                stop = True
                continue
            except OSError as e:
                answer += f"RESULT SocketError {e}\n"
                stop = True
                continue
            else:
                if "SUCCESS" in msg:
                    answer += msg
                    stop = True
                    continue
                elif "ERROR" in msg:
                    answer += msg
                    stop = True
                    # global error
                    self.error = self.error + 1
                    continue
                elif "PROGRESS" in msg:
                    try:
                        self.progress = float(msg.strip("PROGRESS "))
                    except Exception:
                        self.progress = 0
                    continue
                else:
                    if command_no == 0:
                        logger.debug(msg)
                    answer += msg
                if msg == "":
                    break

        self.S.settimeout(self.timeout)
        self.answer.update(
            {
                "SUCCESS": self.pick(answer, "SUCCESS"),
                "RESULT": self.pick(answer, "RESULT"),
                "SDTOUT": self.pick(answer, "STDOUT"),
                "BASE64": self.pick(answer, "BASE64"),
                "IMAGE": self.pick(answer, "IMAGE"),
                "FILE": self.pick(answer, "FILE"),
            }
        )
        if msgType != "*":
            answer = self.pick(answer, msgType)
        return answer

    def pick(self, answer, res="RESULT"):
        picked = ""
        for a in answer.split("\n"):
            if a.find(res) == 0:
                picked += a[1 + len(res) :].strip("\r") + "\n"
        if len(picked) == 0:
            return res + " not found."
        return picked

    def get_answer(self, key):
        return self.answer[key]

    def disconnect(self):
        try:
            self.S.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass
        self.S.close()

    def get_image(self, imageName: str) -> tuple[Image.Image, np.ndarray]:

        npTypes = [
            np.bool_,
            np.ubyte,
            np.byte,
            np.ubyte,
            np.short,
            np.ushort,
            np.intc,
            np.uintc,
            np.int_,
            np.uint,
            np.single,
            np.double,
        ]
        try:
            imageData = self.answer["BASE64"]

            decodedData = base64.b64decode((imageData))

            imageHeader = self.answer["IMAGE"].split()
            dtype = npTypes[int(imageHeader[4])]
            im = np.frombuffer(decodedData, dtype).reshape(
                (int(imageHeader[1]), int(imageHeader[0]))
            )

            return Image.fromarray(im), im

        except Exception as e:
            logger.exception("Error decoding image %s", imageName)
            # es handelt sich um einen Fehler und wir geben eine fallback Bild und array zurück
            size = (141, 141)
            arr_fallback = np.zeros(size, dtype=np.uint8)
            img_fall = Image.fromarray(arr_fallback)
            return img_fall, arr_fallback

    def save_disk(self, im: np.ndarray, imageName: str) -> None:
        Image.fromarray(im).save(imageName)

    # speichert direkt aus dem Image Object, sollte schneller sein
    def save_disk_imgObject(self, Img: Image.Image, imageName: str) -> None:
        Img.save(imageName)

    def receive_file(self, fileName):
        fileData = self.answer["BASE64"]
        decodedFile = base64.b64decode((fileData))
        artistFile = open(fileName, "wb")
        artistFile.write(decodedFile)
        artistFile.close()

    def send_file(self, fileName):
        outFile = open(fileName, "br")
        fileBytes = outFile.read()
        encBytes = base64.b64encode((fileBytes))
        encString = str(encBytes)
        encString = encString.lstrip("b'").rstrip("'")
        fileExtension = pathlib.Path(fileName).suffix
        com = "::RemoteControl::ReceiveFile " + encString + " " + fileExtension
        recAnswer = self.send(com, "RESULT")
        return recAnswer
