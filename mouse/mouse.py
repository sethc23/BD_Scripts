#!/usr/bin/python

#  SEE API SYSTEM


import os

# import sys
# import time
# from Quartz.CoreGraphics import *  # imports all of the top-level symbols in the module
# 
# def mouseEvent(type, posx, posy):
# 	theEvent = CGEventCreateMouseEvent(None, type, (posx, posy), kCGMouseButtonLeft)
# 	CGEventPost(kCGHIDEventTap, theEvent)
# 
# def mousemove(posx, posy):
# 	mouseEvent(kCGEventMouseMoved, posx, posy)
# 
# def mouseclickdn(posx, posy):
# 	mouseEvent(kCGEventLeftMouseDown, posx, posy)
# 
# def mouseclickup(posx, posy):
# 	mouseEvent(kCGEventLeftMouseUp, posx, posy)
# 
# def mousedrag(posx, posy):
#     mouseEvent(kCGEventLeftMouseDragged, posx, posy)
#     ourEvent = CGEventCreate(None)	
#     currentpos = CGEventGetLocation(ourEvent)  # Save current mouse position
#     mouseclickdn(60, 100)
#     mousedrag(60, 300)
#     mouseclickup(60, 300)
#     time.sleep(1)
#     mousemove(int(currentpos.x), int(currentpos.y))  # Restore mouse position

'''
from 
   'cliclick 26 12' will click the apple menu
   'cliclick 50 60 c70 80' will click at 50/60, then Control-click at 70/80
   'cliclick d50 60' will doubleclick at 50/60
   'cliclick dm m' will doubleclick the current mouse location
   'cliclick c500 m' will control-click at x position 500 and
                     the mouse's current y position.
   'cliclick -w 50 26 11 26 33' will open the "About this Mac" panel
   'cliclick -r 26 12' will click the apple menu and, afterwards,
                       restore the initial mouse location.
   'cliclick -q' will print the current mouse location.
'''


def getMousePos():
	return os.system('cliclick -q')

	
def clickMouse():
	x=str(getMousePos())
	
	print x
	cmd = 'cliclick '+x[0]+" "+x[1]
	os.system(cmd)
