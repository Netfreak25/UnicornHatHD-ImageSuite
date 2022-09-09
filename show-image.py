#!/usr/bin/env python

import signal
import time
from sys import exit
import sys, getopt
from PIL import Image
import numpy as np

try:
    from PIL import Image
except ImportError:
    exit("This script requires the pillow module\nInstall with: sudo pip install pillow")

try:
    import unicornhathd
except ImportError:
    print("no unicorn hat hd detected - using simulator")
    try:
        from unicorn_hat_sim import unicornhathd
    except ImportError:
        print("no unicorn hat hd simulator found - exiting now")
        print("You need to install at least a Simulator (unicorn_hat_sim) or the Libraries (unicornhathd)")


# default values for animations
pulseamount = 3
blinkamount = 6
spinamount = 3
zoomloop = 1
animationamount = 1

animation_sleep = 0.05


rotation = 0
brightness = 1

# initialization of booleans
myfile = False
blink = False
spin = False
pulse = False
fun = False
zoomin = False
zoomout = False
zoom = False
loop = False
colorize = False
demo = False
filechoosen = False


true_array = ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']
help_text = """This is a Python Image Suite for Pimoroni Unicorn HD

This is based on the original show-png.py example from Pimoroni

It can be used to display images on the Unicorn HD. If the Image is to big it will be automatically resized to 16x16 pixel, but it won't take care of aspect ratio.
So for best results make sure you have already adjusted your Image to 16x16 pixels. You can choose between multiple effects, if you don't choose a effect you will get a static picture!
GIF animations will be played automatically, but will stop after one turn.


Usage:
./show-png.py --file /path/file.png

--blink True           Let the image blink
--spin False           Spin the Image
--pulse False           Let the image pulse
--zoomin False         Zoom into the Image
--zoomout False        Zoom out of the Image
--zoom False           Zoom In and Out of the Image
--fun False            Move the outter border od the Image

--loop                 Loops the animation (Blink/Pulse/Spin/Zoom)
                       If you provide gif animation it will be played in a loop
--colorize 255,0,0     Colorizes the image before showing
--animationsleep 0.1   Set the sleep time between animation frames

--demo False           Shows all animations with attached palm.png"""
demo_text = "To get a demo use the '--demo True' parameter"


try:
   try:
      argv = sys.argv[1:]
      opts, args = getopt.getopt(argv,"hi:o:",["file=","blink=","spin=","pulse=","zoomin=","fun=","zoomout=","zoom=","demo=","loop=","colorize=","animationsleep=","rotation="])
   except getopt.GetoptError as e2:
      print(help_text)
      print(demo_text)
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print(help_text)
         sys.exit()
      if opt in ("-f", "--file"):
         filechoosen = True
         myfile = str(arg)
      if opt in ("-b", "--blink"):
         blink = str(arg).lower() in true_array
      if opt in ("-l", "--loop"):
         loop = str(arg).lower() in true_array
      if opt in ("-s", "--spin"):
         spin = str(arg).lower() in true_array
      if opt in ("-p", "--pulse"):
         pulse = str(arg).lower() in true_array
      if opt in ("-ff", "--fun"):
         fun = str(arg).lower() in true_array
      if opt in ("-zi", "--zoomin"):
         zoomin = str(arg).lower() in true_array
      if opt in ("-zo", "--zoomout"):
         zoomout = str(arg).lower() in true_array
      if opt in ("-z", "--zoom"):
         zoom = str(arg).lower() in true_array
      if opt in ("-c", "--colorize"):
         colorize = str(arg).lower()
      if opt in ("-a", "--animationsleep"):
         animation_sleep = float(arg)
      if opt in ("-r", "--rotation"):
         rotation = int(arg)
      if opt in ("-d", "--demo"):
         demo = str(arg).lower() in true_array
except Exception as e:
    print(e)


unicornhathd.rotation(rotation)
unicornhathd.brightness(brightness)


if demo == True:
    filechoosen = True
    myfile = "./palm.png"
    blink = True
    spin = True
    pulse = True
    fun = True
    zoomin = True
    zoomout = True
    zoom = True

if not filechoosen:
    print("Error: You need to select a file via --file")
    print("")
    print(help_text)
    print(demo_text)
    sys.exit(2)

width, height = unicornhathd.get_shape()

img = Image.open(myfile)
mypalette = img.getpalette()
pwidth, pheight = img.size


# automatically resize image to 16x16 pixel as more makes no sense and does not work

if pwidth > 16:
    img = img.resize((16,16))


# try to convert image 
try:
    img = img.convert('RGBA')
except Exception as e:
    print(e)
    pass


def showit(theimg = img, newr = 0, newg = 0, newb = 0):
    try:
        for x in range(width):
            for y in range(height):
                pixel = theimg.getpixel((y,x))

                r,g,b,a = pixel[0],pixel[1],pixel[2],pixel[3]


                try:
                    if int(a) == 0:
                       r,g,b = 0,0,0
                except Exception as e:
                    pass

                if (newr != 0) or (newg != 0) or (newb != 0):
                    try:
                        if int(a) != 0:
                           r,g,b = newr,newg,newb
                    except Exception as e:
                        pass


                try:
                    if r or g or b:
                        valid = True
                        unicornhathd.set_pixel(x, y, r, g, b)
                except Exception as e:
                    pass
                print("")
        unicornhathd.show()
    except Exception as e:
        pass


newr = 0
newg = 0
newb = 0

if colorize != False:
    newr = int(colorize.split(",")[0].strip())
    newg = int(colorize.split(",")[1].strip())
    newb = int(colorize.split(",")[2].strip())

def deleteit():
    if blink == True:
        time.sleep(0.2)
        for x in range(0,width):
            for y in range(0,height):
                r, g, b = 0, 0, 0
                unicornhathd.set_pixel(x, y, r, g, b)
                unicornhathd.set_pixel(x, y, r, g, b)
        unicornhathd.show()
        time.sleep(0.2)

def blank():
    for x in range(0,width):
        for y in range(0,height):
            r, g, b = 0, 0, 0
            unicornhathd.set_pixel(x, y, r, g, b)
            unicornhathd.set_pixel(x, y, r, g, b)



def analyseImage(path):
    im = Image.open(path)
    results = {
        'size': im.size,
        'mode': 'full',
    }
    try:
        while True:
            im.seek(im.tell() + 1)
    except EOFError:
        pass
    return results



showed = False
try:
    if zoomin == True:
        unicornhathd.brightness(brightness)
        blank()
        showed = True
        original_image = img
        for i in range(1,16):

            blank()
            layer = original_image.resize((i,i))

            img_w, img_h = layer.size
            background = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
            bg_w, bg_h = background.size
            offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
            background.paste(layer, offset)
            img = background
            showit(img, newr, newg, newb)
        img = original_image
        blank()
        showit(img, newr, newg, newb)

    if blink == True:
        unicornhathd.brightness(brightness)

        blank()
        showed = True
        myi = 0
        while ((myi <= blinkamount) or loop):
            showit(img, newr, newg, newb)
            time.sleep(0.2)
            deleteit()
            myi += 1
        showit(img, newr, newg, newb)
        time.sleep(0.3)
    if pulse == True:
        blank()
        showed = True
        myi = 0
        while ((myi <= pulseamount) or loop):
            time.sleep(0.05)
            for i in range (10,2,-1):
                value = "0."+str(i)
                if value == "0.10":
                    value = "1"
                value = float (value)
                unicornhathd.brightness(value)
                showit(img, newr, newg, newb)
                time.sleep(0.04)

            time.sleep(0.05)
            for i in range (2,10,1):
                value = "0."+str(i)
                if value == "0.10":
                    value = "1"
                value = float (value)
                unicornhathd.brightness(value)
                showit(img, newr, newg, newb)
                time.sleep(0.04)
            myi += 1
    if spin == True:
        unicornhathd.brightness(brightness)
        blank()
        amount = 0
        showed = True
        while ((amount <= spinamount) or loop):
            for i in range(0,360,12):
                blank()
                newimg = Image.open(myfile)
                img =  newimg.rotate(i, Image.NEAREST)

                try:
                    img = img.convert('RGBA')
                except:
                    pass
                showit(img, newr, newg, newb)
            amount += 1
        blank()
        newimg = Image.open(myfile)
        img =  newimg
        try:
            img = img.convert('RGBA')
        except:
            pass

        showit(img, newr, newg, newb)

    if fun == True:
        unicornhathd.brightness(brightness)
        blank()
        showed = True
        original_image = img
        for i in range(0,480,5):
            # Calls the function to rotate the image by given angle
            img =  img.rotate(5)
            blank()
            showit(img, newr, newg, newb)
            time.sleep(0.02)
        blank()
        img = original_image
        showit(img, newr, newg, newb)

    if zoomout == True:
        unicornhathd.brightness(brightness)
        blank()
        showed = True
        original_image = img
        for i in range(16,0,-1):
            blank()
            layer = original_image.resize((i,i))

            img_w, img_h = layer.size
            background = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
            bg_w, bg_h = background.size
            offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
            background.paste(layer, offset)
            img = background
            showit(img, newr, newg, newb)

        blank()
        background = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
        img = background
        showit(img, newr, newg, newb)
        img = original_image

    if zoom == True:
        myloop = 0
        while ((myloop <= spinamount) or loop):
            unicornhathd.brightness(brightness)

            blank()
            showed = True
            original_image = img
            for i in range(1,16):
                blank()
                layer = original_image.resize((i,i))

                img_w, img_h = layer.size
                background = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
                bg_w, bg_h = background.size
                offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
                background.paste(layer, offset)
                img = background
                showit(img, newr, newg, newb)
            img = original_image
            blank()
            showit(img, newr, newg, newb)

            time.sleep(0.2)

            unicornhathd.brightness(brightness)
            showed = True
            for i in range(16,0,-1):
                blank()
                layer = original_image.resize((i,i))

                img_w, img_h = layer.size
                background = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
                bg_w, bg_h = background.size
                offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
                background.paste(layer, offset)
                img = background
                showit(img, newr, newg, newb)
            myloop += 1

            blank()
            background = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
            img = background
            showit(img, newr, newg, newb)
            img = original_image

    if showed == False:
        blank()
        showed = True
        animated = True

        mode = analyseImage(myfile)['mode']
        im = Image.open(myfile)

        i = 0
        p = im.getpalette()
        last_frame = im.convert('RGBA')

        myloop = 1
        while ((myloop <= animationamount) or loop):
            try:
                im.seek(0)
                myloop += 1
                while True:
                    new_frame = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
                    new_frame.paste(im, (0,0), im.convert('RGBA'))
                    blank()
                    showit(new_frame, newr, newg, newb)
                    i += 1
                    last_frame = new_frame
                    time.sleep(animation_sleep)
                    im.seek(im.tell() + 1)
            except Exception as e3:
                print(e3)
                pass
        showit(new_frame, newr, newg, newb)



except KeyboardInterrupt:
    unicornhathd.off()
