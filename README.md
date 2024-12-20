# Fossil-Fighters-Graphics-Editor
You MUST put the ROM in the same folder as the exe, or it won't work.

This is just a nice tool to make editing Fossil Fighters graphics easy. All you have to do is drag your ROM onto start.exe, and the code
will split it apart and convert the graphics. The converted files can then be edited with NitroPaint, provided here for convenience. When
you are done, you just drag your ROM onto start.exe again, and as long as the three folders it made are still there, it will rebuild you
a new ROM. Due to how ndstool works, this new ROM will aways be smaller than the original.

To download this, if you are confused, press the Green "Code" button in the top right, then choose "Download ZIP".

Furthermore, this is only designed for Windows. For Mac and Linux, I can only point you to WINE: https://www.winehq.org

# Notes
1. None of the graphics have names or anything, they're just numbers. To make things a little easier, however, every directory has a
file named "combo.txt," which lists all of the non-arc files in motion and image, along with what sprites and palettes they use. You can
thus match things up this way, but remember the golden rule: if you can't tell what it is, don't mess with it.

2. For additional help, you can now run openNP.exe, which lets you open all the files for a given bin file at once.

3. If you are planning on creating your own graphics using NitroPaint's "Create BG" feature, make sure to uncheck the "Compress"
button in the import menu, or it will not appear properly in-game.

4. If the graphics you see in NitroPaint look correct, but scrambled, try changing the value of the "Width" drop-down menu under
the image. If it looks to be totally gibberish, first try checking or unchecking the "8bpp" option.

# Source Codes
- NitroPaint: https://github.com/Garhoogin/NitroPaint
- FFTool: https://github.com/jianmingyong/Fossil-Fighters-Tool
- NDSTool: https://github.com/devkitPro/ndstool (this is a later version; the one used here came without a license as part of DSLazy)
- xdelta: https://github.com/jmacd/xdelta-gpl
