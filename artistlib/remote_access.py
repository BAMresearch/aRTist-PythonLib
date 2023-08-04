import sys
import os
path = os.path.dirname(os.path.abspath(__file__))
path = os.path.dirname(path)
sys.path.insert(0, path)

import artistlib as a
from prompt_toolkit import PromptSession
session = PromptSession()

list = ["SUCCESS", "RESULT", "STDOUT"]
commands = []

rc = a.Junction()

c = 0

while True:
    try:
        com = session.prompt("Command: ")

        if "::RemoteControl::ReceiveFile" in com:
            fileName2 = input("Send following file: ")
            recAnswer = a.Junction.send_file(rc, fileName2)
            print(recAnswer)

        else:
            ans = a.Junction.send(rc, com, "*")

            if "FILE" in ans:
                fileName = input("Save file as: ")
                a.Junction.receive_file(rc, fileName)
                print("File saved as ", fileName)      

            for i in list:
                typ = a.Junction.pick(rc, ans, i)
                if "IMAGE" in ans and not "{}" in typ:
                    name = input("Save Image as: ")
                    a.Junction.save_image(rc, name)
                    print("Image saved as ", name)

                if not "{}" in typ:
                    if not "not found" in typ:
                        print(typ)
                    else:
                        c += 1
                else:
                    c += 1

            if c >= 3 and not "BASE64" in ans:
                print(ans)

            c = 0

    except KeyboardInterrupt:
        raise SystemExit
