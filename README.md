# UnicornHatHD-ImageSuite

![Python 2.7](https://img.shields.io/badge/python-2.7-blue.svg)

This is a Python Image Suite for Pimoroni Unicorn HD

This is based on the original show-png.py example from Pimoroni

It can be used to display images on the Unicorn HD. If the Image is to big it will be automatically resized to 16x16 pixel, but it won't take care of aspect ratio.
So for best results make sure you have already adjusted your Image to 16x16 pixels. You can choose between multiple effects, if you don't choose a effect you will get a static picture!
GIF animations will be played automatically, but will stop after one turn.

Tested with: png, gif, ico

## Usage:

```
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

--demo False           Shows all animations with attached palm.png
```

## Installation:
* Install pip and git
```
apt-get install python-pip git
```
* Clone the Project
```
git clone https://github.com/Netfreak25/UnicornHatHD-ImageSuite.git
```
* Install python libraries
```
pip install numpy pillow
```
