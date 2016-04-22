#!/usr/bin/env python3
import time
import argparse
from Xlib import display # python3-xlib
from gi.repository import Gio

def get_cursor_size():
    setting = Gio.Settings.new("org.gnome.desktop.interface");
    return setting.get_int('cursor-size')

def set_cursor_size(cursor_size):
    global current_cursor_size    
    current_cursor_size = cursor_size
    setting = Gio.Settings.new("org.gnome.desktop.interface");
    setting.set_int('cursor-size',  cursor_size)

def get_mouse_position():
    qp = display.Display().screen().root.query_pointer()
    return [qp.root_x, qp.root_y]

parser = argparse.ArgumentParser(description='Magnify mouse cursor if mouse is shaken.')
parser.add_argument('--debug', help='Pring debug data during program execution', action="store_true")
args = parser.parse_args()

is_debug_on = 0

if args.debug:
    is_debug_on = 1
    
original_cursor_size = get_cursor_size()
max_cursor_size = 48
current_cursor_size = original_cursor_size

previous_pos = get_mouse_position()

xDeltas = []
yDeltas = []

try:
    while True:
        time.sleep(0.01)
        pos = get_mouse_position()

        if len(xDeltas) > 10:
            xDeltas.pop()

        xDeltas.insert(0, previous_pos[0] - pos[0])

        xSignChangedCount = 0

        prev = xDeltas[0]
        
        for val in xDeltas:
            if val * prev < 0:
                xSignChangedCount = xSignChangedCount + 1

            prev = val

        if is_debug_on:    
            print(str(xSignChangedCount) + ":" + str(current_cursor_size))

        if xSignChangedCount > 1 and current_cursor_size < max_cursor_size:
            set_cursor_size(min(current_cursor_size + 8, max_cursor_size))
        elif xSignChangedCount <= 1 and current_cursor_size > original_cursor_size:
            set_cursor_size(max(current_cursor_size - 8, original_cursor_size))

        previous_pos = pos
except KeyboardInterrupt:
    print('interrupted!')
