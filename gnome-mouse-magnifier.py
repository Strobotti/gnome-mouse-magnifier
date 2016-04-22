#!/usr/bin/env python3
import subprocess
import time

def get_cursor_size():
    ret = subprocess.check_output(["gsettings", "get", "org.gnome.desktop.interface", "cursor-size"]).decode("utf-8")
    return int(ret)

def set_cursor_size(cursor_size):
    ret = subprocess.check_output(["gsettings", "set", "org.gnome.desktop.interface", "cursor-size", str(cursor_size)])

def get_mouse_position():
    curr = subprocess.check_output(["xdotool", "getmouselocation"]).decode("utf-8")
    return [int(it.split(":")[1]) for it in curr.split()[:2]]

original_cursor_size = get_cursor_size()
max_cursor_size = original_cursor_size * 3

previous_pos = get_mouse_position()

xDeltas = []
yDeltas = []

while True:
    time.sleep(0.001)
    pos = get_mouse_position()

    if len(xDeltas) > 6:
        xDeltas.pop()

    if len(yDeltas) > 6:
        yDeltas.pop()

    xDeltas.insert(0, previous_pos[0] - pos[0])
    yDeltas.insert(0, previous_pos[1] - pos[1])

    xSignChangedCount = 0

    prev = xDeltas[0]
    
    for val in xDeltas:
        if val * prev < 0:
            xSignChangedCount = xSignChangedCount + 1
        
    #print(str(xSignChangedCount))

    if xSignChangedCount > 1 and get_cursor_size() < max_cursor_size:
        set_cursor_size(get_cursor_size() + 6)
    elif xSignChangedCount < 2 and get_cursor_size() > original_cursor_size:
        set_cursor_size(get_cursor_size() - 6)

    previous_pos = pos
