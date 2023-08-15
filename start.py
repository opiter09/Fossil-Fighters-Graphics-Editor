import combo
import convert
import finish
import os
import shutil
import subprocess
import sys

check = 0
folder = sys.argv[1].split("\\")[-1][0:-4] + "/"

if (os.path.exists(folder) == False):
    subprocess.run([ "dslazy.bat", "UNPACK", sys.argv[1] ])
    os.rename("NDS_UNPACK", folder)
    check = 1

if (os.path.exists("motion_" + folder) == False):
    os.mkdir("motion_" + folder)
    d = []
    for root, dirs, files in os.walk(folder + "data/motion"):
        for k in dirs:
            d.append(k)
    for val in d:
        palList = []
        imgList = []
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
                        palList = palList + ret[0]
                        imgList = imgList + ret[1]
                    else:
                        ret = combo.mpmContribute(file, data, "motion_" + folder + val + "/combo.txt")
                        palList = palList + ret[0]
                        imgList = imgList + ret[1]
                        if (len(ret[2]) > 0):
                            screenDict[str(int.from_bytes(data[0x34:0x38], "little")) + ".bin"] = [
                                int.from_bytes(data[0x10:0x14], "little"),
                                int.from_bytes(data[0x14:0x18], "little")
                            ]
        for root, dirs, files in os.walk(folder + "data/motion/" + val):
            for file in files:
                if (file.endswith("_arc.bin") == True) and (file.endswith(".json") == False):
                    os.mkdir("motion_" + folder + val + "/" + file + "/")
                    subprocess.run(["fftool.exe", os.path.join(root, file) ])
                    for root2, dirs2, files2 in os.walk(folder + "data/motion/" + val + "/bin/" + file):
                        for file2 in files2:
                            try:
                                convert.toNitro("motion_" + folder + val + "/" + file + "/", os.path.join(root2, file2), file2,
                                    screenDict[file2], palList, imgList, False)
                            except KeyError:
                                convert.toNitro("motion_" + folder + val + "/" + file + "/", os.path.join(root2, file2), file2, None,
                                    palList, imgList, False)
        os.rename(folder + "data/motion/" + val + "/bin/", "motion_" + folder + val + "/bin/")
    check = 1

if (os.path.exists("image_" + folder) == False):        
    os.mkdir("image_" + folder)
    palList = []
    imgList = []
    screenDict = {}
    com = open("image_" + folder + "combo.txt", "wt")
    com.close()
    for root, dirs, files in os.walk(folder + "data/image"):
        for file in files:
            if (file.endswith("_archive") == False) and (file.endswith(".json") == False):
                f = open(os.path.join(root, file), "rb")
                data = f.read()[0x2C:]
                f.close()
                if (int.from_bytes(data[0:4], "big") == 0x4D4D5300):
                    ret = combo.mmsContribute(file, data, "image_" + folder + "/combo.txt")
                    palList = palList + ret[0]
                    imgList = imgList + ret[1]
                else:
                    ret = combo.mpmContribute(file, data, "image_" + folder + "/combo.txt")
                    palList = palList + ret[0]
                    imgList = imgList + ret[1]
                    if (len(ret[2]) > 0):
                        screenDict[str(int.from_bytes(data[0x34:0x38], "little")) + ".bin"] = [
                            int.from_bytes(data[0x10:0x14], "little"),
                            int.from_bytes(data[0x14:0x18], "little")
                        ]
    for root, dirs, files in os.walk(folder + "data/image"):
        for file in files:
            if (file.endswith("_archive") == True) and (file.endswith(".json") == False):
                os.mkdir("image_" + folder + file)
                subprocess.run(["fftool.exe", os.path.join(root, file) ])
                for root2, dirs2, files2 in os.walk(folder + "data/image/bin/" + file):
                    for file2 in files2:
                        try:
                            convert.toNitro("image_" + folder + file + "/", os.path.join(root2, file2), file2, screenDict[file2],
                                palList, imgList, True)
                        except KeyError:
                            convert.toNitro("image_" + folder + file + "/", os.path.join(root2, file2), file2, None,
                                palList, imgList, True)
    os.rename(folder + "data/image/bin/", "image_" + folder + "bin/")
    os.remove("image_" + folder + "bin/image_archive/meta.json")
    shutil.copyfile("meta_image.json", "image_" + folder + "bin/image_archive/meta.json")
    os.remove("image_" + folder + "bin/image_cleaning_archive/meta.json")
    shutil.copyfile("meta_cleaning.json", "image_" + folder + "bin/image_cleaning_archive/meta.json")    
    check = 1

if (check == 0):
    finish.run()

        
    