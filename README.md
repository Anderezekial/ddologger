# ddologger
A logger for the DDO MMO combat log

## Pre-requisites
- Python 2.7 - https://www.python.org/downloads/
- Pillow
- An image manipulation tool to get pixels. I used Paint.NET - http://www.getpaint.net/index.html
- Tesseract - I used version 3.02.02 -  https://code.google.com/p/tesseract-ocr/downloads/detail?name=tesseract-ocr-setup-3.02.02.exe&can=2&q=

## Setup
- Install Python
- Install Pillow
```
pip install Pillow
```
- Install Paint.NET
- Create a folder for everything to live in, such as: `C:\Users\User\Documents\ddologger`
- Install Tesseract. Install it to your created folder.
- Put the `ddo-logger.py` file in the created folder
- Put the `ddo.traineddata` file inside the `tessdata` folder

## Prep Work

*You should redo this section any time you move your screen (if windowed) or move your Combat window*

- Open up a command line. `cmd.exe` or find the `Command Prompt`
- Navigate to the created folder.
```
C:\ cd C:\Users\User\Documents\ddologger
```
- Open up DDO. Log in and get on your character. Either focus to your Combat tab or pull your Combat tab out to its own window.
- ALT-TAB if in Fullscreen.
- Focus the Command prompt and run:
```
C:\Users\User\Documents\ddologger python ddo-logger.py -m S
```
- This will create a file called `ddo_ss_single.bmp` in the folder.
- Open up the `ddo_ss_single.bmp` file in Paint.NET
  - I choose the `Color Picker` tool, so I don't mess anything up.
  - Hover over the top-left corner of the Combat window. Write down the coordinates, ex: 95,458
  - Hover over the bottom-right corner of the Combat window. Write down the coordinates, ex: 602,758
- We now have our box coordinates by combining the two sets: (95,458,602,758)
- Focus back to the Command prompt and run:
```
C:\Users\User\Documents\ddologger python ddo-logger.py -m B -b (95,458,602,758)
```
  - *MAKE SURE TO NOT PUT ANY SPACES IN THE COORDINATES*
- This will create an image called `ddo_box_ss_single.bmp` in the folder.
  - Open this image in Paint.NET and see if it correctly gets all of the Combat window
    - If not, bump around the coordinate numbers and rerun the command till you get the correct image

## Executing

Once we have the correct coordinates, we just need to run the program while we play
```
C:\Users\User\Documents\ddologger python ddo-logger.py -m F -b (95,458,602,758)
```

### Development

Here are my notes for what I did to create this for those that are interested.

If you want, you can add the optional `-s` flag, which will save the screenshots (not all images) and text files generated so you can see what is going on.
- *WARNING* - This will take up alot of space on your harddrive. For me, it was about 180MB per minute.

Training Tesseract

- Got the jTessBoxEditor. Any of the editors will do, just need to be able to fix the mappings.
  - http://vietocr.sourceforge.net/training.html
- I tested saving as .png and .bmp files. Going to go with .bmp, though not sure which is best to use.
- Took the box coordinates images, since that is all I really care about from the screenshots.
- Convert images to just White Text on Black background
- Resize the image to be 6 times as big. This seemed to be the sweet spot where Tesseract read the font the best while not going overboard on size.
- Renamed my 3 test images to `ddo-ddo_font-expX.bmp`, with X being 1,2,3
- Ran for all 3
```
tesseract.exe ddo-ddo_font-expX.bmp ddo-ddo_font-expX batch.nochop makebox
```
  - Didn't do it, but should for future cases. Refer to the Tip #1 in the resolverdiologic link.
- Opened up each .bmp in the jTessBoxEditor. Manually fixed any issues, such as doing 'Split' and 'Merge' to get correct character reads. Also selected a ton of boxes at the top and did 'Delete' to get rid of the junk mapping for the chopped off data.
  - Since the .bmp and .box files are named the same, this is how jTessBoxEditor opens it correctly
- Saved the newly edited .box files
- Ran for all 3
```
tesseract.exe ddo-ddo_font-expX.bmp ddo-ddo_font-expX nobatch box.train
```
- Need to open up all the generated `.tr` files, find the `UnknownFont` entries and do a Replace All with `ddo_font`, otherwise the other tools break because I am using `ddo_font`
- Ran 
```
unicharset_extractor.exe ddo-ddo_font-exp1.box ddo-ddo_font-exp2.box ddo-ddo_font-exp3.box
```
- Take a look at the generated `unicharset` file. Look for any strange characters, that means you missed something in one of the .box files. Go back and fix, then rerun everything.
- Made the `font_properties` file and put `ddo_font 0 0 0 0 0` in it
  - Need to make a file without an extension. I just created a new `.txt` file and did a `Rename`, removing the `.txt` extension
- Ran 
```
shapeclustering.exe -F font_properties -U unicharset ddo-ddo_font-exp1.tr ddo-ddo_font-exp2.tr ddo-ddo_font-exp3.tr
```
- Ran 
```
mftraining -F font_properties -U unicharset -O tla.unicharset ddo-ddo_font-exp1.tr ddo-ddo_font-exp2.tr ddo-ddo_font-exp3.tr
```
- Ran 
```
cntraining ddo-ddo_font-exp1.tr ddo-ddo_font-exp2.tr ddo-ddo_font-exp3.tr
```
- Ran 
```
move inttemp ddo.inttemp
move normproto ddo.normproto
move pffmtable ddo.pffmtable
move shapetable ddo.shapetable
```
- Ran 
```
combine_tessdata ddo.
```
  - *Don’t forget the period at the end of the line!*
- Copy the `ddo.trainneddata` file into the `tessdata` folder

Tesseract should now be trained.

- Run 
```
tesseract.exe ddo-ddo_font-expX.bmp ddo-ddo_font-expX -l ddo -psm 6
``` 
- This generates the `ddo-ddo_font-expX.txt` file.
  - Need to use the `-psm 6` command argument to have it treat the text as a block instead of columns due to the consistent (Combat) style entries at the beginning of each line

### Reference
This tutorial helped me a ton - http://www.resolveradiologic.com/blog/2013/01/15/training-tesseract/
Also this - http://emop.tamu.edu/node/48

