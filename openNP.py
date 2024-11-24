import os
import sys
import subprocess
import FreeSimpleGUI as psg

layout = [
    [ psg.Button("Image", key = "image") ],
    [ psg.Button("Motion", key = "motion") ],
    [ psg.Button("Both", key = "both") ]
]

window = psg.Window("", layout, grab_anywhere = True, resizable = True, font = "-size 12")

locList = []
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if (event == psg.WINDOW_CLOSED) or (event == "Quit"):
        break
    elif (event == "image"):
        locList = ["./image_NDS_UNPACK"]
        break
    elif (event == "motion"):
        locList = ["./motion_NDS_UNPACK"]
        break
    elif (event == "both"):
        locList = ["./image_NDS_UNPACK", "./motion_NDS_UNPACK"]
        break
window.close()

forbidden = ["image_big_archive"]
bigDictEnergy = {}

for loc in locList:
    for root, dirs, files in os.walk(loc):
        for file in files:
            if (file == "combo.txt"):
                f = open(os.path.join(root, file), "rt")
                r = f.read()
                f.close()
                lines = list(r.split("\n")).copy()
                current = ""
                palArc = ""
                imgArc = ""
                scrArc = ""
                for i in range(len(lines)):
                    if ((lines[i] != "") and ((i == 0) or ((i >= 2) and (lines[i - 2] == "") and (lines[i - 1] == "")))):
                        palArc = ""
                        imgArc = ""
                        scrArc = ""
                        current = lines[i][0:-1] + " (" + os.path.join(root, file)[2:-9].replace("_NDS_UNPACK", "") + ")"
                        bigDictEnergy[current] = { "pal": [], "img": [], "scr": [] }
                    elif (lines[i].startswith("Palette ARC") == True):
                        palArc = lines[i].split(": ")[1]
                    elif (lines[i].startswith("Image ARC") == True):
                        imgArc = lines[i].split(": ")[1]    
                    elif (lines[i].startswith("Screen ARC") == True):
                        scrArc = lines[i].split(": ")[1]
                    elif (lines[i].endswith(".nclr") == True):
                        if (palArc not in forbidden):
                            bigDictEnergy[current]["pal"].append(os.path.join(root, file)[0:-9] + "/" + palArc + "/" + lines[i][1:])
                    elif (lines[i].endswith(".ncgr") == True):
                        if (imgArc not in forbidden):
                            bigDictEnergy[current]["img"].append(os.path.join(root, file)[0:-9] + "/" + imgArc + "/" + lines[i][1:])    
                    elif (lines[i].endswith(".nscr") == True):
                        if (scrArc not in forbidden):
                            bigDictEnergy[current]["scr"].append(os.path.join(root, file)[0:-9] + "/" + scrArc + "/" + lines[i][1:])  

keys = list(bigDictEnergy.keys()).copy()
for k in bigDictEnergy.keys():
    if (len(bigDictEnergy[k]["pal"]) == 0):
        keys.remove(k)
keys.sort()

layout2 = [
    [ psg.Text("Combo:", size = 7), psg.DropDown(keys, key = "file", default_value = keys[0]) ],
    [ psg.Text("Sprite:", size = 7), psg.DropDown(list(range(1, 100)), key = "num", default_value = 1) ],
    [ psg.Button("Open", key = "open") ]
]

window2 = psg.Window("", layout2, grab_anywhere = True, resizable = True, font = "-size 12")

while True:
    event, values = window2.read()
    # See if user wants to quit or window was closed
    if (event == psg.WINDOW_CLOSED) or (event == "Quit"):
        break
    elif (event == "open"):
        val = values["file"]
        val2 = values["num"]
        inp = ["NitroPaint_old.exe"]
        for k in ["pal", "img", "scr"]:
            if (len(bigDictEnergy[val][k]) >= val2):
                inp.append(bigDictEnergy[val][k][val2 - 1].replace("./", "./\\"))
            elif (len(bigDictEnergy[val][k]) > 0):
                inp.append(bigDictEnergy[val][k][-1].replace("./", "./\\"))
        subprocess.Popen(inp)

    