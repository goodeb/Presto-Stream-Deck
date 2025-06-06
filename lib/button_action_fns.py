# SPDX-FileCopyrightText: 2025 Brent Goode
# SPDX-License-Identifier: MIT

"""
button_action_functions.py 2025-06-02 v 1.0

Author: Brent Goode

File containing the functions that are called when a screen button is pressed.
This is how the custom functionality for each set up is implemented

"""

from utils import color_converter
import urequests
import json

def initialize_other_vars(kwargs):
    """"""
    other_vars = kwargs.get('other_vars')
    
    if other_vars.get('buzzer_pin'):
        from presto import Buzzer
        global buzzer
        buzzer = Buzzer(other_vars.pop('buzzer_pin'))
    
    if other_vars:
        for var_name, var_value in other_vars.items():
            globals()[var_name]=var_value

def next_page(*arg):
    """Change the current page to the next page of buttons if possible"""
    if ButtonSet.current_page < ButtonSet.max_page:
        ButtonSet.current_page += 1
        ButtonSet.needs_redrawing = True

def previous_page(*arg):
    """Change the current page to the previous page of buttons if possible"""
    if ButtonSet.current_page > ButtonSet.min_page:
        ButtonSet.current_page -= 1
        ButtonSet.needs_redrawing = True

def jump_to_page(page_number: int,*arg):
    """Change the current page to the page given as an input if possible"""
    if ButtonSet.min_page <= page_number <= ButtonSet.max_page:
        ButtonSet.current_page = page_number
        ButtonSet.needs_redrawing = True

def light_backlight(color: str | list | tuple | None = None,* arg) -> None:
    """Lights Presto backlight to the color given by color"""
    r,g,b = color_converter(color)
    for i in range(7):
        board_obj.set_led_rgb(i,r,g,b)

def sound_buzzer(tone: int,*arg):
    """Sounds the buzzer hardware object"""
    buzzer.set_tone(tone)

def cycle_through_colors(address,*arg):
    address = tuple([int(i) for i in address.split(',')])
    this_button = ButtonSet.get_button_obj(address)
    color_cycle.append(color_cycle.pop(0))
    this_button.outline_color = board_obj.display.create_pen(*color_converter(color_cycle[0]))
    this_button.redraw_button()
    
def add_amount_to_label(address,amount,*arg):
    """Changes the number label of a button at address by amount and redraws"""
    address = tuple([int(i) for i in address.split(',')])
    this_button = ButtonSet.get_button_obj(address)
    this_button.label = str(int(this_button.label)+amount)
    this_button.redraw_button()

def set_label(address,text,*arg):
    """Sets the label of a button to be the input text and redraws"""
    address = tuple([int(i) for i in address.split(',')])
    this_button = ButtonSet.get_button_obj(address)
    this_button.label = str(text)
    this_button.redraw_button()

def http_post(url,query_data,*arg):
    """
    """
    try:
        request = urequests.post(url, json = query_data)
    except Exception as exc:
        print(exc)

def http_get(url,query_data,*arg):
    """
    """
    try:
        request = urequests.get(url, json = query_data)
        result_data = json.loads(request.content.decode("utf-8"))
        print(result_data)
        return result_data
    except Exception as exc:
        print(exc)


