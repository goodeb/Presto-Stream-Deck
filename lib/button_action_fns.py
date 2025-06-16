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
    """
    Required setup function for using the ButtonSet class with this script.
    """
    other_vars = kwargs.get('other_vars')
    
    if other_vars.get('buzzer_pin'):
        from presto import Buzzer
        global buzzer
        buzzer = Buzzer(other_vars.pop('buzzer_pin'))
    
    if other_vars:
        for var_name, var_value in other_vars.items():
            globals()[var_name]=var_value

def light_backlight(color: str | list | tuple | None = None) -> None:
    """Lights Presto backlight to the color given by color"""
    r,g,b = color_converter(color)
    for i in range(7):
        board_obj.set_led_rgb(i,r,g,b)

def sound_buzzer(tone: int):
    """
    Sounds the buzzer hardware object
    Args:
        tone: the intensity of the buzzer sound. An int from 0 to 255
    """
    buzzer.set_tone(tone)

def cycle_through_colors(address):
    """
    Cycles the outline color of a button throng the global color_cycle list
    Args:
        address: a comma separated string of three ints with the page, row,
            and column of the button
    """
    address = tuple([int(i) for i in address.split(',')])
    this_button = ButtonSet.get_button_obj(address)
    color_cycle.append(color_cycle.pop(0))
    this_button.outline_color = board_obj.display.create_pen(*color_converter(color_cycle[0]))
    this_button.redraw_button()
    
def add_amount_to_label(address,amount):
    """
    Changes the number label of a button at address by amount and redraws
    Args:
        address: a comma separated string of three ints with the page, row,
            and column of the button
        amount: a signed int of the amount to add to the label
    """
    address = tuple([int(i) for i in address.split(',')])
    this_button = ButtonSet.get_button_obj(address)
    this_button.label = str(int(this_button.label)+amount)
    this_button.redraw_button()

def set_label(address,text):
    """
    Sets the label of a button to be the input text and redraws
    Args:
        address: a comma separated string of three ints with the page, row,
            and column of the button
        text: the new text for the label
    """
    address = tuple([int(i) for i in address.split(',')])
    this_button = ButtonSet.get_button_obj(address)
    this_button.label = str(text)
    this_button.redraw_button()

def http_post(url,query_data):
    """
    Makes a POST request to the give url
    Args:
        url: the web page address to send the request to
        query_data: a dictionary object to send to the url
    """
    try:
        request = urequests.post(url, json = query_data)
    except Exception as exc:
        print(exc)

def http_get(url,query_data):
    """
    Makes a GET request to the give url
    Args:
        url: the web page address to send the request to
        query_data: a dictionary object to send to the url
    Returns:
        the request response object the web page sent
    """
    try:
        request = urequests.get(url, json = query_data)
        result_data = json.loads(request.content.decode("utf-8"))
        print(result_data)
        return result_data
    except Exception as exc:
        print(exc)


