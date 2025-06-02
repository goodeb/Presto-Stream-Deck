# SPDX-FileCopyrightText: 2025 Brent Goode
# SPDX-License-Identigier: MIT

"""
button_action_functions.py 2025-06-02 v 1.0

Author: Brent Goode

File containing the functions that are called when a screen button is pressed

"""

from utils import color_converter

def initialize_other_vars(kwargs):
    """"""
    other_vars = kwargs.get('other_vars')
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
    r,g,b = color_converter(color)
    for i in range(7):
        board_obj.set_led_rgb(i,r,g,b)

def sound_buzzer(tone: int,*arg):
    buzzer.set_tone(tone)

def add_one_to_label(address,*arg):
    address = tuple([int(i) for i in address.split(',')])
    this_button = ButtonSet.get_button_obj(address)
    this_button.label = str(int(this_button.label)+1)
    this_button.redraw_button()
    
def add_amount_to_label(address,amount,*arg):
    address = tuple([int(i) for i in address.split(',')])
    this_button = ButtonSet.get_button_obj(address)
    this_button.label = str(int(this_button.label)+amount)
    this_button.redraw_button()

def set_label(address,number,*arg):
    address = tuple([int(i) for i in address.split(',')])
    this_button = ButtonSet.get_button_obj(address)
    this_button.label = str(number)
    this_button.redraw_button()
