        if (os.path.exists(folder + "2") == False):
            psg.popup("There is no folder to build from!")
        else:
            layout = [[psg.Text("Please drag and drop " + folder + ".bin onto HackedNitroPaint.exe.\n\
Press OK if prompted, then close the grey window, then close this.")]]
            window = psg.Window("", layout, grab_anywhere = True, font = "-size 12")
            while True:
                event, values = window.read()
                if (event == psg.WINDOW_CLOSED) or (event == "Quit"):
                    break
            window.close()
            try:
                os.remove(folder + "2" + "/data/BP/Entities.ebp")
            except FileNotFoundError:
                pass
            os.rename("testC.bin", folder + "2" + "/data/BP/Entities.ebp")
            os.rename(folder + "2", "NDS_UNPACK")
            subprocess.run([ "dslazy.bat", "PACK", folder + "2" + ".nds" ])
            os.rename("NDS_UNPACK", folder + "2")
            subprocess.run([ "xdelta3-3.0.11-x86_64.exe", "-e", "-s", folder + ".nds", folder + "2" + ".nds", folder + "2" + ".xdelta" ])