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
    """A collection of FunctionButton objects with addresses and dynamically calculated sizes
    
    Takes a list of dictionaries with button definitions for FunctionButton objects and calculates
    their size and location and instantiates those objects. 
    Provides methods for getting and drawing a page of buttons, changing pages, interacting
    with buttons through touch and direct addressing and retrieving individual button objects
    for external interaction with its attribute. Assumes that another script called button_action_fns.py
    will exists with an initialize_other_vars()function and other action functions for each of the buttons.

    Class Variables
    ---------------
    current_page: int
        Holds the current page of buttons being displayed
    max_page: int
        number of the highest page in the buttons set
    min_page: int
        number of the lowest page in the buttons set
    needs_redrawing: bool
        indicates that the draw_page need to be called
    buttons: dict
        externally accessible copy of te ButtonSet dict
    
    Attributes
    ----------
    ButtonSet: dict
        a dictionary of FunctionButton objects addressed by the tuple of page, row, and column numbers
    board_obj: 
        The Presto class object for the hardware interface
    display:
        The PicoGraphics class object for drawing on the screen
    background_color: str | list | tuple
        The background screen color to be displayed behind buttons

    Methods
    -------
    touch_to_button_address() -> tuple
        returns the address of a button that was just touched
    run_addressed_button(address: tuple)
        triggers the action of the button at address
    touch_to_action()
        triggers the action of the button that was just touched
    get_a_page(page_number: int) -> list
        returns a list of all the FunctionButton objects on page_number
    draw_page()
        clears the screen and draws the buttons on current_page

    Class Functions
    ---------------
    next_page()
        adds one to current page if in range and sets needs_redrawing to True
    previous_page()
        subtracts one to current page if in range and sets needs_redrawing to True
    jump_to_page(page_number: int)
        sets current page to page_number if in range and sets needs_redrawing to True
    """
    current_page = 0
    max_page = 0
    min_page = 0
    needs_redrawing = False
    buttons = {}

    def __init__(self,
                 buttons_defs: list[dict],
                 board_obj,
                 margin_ratio: float | None = 0.1,
                 default_color: str | list | tuple | None = 'white',
                 background_color: str | list | tuple | None = 'black',
                 default_font: str | None = None,
                 corner_radius: int | None = None,
                 **kwargs):
        """Inits ButtonSet with defaults for nonessential attributes."""

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
                        self.ButtonSet[address] = \
                                FunctionButton(gap*(column+1)+column*button_width,
                                               gap*(row+1)+row*button_height,
                                               button_width,
                                               button_height,
                                               address,
                                               board_obj,
                                               this_buttons_info.get('name'),
                                               corner_radius,
                                               this_buttons_info.get('label'),
                                               this_buttons_info.get('label_font',default_font),
                                               this_buttons_info.get('color',default_color),
                                               this_buttons_info.get('outline_color'),
                                               this_buttons_info.get('label_color'),
                                               this_buttons_info.get('symbol'),
                                               this_buttons_info.get('fn_name'),
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
        button = self.ButtonSet.get(address)
        if button.fn:
            if button.arg:
                if list is type(button.arg):
                    return button.fn(*button.arg)
                else:
                    return button.fn(button.arg)
            else:
                return button.fn()

    def touch_to_action(self) -> None:
        """
        Triggers the action tied to the button that was touched
        Args:
            None
        Returns:
            whatever the triggered function returns
        """
        for button in self.get_current_page():
            if button.just_pressed() and button.fn:
                if button.arg:
                    if list is type(button.arg):
                        return button.fn(*button.arg)
                    else:
                        return button.fn(button.arg)
                else:
                    return button.fn()

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

    def get_button_obj(address):
        """
        Returns the FunctionButton object at address to allow another function to modify it
        Args:
            address: a tuple with three integers giving page, row, and column
        Returns:
            a FunctionButton object or None
        """
        return ButtonSet.buttons.get(address)

    def draw_page(self):
        """Draws a page of FunctionButton objects after a page change"""
        self.display.set_pen(self.display.create_pen(*color_converter(self.background_color)))
        self.display.clear()
        current_page = self.get_current_page()
        for button in current_page:
            button.draw_button()
        self.board_obj.update()
    
    def next_page():
        """Change the current page to the next page of buttons if possible"""
        if ButtonSet.current_page < ButtonSet.max_page:
            ButtonSet.current_page += 1
            ButtonSet.needs_redrawing = True

    def previous_page():
        """Change the current page to the previous page of buttons if possible"""
        if ButtonSet.current_page > ButtonSet.min_page:
            ButtonSet.current_page -= 1
            ButtonSet.needs_redrawing = True

    def jump_to_page(page_number: int):
        """
        Change the current page to the page given as an input if possible
        Args:
            page_number: an integer for the page number to jump to.
        """
        if ButtonSet.min_page <= page_number <= ButtonSet.max_page:
            ButtonSet.current_page = page_number
            ButtonSet.needs_redrawing = True
    
class FunctionButton(Button):
    """ 
    An extension to the Button class to link a button to a function,
    draw a rounded rectangle, add text, and add an image.

    Handles missing or default inputs, calculates sizes and positioning to 
    center labels and symbols, and adds a rounded rectangle border.
    Contains methods for registering a button touch as a single debounced 
    action either when a button is first touched or first released.
    Also contains methods for drawing and redrawing buttons.

    Attributes
    ----------
    x: int
        screen position of the left edge of the button
    y: int
        screen position of the top edge of the button
    width: int
        width of the button
    height: int
        height of the button
    address: tuple
        page, row, and column address of this button
    board_obj: 
        The Presto class object for the hardware interface
    name: str
        Name of this button
    radius: int
        Corner radius of the rounded rectangle
    label: str
        Text that will be displayed on the button
    label_font: str
        Name of font file to used for the label text
    color: str | tuple | list
        color to be used for the text and outline
    outline_color: str | tuple | list
        color to be used for the outline, overrides color
    label_color: str | tuple | list
        color to be used for the label, overrides color
    symbol: str
        name of a png file with symbol to be displayed
    fn_name: str
        name of the function to be called when the button is pressed
    arg: str | list | dict | int | float
        arguments to the function to be called when the button is pressed

    Methods
    -------
    draw_button()
        draws button elements to be ready for a screen update
    redraw_button()
        draws button elements and calls a partial screen update around the button
    just_pressed()
        returns true once on the first calling after a button is touched
    just_released()
        returns true once on the first calling after a button is released
    """

    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 address: tuple,
                 board_obj,
                 name: str | None = None,
                 radius: int = 14,
                 label: str | None = None,
                 label_font: str | None = None,
                 color: str | tuple | list | None = 'white',
                 outline_color: str | tuple | list | None = None,
                 label_color: str | tuple | list | None = None,
                 symbol: str | None = None,
                 fn_name: str | None = None,
                 arg: str | list | dict | int | float | None = None,
                 **kwargs):
        """ Inits a FunctionButton object withe defaults for nonessential values."""
        super().__init__(x, y, width, height)

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.radius = radius
        self.address = address
        self.board_obj = board_obj
        self.name = name
        self.display = board_obj.display
        self.touch = board_obj.touch
        self.fn_name = fn_name
        self.arg = arg
        self.label = label
        self.depressed = False

        try:
            open(f'/art/{label_font}')
            self.label_font = f'/art/{label_font}'
        except Exception as exc:
            print(f"No font file called {label_font} found for button {self.name}. Using system font.")
            print(exc)
            self.label_font = None

        if outline_color:
            self.outline_color = self.display.create_pen(*color_converter(outline_color))
        else:
            self.outline_color = self.display.create_pen(*color_converter(color))
        
        if label_color:
            self.label_color = self.display.create_pen(*color_converter(label_color))
        else:
            self.label_color = self.display.create_pen(*color_converter(color))
        
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
                    print(f'There is no function named {fn_name} for button {self.name}.')
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
                print(f"No image file called {self.symbol_path} found for button {self.name}.")
                print(exc)
            
        if self.label:
            self.display.set_pen(self.label_color)
            if self.label_font:
                vector.set_font(self.label_font, int(0.33*self.height))
                text_x, text_y, text_width, text_height = vector.measure_text(self.label)
                if text_width > 0.9*self.width:
                    vector.set_font(self.label_font, int(0.9*self.width/text_width*0.33*self.height))
                    text_x, text_y, text_width, text_height = vector.measure_text(self.label)
                vector.text(self.label, 
                            int(self.x+0.5*self.width-text_x-0.5*text_width),
                            int(self.y+0.5*self.height+text_y+0.5*text_height))
            else:
                self.board_obj.display.text(self.label,
                                            int(self.x+5),
                                            int(self.y+0.5*self.height-5),
                                            int(self.width-10),
                                            3)
        self.display.set_pen(self.outline_color)
        shape = Polygon()
        shape.rectangle(self.x, 
                        self.y,
                        self.width, 
                        self.height, 
                        corners=(self.radius, self.radius, self.radius, self.radius), 
                        stroke=3)
        vector.draw(shape)

    def redraw_button(self):
        """Redraws a single button after some aspect of its appearance has been updated"""
        self.draw_button()
        self.board_obj.partial_update(int(self.x)-1,
                                      int(self.y)-1,
                                      int(self.width)+2,
                                      int(self.height)+2)

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
