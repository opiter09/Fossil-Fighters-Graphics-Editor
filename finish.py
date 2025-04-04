import convert
import FreeSimpleGUI as psg
import os
import subprocess
import sys

def run(rom):
    folder = "NDS_UNPACK"
    d = []
    for root, dirs, files in os.walk("motion_" + folder):
        for k in dirs:
            d.append(k)
    d = list(set(d))
    for val in d:
        dv = []
        for root, dirs, files in os.walk("motion_" + folder + "/" + val):
            for k in dirs:
                dv.append(k)
        dv = list(set(dv))
        try:
            dv.remove("bin")
        except:
            continue
        for val2 in dv:
            for root, dirs, files in os.walk("motion_" + folder + "/" + val + "/" + val2):
                for file in files:
                    if (file.endswith(".nclr") == True):
                        header = 40
                    elif (file.endswith(".ncgr") == True):
                        header = 48
                    else:
                        header = 36
                    f = open("motion_" + folder + "/" + val + "/bin/" + val2 + "/" + file[0:-5] + ".bin", "rb")
                    reading = f.read()
                    f.close()
                    start = reading[0:4]
                    os.remove("motion_" + folder + "/" + val + "/bin/" + val2 + "/" + file[0:-5] + ".bin")
                    new = open("motion_" + folder + "/" + val + "/bin/" + val2 + "/" + file[0:-5] + ".bin", "wb")
                    new.close()
                    new = open("motion_" + folder + "/" + val + "/bin/" + val2 + "/" + file[0:-5] + ".bin", "ab")
                    f2 = open(os.path.join(root, file), "rb")
                    reading2 = f2.read()
                    f2.close()
                    if (header != 36):
                        new.write(start)
                    new.write(reading2[header:])
                    new.close()
            try:
                os.rename("motion_" + folder + "/" + val + "/bin/" + val2 + "/meta.json",
                    "motion_" + folder + "/" + val + "/bin/" + val2 + "/metaz.json")
            except:
                pass
            try:
                os.remove(folder + "/data/motion/" + val + "/" + val2)
            except:
                pass
            subprocess.run([ "fftool.exe", "compress", "motion_" + folder + "/" + val + "/bin/" + val2, "-c", "Rle", "-c", "None",
                "-m", "32768", "-o", folder + "/data/motion/" + val + "/" + val2 ])
            print("motion/" + val + "/" + val2 + " Done")


    dv = [ "image_archive", "image_big_archive", "image_cleaning_archive" ]
    if (rom == "ffc"):
        dv = dv + [ "image_bitmap_archive", "image_credit_archive", "image_map_archive", "image_object_archive" ]
        # dv.remove("image_big_archive")
    for val2 in dv:
        for root, dirs, files in os.walk("image_" + folder + "/" + val2):
            for file in files:
                if (file.endswith(".nclr") == True):
                    header = 40
                elif (file.endswith(".ncgr") == True):
                    header = 48
                else:
                    header = 36
                os.remove("image_" + folder + "/bin/" + val2 + "/" + file[0:-5] + ".bin")
                new = open("image_" + folder + "/bin/" + val2 + "/" + file[0:-5] + ".bin", "wb")
                new.close()
                new = open("image_" + folder + "/bin/" + val2 + "/" + file[0:-5] + ".bin", "ab")
                f2 = open(os.path.join(root, file), "rb")
                reading2 = f2.read()
                f2.close()
                new.write(reading2[header:])
                new.close()
        try:
            os.rename("image_" + folder + "/bin/" + val2 + "/meta.json", "image_" + folder + "/bin/" + val2 + "/metaz.json")
        except:
            pass
        try:
            os.remove(folder + "/data/image/" + val2)
        except:
            pass
        if (rom == "ffc") and (val2 == "image_archive"):
            subprocess.run([ "fftool.exe", "compress", "image_" + folder + "/bin/" + val2,  "-c", "None", "-c", "None",
                "-m", "32768", "-o", folder + "/data/image/" + val2 ])
        else:
            subprocess.run([ "fftool.exe", "compress", "image_" + folder + "/bin/" + val2,  "-c", "Rle", "-c", "None",
                "-m", "32768", "-o", folder + "/data/image/" + val2 ])
        print("image/" + val2 + " Done")

    # os.rename(folder, "NDS_UNPACK")
    subprocess.run([ "dslazy.bat", "PACK", "out.nds" ])
    # os.rename("NDS_UNPACK", folder)
    folder = sys.argv[1].split("\\")[-1][0:-4]
    subprocess.run([ "xdelta3-3.0.11-x86_64.exe", "-e", "-f", "-s", folder + ".nds", "out.nds", "out.xdelta" ])
    psg.popup("You can now play out.nds!", font = "-size 12")