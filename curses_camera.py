#!/usr/bin/env python
import sys,os
import curses

try:
    from picamera import PiCamera
except ImportError:
    exit('This script requires the picamera module\nInstall with: sudo pip install picamera')

try:
    from PIL import Image
except ImportError:
    exit('This script requires the pillow module\nInstall with: sudo pip install pillow')

class CameraOutput():
    def __init__(self, stdscr, camera):
        self.stdscr = stdscr

        # Clear and refresh the screen for a blank canvas
        self.stdscr.clear()
        self.stdscr.refresh()
        # self.stdscr.nodelay(True)

    def start(self):
        k = 0

        while (k != ord('q')):
            k = self.stdscr.getch()

    def write(self, buf):
        img = Image.frombytes('RGB', (256, 256), buf)
        img = img.resize((128, 64), Image.BILINEAR)

        pixels = [ord('@'), ord('%'), ord('#'), ord('*'), ord('+'),  ord('='), ord('-'), ord(':'), ord('.'), ord(' ')]

        for x in range(128):
            for y in range(64):
                r, g, b = img.getpixel((x, y))
                i = 0.2125 * r + 0.7154 * g + 0.0721 * b
                self.stdscr.addch(y, x, pixels[int(i) / 26])
                # self.stdscr.addstr(y, x, "x")


        # Refresh the screen
        self.stdscr.refresh()

def main(stdscr):

    with PiCamera() as camera:
        
        camera.resolution = (256, 256)
        camera.contrast = 10 # 50
        camera.rotation = 270
        camera.start_preview()


        camOut = CameraOutput(stdscr, camera)
        camera.start_recording(camOut, 'rgb')

        try:
            camOut.start()

        finally:
            camera.stop_recording()

if __name__ == "__main__":
    curses.wrapper(main)
