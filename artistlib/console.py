import artistlib as a

list = ["SUCCESS", "RESULT", "STDOUT"]
commands = []

rc = a.Junction()

com = "::aRTist::GetVersion full"

c = 0
d = -1

while com != "exit":
    com = input("Command:")

    if "ß" in com:
        try:
            length = len(com)-1
            com = commands[d-length]
        except IndexError:
            print("No previous Command!")
    else:
        if not com in commands:
            commands.append(com)
            d += 1
    
    ver = a.Junction.send(rc, com, "*")

    for i in list:
        typ = a.Junction.pick(rc, ver, i)
        if "IMAGE" in ver and not "{}" in typ:
            name = input("Filename:")
            a.Junction.image(rc, name)
            print("Image saved as ", name)
            
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

else:
    exit()


