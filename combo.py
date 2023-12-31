import os

def mmsContribute(file, data, com):
    palList = []
    imgList = []
    new = open(com, "at")
    palCount = int.from_bytes(data[0x24:0x28], "little")
    palStart = int.from_bytes(data[0x28:0x2C], "little")
    palName = int.from_bytes(data[0x2C:0x30], "little")
    imgCount = int.from_bytes(data[0x30:0x34], "little")
    imgStart = int.from_bytes(data[0x34:0x38], "little")
    imgName = int.from_bytes(data[0x38:0x3C], "little")
    new.write(file.upper() + ":" + "\n")
    name1 = ""
    i = palName
    while data[i] > 0:
        name1 = name1 + chr(data[i])
        i = i + 1
    new.write("Palette ARC: " + name1 + "\n")
    new.write("Palettes:" + "\n")
    for j in range(palCount):
        new.write("\t" + str(int.from_bytes(data[(palStart + j * 4):(4 + palStart + j * 4)], "little")) + ".nclr" + "\n")
        palList.append(str(int.from_bytes(data[(palStart + j * 4):(4 + palStart + j * 4)], "little")) + ".bin")
    name2 = ""
    i = imgName
    while data[i] > 0:
        name2 = name2 + chr(data[i])
        i = i + 1
    new.write("Image ARC: " + name2 + "\n")
    new.write("Images:" + "\n")
    for j in range(imgCount):
        new.write("\t" + str(int.from_bytes(data[(imgStart + j * 4):(4 + imgStart + j * 4)], "little")) + ".ncgr" + "\n")
        imgList.append(str(int.from_bytes(data[(imgStart + j * 4):(4 + imgStart + j * 4)], "little")) + ".bin")
    new.write("\n\n")
    new.close()
    return([palList, imgList, [], name1, name2])
    
def mpmContribute(file, data, com):
    palList = []
    imgList = []
    scrList = []
    new = open(com, "at")
    palIndex = int.from_bytes(data[0x24:0x28], "little")
    palName = int.from_bytes(data[0x28:0x2C], "little")
    imgIndex = int.from_bytes(data[0x2C:0x30], "little")
    imgName = int.from_bytes(data[0x30:0x34], "little")
    scrIndex = int.from_bytes(data[0x34:0x38], "little")
    scrName = int.from_bytes(data[0x38:0x3C], "little")
    new.write(file.upper() + ":" + "\n")
    name1 = ""
    i = palName
    while data[i] > 0:
        name1 = name1 + chr(data[i])
        i = i + 1
    new.write("Palette ARC: " + name1 + "\n")
    new.write("Palettes:" + "\n")
    for j in range(1):
        new.write("\t" + str(palIndex) + ".nclr" + "\n")
        palList.append(str(palIndex) + ".bin")
    name2 = ""
    i = imgName
    while data[i] > 0:
        name2 = name2 + chr(data[i])
        i = i + 1
    new.write("Image ARC: " + name2 + "\n")
    new.write("Images:" + "\n")
    for j in range(1):
        new.write("\t" + str(imgIndex) + ".ncgr" + "\n")
        imgList.append(str(imgIndex) + ".bin")
    name3 = ""
    i = scrName
    while data[i] > 0:
        name3 = name3 + chr(data[i])
        i = i + 1
    if (name3 != "MPM"):
        new.write("Screen ARC: " + name3 + "\n")
        new.write("Screens:" + "\n")
        for j in range(1):
            new.write("\t" + str(scrIndex) + ".nscr" + "\n")
            scrList.append(str(scrIndex) + ".bin")
        new.write("\n\n")
        new.close()
    else:
        new.write("\n\n")
        new.close()
    return([palList, imgList, scrList, name1, name2, name3])