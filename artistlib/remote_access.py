import artistlib as a
import sys
from prompt_toolkit import PromptSession
session = PromptSession()

list = ["SUCCESS", "RESULT", "STDOUT"]
commands = []

rc = a.Junction()

c = 0

while True:
    try:
        com = session.prompt("Command: ")
    
        ver = a.Junction.send(rc, com, "*")

        for i in list:
            typ = a.Junction.pick(rc, ver, i)
            if "IMAGE" in ver and not "{}" in typ:
                name = input("Save Image as: ")
                a.Junction.image(rc, name)
                print("Image saved as ", name)
            
            if not "{}" in typ:
                if not "not found" in typ:
                    print(typ)
                else:
                    c += 1
            else:
                c += 1

        if c >= 3 and not "BASE64" in ver:
            print(ver)

        c = 0

    except KeyboardInterrupt:
        raise SystemExit


