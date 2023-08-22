# Writeup

This challenge consist of 2 parts:
1. Find out the auto save location of Snip & Sketch
2. Image recovery of cropped screen capture, base on aCropalypse (CVE 2023-21036)

## Tool

- Volatility 3
- HxD Editor

## Flow

0. Prepare your symbol table in case. I build the whole challenge on Windows 22H2 and didn't give out the exact Windows build. You can get most of the symbol table [here](https://github.com/JPCERTCC/Windows-Symbol-Tables). If you are using Volatility 2, then you will may difficulties in profile building. But this is not my problem.

1. Extract the files using the command `python3 vol.py -f "Windows 10 x64.dmp" -o ./files/ windows.filescan | tee filescan.log`

Your output should look like this:
```
Volatility 3 Framework 2.4.2

Offset	Name	Size

0x9c8e51b48ef0	\Users\Administrator\AppData\Local\Packages\Microsoft.ScreenSketch_8wekyb3d8bbwe\TempState\{65B9F8B5-5737-41FE-8D6F-F8F6401C5A2A}.jpg	216
0x9c8e51b49850	\Users\Administrator\AppData\Local\Packages\Microsoft.ScreenSketch_8wekyb3d8bbwe\TempState\{65B9F8B5-5737-41FE-8D6F-F8F6401C5A2A}.jpg	216
0x9c8e51b577c0	\Users\Administrator\AppData\Local\Packages\Microsoft.ScreenSketch_8wekyb3d8bbwe\TempState	216
0x9c8e51b582b0	\Users\Administrator\AppData\Local\Packages\Microsoft.ScreenSketch_8wekyb3d8bbwe\TempState	216
0x9c8e518403a0	\Users\Administrator\AppData\Local\Packages\Microsoft.ScreenSketch_8wekyb3d8bbwe\TempState\{3F2220FC-D10A-4CCD-85E4-2D666B9667CA}.jpg	216
0x9c8e51b419c0	\Users\Administrator\AppData\Local\Packages\Microsoft.ScreenSketch_8wekyb3d8bbwe\TempState\{3F2220FC-D10A-4CCD-85E4-2D666B9667CA}.jpg	216
```

2. As the challenge mentioned the "Autosave" feature of Snip & Sketch, you can directly known where the path is. It should locate under `%LocalAppData%\Packages\Microsoft.ScreenSketch_8wekyb3d8bbwe\TempState\`. That's why you can target the 4 JPG files in a short time.

Note: Windows 10 21H2 was being used for this challenge. The autosave location has been changed to `%LocalAppData%\Packages\Microsoft.Windows.ShellExperienceHost_cw5n1h2txyewy\TempState\ScreenClip` in Windows 10 22H2.

3. Dump all the images out:
```
python3 vol.py -f "Windows 10 x64.dmp" -o ./files/ windows.dumpfiles --virtaddr 0x9c8e51b419c0
python3 vol.py -f "Windows 10 x64.dmp" -o ./files/ windows.dumpfiles --virtaddr 0x9c8e51b48ef0
```

4. When you compare the 2 images, you can see that both images have similar file size but different resolution. It is due to a bug in Snip & Sketch in Windows 10 and Snipping Tools in Windows 11. Which matches the title "Extrapolation".

5. Image recovery on `{3F2220FC-D10A-4CCD-85E4-2D666B9667CA}.jpg`, use HxD for help:
- Remove the first "FFD9", this represent end of file in JPEG and interpreter will stop to render the image.
- Copy the file header found on `{65B9F8B5-5737-41FE-8D6F-F8F6401C5A2A}.jpg `. This is the reason why I give out an reference image. The header contains information on image resolution.

Before:
- [](./img/001.png)
- [](./img/002.png)

After:
- [](./img/003.png)
- [](./img/004.png)

6. Profit
[](./img/005.png)

## Epilogue

The PNG chunk recovery is not successful so I change the challenge into JPG. JPG format will be easier to recover.

There's a twitter suggest using <https://jpg.repair/> for JPG recovery but it does not succeed.

The CVE was found on Pixel 7 at first. But it also appears on Windows with a different cause.

## Reference
- <https://www.tomshardware.com/news/bug-makes-windows-11-snipping-tool-images-recoverable-after-editing>
- <https://acropalypse.app/>
- <https://www.da.vidbuchanan.co.uk/blog/exploiting-acropalypse.html>
- <https://twitter.com/wdormann/status/1638235267919233024>