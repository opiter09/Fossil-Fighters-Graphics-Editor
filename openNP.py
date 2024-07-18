import os
import sys
import subprocess
import FreeSimpleGUI as psg

bigDictEnergy = {}

for loc in ["./image_NDS_UNPACK", "./motion_NDS_UNPACK"]:
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
                        bigDictEnergy[current]["pal"].append(os.path.join(root, file)[0:-9] + "/" + palArc + "/" + lines[i][1:])
                    elif (lines[i].endswith(".ncgr") == True):
                        bigDictEnergy[current]["img"].append(os.path.join(root, file)[0:-9] + "/" + imgArc + "/" + lines[i][1:])    
                    elif (lines[i].endswith(".nscr") == True):
                        bigDictEnergy[current]["scr"].append(os.path.join(root, file)[0:-9] + "/" + scrArc + "/" + lines[i][1:])  

keys = list(bigDictEnergy.keys()).copy()
keys.sort()
layout = [
    [ psg.Text("Combo:", size = 7), psg.DropDown(keys, key = "file", default_value = keys[0]) ],
    [ psg.Text("Sprite:", size = 7), psg.DropDown(list(range(1, 100)), key = "num", default_value = 1) ],
    [ psg.Button("Open", key = "open") ]
]

window = psg.Window("", layout, grab_anywhere = True, resizable = True, font = "-size 12")

while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if (event == psg.WINDOW_CLOSED) or (event == "Quit"):
        break
    elif (event == "open"):
        val = values["file"]
        val2 = values["num"]
        inp = ["NitroPaint.exe"]
        for k in ["pal", "img", "scr"]:
            if (len(bigDictEnergy[val][k]) >= val2):
                inp.append(bigDictEnergy[val][k][val2 - 1])
            elif (len(bigDictEnergy[val][k]) > 0):
                inp.append(bigDictEnergy[val][k][-1])
        subprocess.run(inp)
        print(bigDictEnergy[val]["pal"])


    