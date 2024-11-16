import combo
import convert
import finish
import os
import shutil
import subprocess
import sys

check = 0
f = open(sys.argv[1], "rb")
test = f.read()[12]
f.close()
if (test == ord("Y")):
    rom = "ff1"
else:
    rom = "ffc"
folder = "NDS_UNPACK" + "/"

if (os.path.exists(folder) == False):
    subprocess.run([ "dslazy.bat", "UNPACK", sys.argv[1] ])
    # os.rename("NDS_UNPACK", folder)
    check = 1
    
if (rom == "ffc"):
    subprocess.run([ "xdelta3-3.0.11-x86_64.exe", "-d", "-f", "-s", "NDS_UNPACK/arm9.bin", "ffc_apFix.xdelta",
        "NDS_UNPACK/arm9x.bin" ])
    if (os.path.exists("NDS_UNPACK/arm9x.bin") == True):
        os.remove("NDS_UNPACK/arm9.bin")
        os.rename("NDS_UNPACK/arm9x.bin", "NDS_UNPACK/arm9.bin")

if (os.path.exists("motion_" + folder) == False):
    os.mkdir("motion_" + folder)
    d = []
    for root, dirs, files in os.walk(folder + "data/motion"):
        for k in dirs:
            d.append(k)
    for val in d:
        palDict = {}
        imgDict = {}
        screenDict = {}
        os.mkdir("motion_" + folder + val)
        com = open("motion_" + folder + val + "/combo.txt", "wt")
        com.close()
        for root, dirs, files in os.walk(folder + "data/motion/" + val):
            for file in files:
                if (file.endswith("_arc.bin") == False) and (file.endswith(".json") == False):
                    f = open(os.path.join(root, file), "rb")
                    data = f.read()[0x2C:]
                    f.close()
                    if (int.from_bytes(data[0:4], "big") == 0x4D4D5300):
                        ret = combo.mmsContribute(file, data, "motion_" + folder + val + "/combo.txt")
                        if (ret[3] in palDict.keys()):
                            palDict[ret[3]] = palDict[ret[3]] + ret[0]
                        else:
                            palDict[ret[3]] = ret[0]
                        if (ret[4] in imgDict.keys()):
                            imgDict[ret[4]] = imgDict[ret[4]] + ret[1]
                        else:
                            imgDict[ret[4]] = ret[1]
                    else:
                        ret = combo.mpmContribute(file, data, "motion_" + folder + val + "/combo.txt")
                        if (ret[3] in palDict.keys()):
                            palDict[ret[3]] = palDict[ret[3]] + ret[0]
                        else:
                            palDict[ret[3]] = ret[0]
                        if (ret[4] in imgDict.keys()):
                            imgDict[ret[4]] = imgDict[ret[4]] + ret[1]
                        else:
                            imgDict[ret[4]] = ret[1]
                        if (ret[5] != "MPM"):
                            if (ret[5] not in screenDict.keys()):
                                screenDict[ret[5]] = {}
                            screenDict[ret[5]][str(int.from_bytes(data[0x34:0x38], "little")) + ".bin"] = [
                                int.from_bytes(data[0x10:0x14], "little"),
                                int.from_bytes(data[0x14:0x18], "little")
                            ]
        for root, dirs, files in os.walk(folder + "data/motion/" + val):
            for file in files:
                if (file.endswith("_arc.bin") == True) and (file.endswith(".json") == False) and (file in palDict.keys()):
                    os.mkdir("motion_" + folder + val + "/" + file + "/")
                    subprocess.run(["fftool.exe", os.path.join(root, file) ])
                    for root2, dirs2, files2 in os.walk(folder + "data/motion/" + val + "/bin/" + file):
                        for file2 in files2:
                            try:
                                convert.toNitro("motion_" + folder + val + "/" + file + "/", os.path.join(root2, file2), file2,
                                    screenDict[file][file2], palDict[file], imgDict[file], False)
                            except KeyError:
                                convert.toNitro("motion_" + folder + val + "/" + file + "/", os.path.join(root2, file2), file2, None,
                                    palDict[file], imgDict[file], False)
        os.rename(folder + "data/motion/" + val + "/bin/", "motion_" + folder + val + "/bin/")
    check = 1

if (os.path.exists("image_" + folder) == False):        
    os.mkdir("image_" + folder)
    palDict = {}
    imgDict = {}
    screenDict = {}
    com = open("image_" + folder + "combo.txt", "wt")
    com.close()
    for root, dirs, files in os.walk(folder + "data/image"):
        for file in files:
            if (file.endswith("_archive") == False) and (file.endswith(".json") == False) and (file.endswith(".hash") == False):
                f = open(os.path.join(root, file), "rb")
                data = f.read()[0x2C:]
                f.close()
                if (int.from_bytes(data[0:4], "big") == 0x4D4D5300):
                    ret = combo.mmsContribute(file, data, "image_" + folder + "/combo.txt")
                    if (ret[3] in palDict.keys()):
                        palDict[ret[3]] = palDict[ret[3]] + ret[0]
                    else:
                        palDict[ret[3]] = ret[0]
                    if (ret[4] in imgDict.keys()):
                        imgDict[ret[4]] = imgDict[ret[4]] + ret[1]
                    else:
                        imgDict[ret[4]] = ret[1]
                else:
                    ret = combo.mpmContribute(file, data, "image_" + folder + "/combo.txt")
                    if (ret[3] in palDict.keys()):
                        palDict[ret[3]] = palDict[ret[3]] + ret[0]
                    else:
                        palDict[ret[3]] = ret[0]
                    if (ret[4] in imgDict.keys()):
                        imgDict[ret[4]] = imgDict[ret[4]] + ret[1]
                    else:
                        imgDict[ret[4]] = ret[1]
                    if (ret[5] != "MPM"):
                        if (ret[5] not in screenDict.keys()):
                            screenDict[ret[5]] = {}
                        screenDict[ret[5]][str(int.from_bytes(data[0x34:0x38], "little")) + ".bin"] = [
                            int.from_bytes(data[0x10:0x14], "little"),
                            int.from_bytes(data[0x14:0x18], "little")
                        ]
    for root, dirs, files in os.walk(folder + "data/image"):
        for file in files:
            if (file.endswith("_archive") == True) and (file.endswith(".json") == False):
                forbidden = ["image_big_archive"]
                if (rom == "ff1") or (file not in forbidden):
                    os.mkdir("image_" + folder + file)
                    subprocess.run(["fftool.exe", os.path.join(root, file) ])
                    for root2, dirs2, files2 in os.walk(folder + "data/image/bin/" + file):
                        for file2 in files2:
                            try:
                                convert.toNitro("image_" + folder + file + "/", os.path.join(root2, file2), file2, screenDict[file][file2],
                                    palDict[file], imgDict[file], True)
                            except KeyError:
                                convert.toNitro("image_" + folder + file + "/", os.path.join(root2, file2), file2, None,
                                    palDict[file], imgDict[file], True)
    os.rename(folder + "data/image/bin/", "image_" + folder + "bin/")
    check = 1

if (check == 0):
    finish.run(rom)

        
    