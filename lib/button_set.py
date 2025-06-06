# SPDX-FileCopyrightText: 2025 Brent Goode
# SPDX-License-Identifier: MIT

"""
ButtonSet.py 2025-06-02 v 1.0

Author: Brent Goode

Class libraries for ButtonSet and FunctionButton objects

"""

import button_action_fns
from picovector import PicoVector, Polygon
from touch import Button
from pngdec import PNG
from utils import color_converter

class ButtonSet:
    """A collection of FunctionButton objects with addresses and dynamically calculated sizes"""
    current_page = 0
    max_page = 0
    min_page = 0
    needs_redrawing = False
    buttons = {}

    def __init__(self,
                 buttons_defs: list[dict] | None = None,
                 board_obj: None = None,
                 margin_ratio: float | None = 0.1,
                 default_color: str | list | tuple | None = 'white',
                 background_color: str | list | tuple | None = 'black',
                 default_font: str | None = None,
                 corner_radius: int | None = None,
                 **kwargs):
        """
        """

        self.ButtonSet: dict | None = None
        self.board_obj = board_obj
        self.display = board_obj.display
        
        button_action_fns.board_obj = board_obj
        button_action_fns.ButtonSet = ButtonSet
        
        button_action_fns.initialize_other_vars(kwargs)
        
        display_width, display_height = self.display.get_bounds()
        
        if background_color:
            self.background_color = background_color
        else:
            self.background_color = "black"
            
        if buttons_defs:
            buttons_seen = {}
            self.ButtonSet = {}

            for item in buttons_defs:
                address = (item['page'],item['row'],item['column'])
                if item['page'] not in buttons_seen:
                    buttons_seen[item['page']] = {}
                if item['row'] not in buttons_seen[item['page']]:
                    buttons_seen[item['page']][item['row']] = {}
                buttons_seen[item['page']][item['row']][item['column']] = item
                if item['page'] > ButtonSet.max_page:
                    ButtonSet.max_page = item['page']
                if item['page'] < ButtonSet.min_page:
                    ButtonSet.min_page = item['page']
            
            for page in buttons_seen:
                n = len(buttons_seen[page])
                button_height = display_height/(n + margin_ratio*n + margin_ratio)
                gap = button_height * margin_ratio
                if not corner_radius:
                    corner_radius = gap
                for row in buttons_seen[page]:
                    m = len(buttons_seen[page][row])
                    button_width = (display_width - (m+1)*gap)/m
                    for column in buttons_seen[page][row]:
                        address = (page,row,column)
                        this_buttons_info = buttons_seen[page][row][column]
                        self.ButtonSet[address] = FunctionButton(gap*(column+1)+column*button_width,
                                                                  gap*(row+1)+row*button_height,
                                                                  button_width,
                                                                  button_height,
                                                                  address,
                                                                  board_obj,
                                                                  this_buttons_info.get('name'),
                                                                  corner_radius,
                                                                  this_buttons_info.get('label'),
                                                                  default_font,
                                                                  this_buttons_info.get('label_font'),
                                                                  default_color,
                                                                  this_buttons_info.get('color'),
                                                                  this_buttons_info.get('outline_color'),
                                                                  this_buttons_info.get('label_color'),
                                                                  this_buttons_info.get('symbol'),
                                                                  this_buttons_info.get('fn'),
                                                                  this_buttons_info.get('arg'))
        ButtonSet.buttons = self.ButtonSet
        
    def touch_to_button_address(self) -> tuple | None:
        """
        Converts a touch on the screen to the button address tuple
        or None if touch outside all buttons
        Args:
            None
        Returns:
             address tuple with page, row, and column of the button pressed
        """
        for button in self.get_current_page():
            if button.just_pressed():
                return button.address
        return None

    def run_addressed_button(self, address:tuple):
        """
        Triggers the action tied to the button at the address given as an input
        Args:
            address: the address tuple (page, row, and column) for the button
        Returns:
            whatever the triggered function returns
        """
        if self.ButtonSet[address].fn:
            if list is type(button.arg):
                return self.ButtonSet[address].fn(*self.ButtonSet[address].arg)
            else:
                return self.ButtonSet[address].fn(self.ButtonSet[address].arg)

    def touch_to_action(self) -> None:
        """
        Triggers the action tied to the button that was touched
        Args:
            None
        Returns:
            whatever the triggered function returns
        """
        button_address = None
        for button in self.get_current_page():
            if button.just_pressed():
                if button.fn:
                    if list is type(button.arg):
                        return button.fn(*button.arg)
                    else:
                        return button.fn(button.arg)
    
    def get_button_obj(address):
        """
        Returns the FunctionButton object at address to allow another function to modify it
        Args:
            address: a tuple with three integers giving page, row, and column
        Returns:
            a FunctionButton object or None
        """
        return ButtonSet.buttons.get(address)

    def get_a_page(self,page_number: int) -> list:
        """
        Returns a list of FunctionButton objects that are all the button on the page given as an input
        Args:
            page_number: the int page number whose buttons are to be returned
        Returns:
            a list of FunctionButton objects
        """
        return_list = []
        for button in self.ButtonSet:
            if button[0] == page_number:
                return_list.append(self.ButtonSet[button])
        return return_list

    def get_current_page(self) -> list:
        """
        Returns a list of FunctionButton objects that are all the button on the current page
            Returns: a list of FunctionButton objects
        """
        return_list = []
        for button in self.ButtonSet:
            if button[0] == ButtonSet.current_page:
                return_list.append(self.ButtonSet[button])
        return return_list

    def redraw_page(self):
        self.display.set_pen(self.display.create_pen(*color_converter(self.background_color)))
        self.display.clear()
        current_page = self.get_current_page()
        for button in current_page:
            button.draw_button()
        self.board_obj.update()

class FunctionButton(Button):
    """ An extension to the Button class to link a button to a function,
        draw a rounded rectangle, add text, and add an image"""

    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 address: tuple,
                 board_obj,
                 name: str | None = None,
                 radius: int = 0,
                 label: str | None = None,
                 default_font: str | None = None,
                 label_font: str | None = None,
                 default_color: str | tuple | list | None = 'white',
                 color: str | tuple | list | None = None,
                 outline_color: str | tuple | list | None = None,
                 label_color: str | tuple | list | None = None,
                 symbol: str | None = None,
                 fn_name: str | None = None,
                 arg: str | None = None,
                 **kwargs):
        """
        """
        super().__init__(x, y, width, height)

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.radius = radius
        self.address = address
        self.board_obj = board_obj
        self.display = board_obj.display
        self.touch = board_obj.touch
        self.fn_name = fn_name
        self.arg = arg
        self.label = label
        self.depressed = False

        if label_font:
            self.label_font = f'/art/{label_font}'
        elif default_font:
            self.label_font = f'/art/{default_font}'
        else:
            self.label_font = None
        
        try:
            open(self.label_font)
        except Exception as exc:
            print(f"No font file called {self.label_font} found.")
            print(exc)
            self.label_font = None
            
        
        if outline_color:
            self.outline_color = self.display.create_pen(*color_converter(outline_color))
        elif color:
            self.outline_color = self.display.create_pen(*color_converter(color))
        else:
            self.outline_color = self.display.create_pen(*color_converter(default_color)
            )
        
        if label_color:
            self.label_color = self.display.create_pen(*color_converter(label_color))
        elif color:
            self.label_color = self.display.create_pen(*color_converter(color))
        else:
            self.outline_color = self.display.create_pen(*color_converter(default_color))
        
        if symbol:
            self.symbol_path = f'/art/{symbol}'
        else:
            self.symbol_path = None

        if fn_name:
            try:
                self.fn = getattr(button_action_fns,fn_name)
            except:
                try:
                    self.fn = getattr(ButtonSet,fn_name)
                except Exception as exc:
                    print(f'There is no function named {fn_name}.')
                    print(exc)
                    self.fn = None
        else:
            self.fn = None

    def draw_button(self):
        """Draws the elements of a Function button with correctly scaled symbol and text"""
        vector = PicoVector(self.display)
        if self.symbol_path:
            png = PNG(self.display)
            try:
                png.open_file(self.symbol_path)
                png.decode(int(self.x+0.5*self.width-0.5*png.get_width()), int(self.y+0.5*self.height-0.5*png.get_height()))
            except Exception as exc:
                print(f"No image file called {self.symbol_path} found.")
                print(exc)
            
        if self.label:
            self.display.set_pen(self.label_color)
            if self.label_font:
                vector.set_font(self.label_font, int(0.33*self.height))
                text_x, text_y, text_width, text_height = vector.measure_text(self.label)
                if text_width > 0.9*self.width:
                    vector.set_font(self.label_font, int(0.9*self.width/text_width*0.33*self.height))
                    text_x, text_y, text_width, text_height = vector.measure_text(self.label)
                vector.text(self.label, int(self.x+0.5*self.width-text_x-0.5*text_width), int(self.y+0.5*self.height+text_y+0.5*text_height))
            else:
                self.board_obj.display.text(self.label, int(self.x+5), int(self.y+0.5*self.height-5), int(self.width-10),3)
        self.display.set_pen(self.outline_color)
        shape = Polygon()
        shape.rectangle(self.x, self.y, self.width, self.height, corners=(self.radius, self.radius, self.radius, self.radius), stroke=3)
        vector.draw(shape)

    def redraw_button(self):
        """Redraws a single button after some aspect of its appearance has been updated"""
        self.draw_button()
        self.board_obj.partial_update(int(self.x)-1, int(self.y)-1, int(self.width)+2, int(self.height)+2)

    def just_pressed(self):
        """Returns True once and only once when a button transitions from not touched to touched"""
        self.touch.poll()
        if self.is_pressed():
            if not self.depressed:
                self.depressed = True
                return True
            else:
                return False
        elif not self.is_pressed():
            self.depressed = False

    def just_released(self):
        """Returns True once and only once when a button transitions from touched to not touched"""
        self.touch.poll()
        if not self.is_pressed():
            if self.depressed:
                self.depressed = False
                return True
            else:
                return False
        elif self.is_pressed():
            self.depressed = True
