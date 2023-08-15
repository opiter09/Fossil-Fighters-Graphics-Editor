import os

def toNitro(folder, path, file, screen, palList, imgList, image):
    f = open(path, "rb")
    data = f.read()
    f.close()
    if (screen != None):
        new = open(folder + file.split(".")[0] + ".nscr", "wb")
        new.close()
        new = open(folder + file.split(".")[0] + ".nscr", "ab")
            
        size = len(data)
        new.write((0x5243534E).to_bytes(4, "big"))
        new.write((0xFFFE0001).to_bytes(4, "big"))
        new.write((16 + 20 + size).to_bytes(4, "little"))
        new.write((0x10000100).to_bytes(4, "big"))
        new.write((0x4E524353).to_bytes(4, "big"))
        new.write((20 + size).to_bytes(4, "little"))
        new.write((screen[0]).to_bytes(2, "little"))
        new.write((screen[1]).to_bytes(2, "little"))
        new.write(bytes(4))
        new.write((size).to_bytes(4, "little"))
        new.write(data)
        new.close()
    elif (file in imgList):
        new = open(folder + file.split(".")[0] + ".ncgr", "wb")
        new.close()
        new = open(folder + file.split(".")[0] + ".ncgr", "ab")

        mod = 4
        if (image == True):
            mod = 0
        size = len(data) - mod
        new.write((0x5247434E).to_bytes(4, "big"))
        new.write((0xFFFE0101).to_bytes(4, "big"))
        new.write((16 + 32 + size).to_bytes(4, "little"))
        new.write((0x10000100).to_bytes(4, "big"))
        new.write((0x52414843).to_bytes(4, "big"))
        new.write((32 + size).to_bytes(4, "little"))
        new.write((size // 2048).to_bytes(2, "little"))
        if (data[2] == 0) and (image == False):
            new.write((0x200003000000).to_bytes(6, "big"))
        else:
            new.write((0x200004000000).to_bytes(6, "big"))
        new.write(bytes(8))
        new.write((size).to_bytes(4, "little"))
        new.write((0x18).to_bytes(4, "little"))
        new.write(data[mod:])
        new.close()
    elif (file in palList):
        new = open(folder + file.split(".")[0] + ".nclr", "wb")
        new.close()
        new = open(folder + file.split(".")[0] + ".nclr", "ab")

        mod = 4
        if (image == True):
            mod = 0
        size = len(data) - mod
        new.write((0x524C434E).to_bytes(4, "big"))
        new.write((0xFFFE0001).to_bytes(4, "big"))
        new.write((16 + 24 + size).to_bytes(4, "little"))
        new.write((0x10000100).to_bytes(4, "big"))
        new.write((0x54544C50).to_bytes(4, "big"))
        new.write((24 + size).to_bytes(4, "little"))
        new.write((3).to_bytes(4, "little"))
        new.write(bytes(4))
        new.write(size.to_bytes(4, "little"))
        new.write((16).to_bytes(4, "little"))
        new.write(data[mod:])
        new.close()