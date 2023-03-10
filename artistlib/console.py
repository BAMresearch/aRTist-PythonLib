import base64
import artistlib as a

list = ["SUCCESS", "RESULT", "STDOUT"]

rc = a.Junction()

com = "::aRTist::GetVersion full"

c = 0

while com != "exit":
    ver = a.Junction.send(rc, com, "*")
    
    for i in list:
        typ = a.Junction.pick(rc, ver, i)
        if not "{}" in typ:
            if not "not found" in typ:
                print(typ)
            else:
                c += 1
        else:
            c += 1

    if c >= 3:
        print(ver)

    c = 0
                
    com = input("Command:")
else:
    exit()


