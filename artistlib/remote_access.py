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

        if "::RemoteControl::ReceiveFile" in com:
            fileName2 = input("Send following file: ")
            rec_final = a.Junction.receive_file(rc, fileName2)
            print(rec_final)
            
        if "::RemoteControl::ReceiveImage" in com:
            imageFile = input("Send following image: ")
            imageList = imageFile.split(".")
            imageName = imageList[0]
            imageType = imageList[1]
            recFinal = a.Junction.receive_image(rc, imageName, imageType)
            print(recFinal)

       
            
        else:
            ver = a.Junction.send(rc, com, "*")

            if "FILE" in ver:
                fileName = input("Sav File as: ")
                a.Junction.send_file(rc, fileName)
                print("File saved as ", fileName)      
                
               

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


