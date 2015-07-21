import os, time, io, re, Queue, threading, subprocess, msvcrt
from optparse import OptionParser,OptionGroup
from ast import literal_eval
from difflib import Differ
from PIL import Image,ImageGrab,ImageOps


def Run(box, timestamp, txtQueue, save):
    if save:
        image = Image.open(SaveScreenshotTime(timestamp))
    else:
        image = GetScreenshot()
    boxImage = GetBoxImage(image, box)
    ConvertImage(boxImage, timestamp, txtQueue)
    #AppendCombatLog(combatTime, txtQueue, first, save)

def SaveScreenshot():
    image = ImageGrab.grab()
    image.save('ddo_ss_single.bmp', dpi=(200, 200))

def SaveScreenshotTime(time):
    ss = 'ddo_ss_' + time + '.bmp'
    image = ImageGrab.grab()
    image.save(ss, dpi=(200, 200))
    return ss

def GetScreenshot():
    image = ImageGrab.grab()
    return image

def SaveBox(coords):
    image = Image.open('ddo_ss_single.bmp')
    region = image.crop(coords)
    region.save('ddo_box_ss_single.bmp', dpi=(200, 200))

def GetBoxImage(image, coords):
    region = image.crop(coords)
    region = ConvertToBW(region)
    return region

def ConvertToBW(image):
    image = image.convert("RGB")
    pixels = image.load()
    for y in xrange(image.size[1]):
        for x in xrange(image.size[0]):
            if pixels[x, y][0] < 80:
                pixels[x, y] = (0, 0, 0, 255)
            if pixels[x, y][1] < 126:
                pixels[x, y] = (0, 0, 0, 255)
            if pixels[x, y][2] > 0:
                pixels[x, y] = (255, 255, 255, 255)
    return image

def ConvertImage(image, time, txtQueue):
    image = image.resize((image.width * 6, image.height * 6), Image.ANTIALIAS)
    regionName = 'ddo_bw_' + time + '.bmp'
    image.save(regionName, dpi=(200,200))
    Tesseract(regionName, "ddo_convert_" + time, txtQueue)

def ConvertAndSaveImage(box_filepath, coords, count):
    image = Image.open(box_filepath)
    image = image.crop(coords)
    image = image.resize((image.width * 6, image.height * 6), Image.ANTIALIAS)
    image = ConvertToBW(image)
    name = 'ddo-ddo_font-exp' + count + '.bmp'
    image.save(name, dpi=(200,200))

def Tesseract(input_filename, output_filename, txtQueue):
    # Call the tesseract.exe file with arguments
    args = ['tesseract.exe', input_filename, output_filename, '-l', 'ddo', '-psm', '6']
    # Use the stderr and stdout to ignore tesseract print statements
    proc = subprocess.Popen(args, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    retcode = proc.wait()
    txtQueue.append(output_filename + ".txt")
    try:
        # Don't want to keep the enlarged box image file since it is pretty big
        os.remove(input_filename)
    except Exception as e:
        print "Couldn't remove temporary files. Check the folder and remove them so they don't take up unneeded space on your harddrive."
        pass

def AppendCombatLog(combatTime, txtQueue, first, save):
    regex = re.compile(r'^\((Combat|Effects)\):.+$', re.IGNORECASE)

    if first[0]:
        if len(txtQueue) > 0:
            with open(txtQueue[0], 'r') as file1:
                initialFile = file1.readlines()

            # Remove junk lines that the OCR failed to parse
            if len(initialFile) > 0 and not regex.match(initialFile[0]):
                initialFile = initialFile[1:]
            # Use list comprehension to remove extra newlines added by OCR
            initialFile = [ x for x in initialFile if not x == '\n' ]

            with open("ddo_combatlog_" + combatTime + ".txt", 'w') as file:
                # Compare the files, get difference deltas
                for line in initialFile:
                    file.write(line)
            first[0] = False
    else:
        if len(txtQueue) >= 2:
            with open(txtQueue[0], 'r') as file1:
                previous = file1.readlines()
            with open(txtQueue[1], 'r') as file2:
                next = file2.readlines()

            # Remove junk lines that the OCR failed to parse
            if len(previous) > 0 and not regex.match(previous[0]):
                previous = previous[1:]
            # Use list comprehension to remove extra newlines added by OCR
            previous = [ x for x in previous if not x == '\n' ]

            # Remove junk lines that the OCR failed to parse
            if len(next) > 0 and not regex.match(next[0]):
                next = next[1:]
            # Use list comprehension to remove extra newlines added by OCR
            next = [ x for x in next if not x == '\n' ]

            with open("ddo_combatlog_" + combatTime + ".txt", 'a') as file:
                # Compare the files, get difference deltas
                for line in Differ().compare(previous, next):
                    # Only want to add the new lines from the next file
                    if line[:2] == "+ ":
                        # Don't want the "+ " identifiers
                        file.write(line[2:])
            if not save:
                try:
                    os.remove(txtQueue[0])
                except Exception as e:
                    print "Couldn't remove text files. Check the folder and remove them so they don't take up unneeded space on your harddrive."
                    pass
            txtQueue.pop(0)

def ProgramOptions():
    parser = OptionParser()
    parser.add_option("-m", "--mode", dest="mode", default="S", help="Mode of operation. Options: S, B, C, F. S - Screenshot mode, B - Box Image mode, C - Conver to BW, F - Full mode. Default: S", type="string", metavar="MODE")
    parser.add_option("-b", "--box", dest="box", default=(0,0,0,0), help="This takes a series of 4 numbers that are the coordinates of the combat log box. (TopLeftCoord,TopRightCoord,BottomRightCoord,BottomLeftCoord)", metavar="COORDS")
    parser.add_option("-i", "--interval", dest="interval", default=2, help="Interval that the program will take screeshots in seconds. Default: 2.", type="int", metavar="TIME")
    parser.add_option("-s", "--savefiles", dest="saveFiles", action="store_true", help="If present, the progam will not delete the images/text it creates.", metavar="FILES")
    parser.add_option("-p", "--picture", dest="pic", help="Image.", metavar="PIC")
    parser.add_option("-c", "--count", dest="count", help="Count.")
    parser.add_option_group(OptionGroup(parser, "Press Escape to exit. Example run:", "python ddo-logger.py -m F -b (0,0,500,800) -i 2 -s"))
    return parser

def main():
    (options, args) = ProgramOptions().parse_args()

    if options.mode == "S":
        SaveScreenshot()
    elif options.mode == "B":
        SaveBox(literal_eval(options.box))
    elif options.mode == "C":
        timestamp = str(int(time.time()))
        ConvertAndSaveImage(options.pic, literal_eval(options.box), options.count)
    elif options.mode == "F":
        first = [True]
        combatTime = str(int(time.time()))
        txtQueue = []
        while True:
            if msvcrt.kbhit():
                if ord(msvcrt.getch()) == 27:
                    if len(txtQueue) > 0:
                        for file in txtQueue:
                            try:
                                os.remove(file)
                            except Exception as e:
                                print "Couldn't remove text files. Check the folder and remove them so they don't take up unneeded space on your harddrive."
                                pass
                        files = [i for i in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(),i)) and 'ddo_bw_' in i]
                        for file in files:
                            try:
                                os.remove(file)
                            except Exception as e:
                                print "Couldn't remove text files. Check the folder and remove them so they don't take up unneeded space on your harddrive."
                                pass
                    break
            AppendCombatLog(combatTime, txtQueue, first, options.saveFiles)
            timestamp = str(int(time.time()))
            thread = threading.Thread(target=Run, args=[literal_eval(options.box), timestamp, txtQueue, options.saveFiles])
            thread.daemon = True
            thread.start()
            #first = False
            time.sleep(options.interval)
    else:
        print("Invalid mode provided.")

if __name__ == '__main__':
    main()
