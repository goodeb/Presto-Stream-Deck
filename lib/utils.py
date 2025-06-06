# SPDX-FileCopyrightText: 2025 Brent Goode
# SPDX-License-Identifier: MIT

"""
utils.py 2025-06-02 v 1.0

Author: Brent Goode

Utility functions for the stream deck project

"""

import json


def color_converter(color):
    """Takes a variety of color imports and converts them to r,g,b values 
        for use as inputs to Pimoroni pico display.create_pen() method
    """
    if isinstance(color,str):
        if color.lower() == 'black':
            return 0, 0, 0
        elif color.lower() == 'white':
            return 255, 255, 255
        elif color.lower() == 'red':
            return 255, 0, 0
        elif color.lower() == 'green':
            return 0, 255, 0
        elif color.lower() == 'blue':
            return 0, 0, 255
        elif color.lower() == 'yellow':
            return 255, 255, 0
        elif color.lower() == 'magenta':
            return 255, 0, 255
        elif color.lower() == 'aqua':
            return 0, 255, 255
        else:
            print(f'Unknown color: {color}. Defaulting to white.')
            return 255, 255, 255
    elif isinstance(color,tuple) or isinstance(color,list):
        return color[0], color[1], color[2]
    else:
        return 255, 255, 255

def show_message(board_obj,label):
    """Sets the screen of a Pimoroni pico device to show the text given by label.
        Useful for start up or other error messages"""
    board_obj.display.set_pen(board_obj.display.create_pen(*color_converter('black')))
    board_obj.display.clear()
    board_obj.display.set_pen(board_obj.display.create_pen(*color_converter('white')))
    display_width, display_height = board_obj.display.get_bounds()
    board_obj.display.text(label, 5, 10, display_width-10, 6)
    board_obj.update()
 
def connect_wifi(board_obj):
    """Connects a Pimoroni pico device to wifi and handles errors"""
    try:
        wifi = board_obj.connect()
        return wifi
    except ValueError as e:
        while True:
            show_message(e)
    except ImportError as e:
        while True:
            show_message(e)

def read_input_file(json_file):
    """Reads the json input file for a presto-steam-deck project and parses 
        data into the correct form including custom vars for that project"""
    with open(json_file,'r') as file:
        init_data = json.load(file)
        buttons_defs = init_data.pop("buttons_defs")
        margin_ratio = init_data.pop("margin_ratio",0.1)
        background_color = init_data.pop("background_color",None)
        font_file = init_data.pop("font_file",None)
        corner_radius = init_data.pop("corner_radius",None)
        other_vars = init_data
        return buttons_defs, margin_ratio, background_color, font_file, corner_radius, other_vars
