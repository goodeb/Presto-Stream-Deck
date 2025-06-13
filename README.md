# Presto Stream Deck

Low Code project for creating custom stream deck controllers on a Pimoroni Presto

# Contents
* [Overview](#overview)
* [Getting Started](#getting-started)
* [Customizing Buttons](#customizing-buttons)
    * [Required Inputs](#required-inputs)
    * [Optional Inputs](#optional-inputs)
    * [Function Arguments](#function-arguments)
    * [General Definitions](#general-definitions)
    * [Notes on Layout](#notes-on-layout)
* [Defining New Button Actions](#defining-new-button-action-functions)
* [FunctionButton Class](#functionbutton-class)
* [ButtonSet Class](#buttonset-class)

# Overview

This project provides a code base and example setup that turn the Pimoroni Preso into a stream deck like controller. The heart of each custom setup is the definitions JSON file. Everything about a button--its location, appearance, and the action it triggers--can be modified in this file. Overall setting such as the background color and default font are also defined in this file. Advanced users may want to add additional button functionality by adding functions to the button_action_fns.py library script, but changes to the other scripts in this project should not be needed.

The code for this project consists of the top level app script, a definitions JSON file, and a few library scripts with useful classes and helper functions. The two classes that make this project run are ``FunctionButton`` and ``ButtonSet``. ``FunctionButton`` extends the existing ``Button`` class to draw a box around each button's touch sensitive area and add optional graphic like button labels, images, and color changes. It also also adds debounced touch triggering through the ``just_pressed()`` and ``just_released()`` methods. Finally, it links each button to a function that defines the action that is taken when the button is pressed. ``ButtonSet`` parses the definitions, calculates the spacing for each page's layout and initializes the buttons. It has methods for converting a screen touch into a button action, and functions that buttons can link to to switch between pages of buttons.

# Getting Started

To use this project copy the main script ``stream_deck.py`` and the definitions file ``button_defs.json`` into the Presto's top level directory. Next copy the contents of the projects' lib directory to the lib directory on the Presto. Finally copy the project's art directory and its contents onto the Presto. 

The first page is a straight forward page full of buttons. Each has a custom label and color. Each button is linked to the same function, ``light_backlight()`` that lights the Presto's LED backlights to whatever color is passed as an argument.

The second page gives examples of adding symbols and controlling the spacing of buttons with a buffer button. It also the first example of custom variables and the use of the ``initialize_other_vars()`` function. In this case it is used to set up the Presto's builtin piezo buzzer so that buttons can turn it on and off.

The final page is the most complex example. The center button has labels and text at the same time. The buttons also trigger actions that change the of the center button. It also shows examples of more complicated function arguments.

# Customizing Buttons

Each button is separately defined by a JSON object in the list under ``button_defs``. These button objects have a mix of required and optional fields.

## Required Inputs
* page: The number of the page this button is on
* row: The number of the row on a page this button is on
* column: The number of the column in the row this button is on

Row and column numbers must be adjacent, start at 0, and be positive. Page numbers can be both positive and negative, but the default starting page will be zero. Button definitions do not have to be in order of page, row, and column in the JSON file, but it may be easier to list them in this way to make finding them later easier. 

## Optional Inputs
* name: Not used except in some error messages, but useful for finding a button definitions in the file
* radius: The corner radius of the rounded rectangle that will be drawn around the button. Make this 0 for square corners. Default value is 14
* label: The text that will be displayed on the button
* label_font: The font file in the ``art`` directory used for the label text. If given this overrides the default font of the rest of the project
* color: Color used for the label text and outline of the button. If not given the default will be white
* outline_color: Color used for the outline of the button. This will override color to make the outline and label have different colors
* label_color: Color used for the label text of the button. This will override color to make the outline and label have different colors
* symbol: The name of a .png file in the ``art/`` directory to be displayed on the button. 90x90 images work well. Symbol is displayed behind any text
* fn_name: The name of the function that will be triggered when the button is pressed. Should be one of the functions defined in ``button_action_fns.py``, or ``next_page()``, ``previous_page()``, or ``jump_to_a_page()``
* arg: The argument for the function, or arguments if given as a list. More on arguments in the next section

Colors can be either the name of one of the predefined colors, or a list or tuple of three integers from 0 to 255 for RGB values.

## Function arguments

Because of how the code handles multiple arguments as a list, if the function needs a single list as an argument, it should be passed as a list of the list. Since JSON cannot handle tuples as a data type, if a function needs a tuple as an input either a string or list should be used, and then the function should internally convert this argument. Several functions in the example code in ``button_defs.json`` do this. For example ``cycle_color()`` and  ``add_amount_to_label()``

## General Definitions

In addition to the button definitions, other general definitions about the project are included in the JSON file. The standard definitions for all projects are:
* margin_ratio: The fraction of the calculated button height to be used as the spacing around and between buttons
* default_color: The default color of text labels and buttons. This can be overridden for each button in its definition.
* background_color: The screen background color. Defaults to black
* default_font: The default font for all label text. This can be overridden for each button in its definition
* corner_radius: The corner radius of the rounded rectangle that will be drawn around the button. Make this 0 for square corners. If not given, the radius will default to the same as the gap between buttons calculated from margin_ratio

It is also possible to also define custom variables that will be accessible to all the button action functions in this area. An example of how this works is shown by the ``color_cycle`` definition. This variable gets declared as a Global in ``button_action_function.py`` and is used by the ``cycle_through_colors()`` function. Triggering this action is done withe center button on the third page, the one with the heart icon.

## Notes on Layout

Button positions are calculated by first dividing each page up into rows so that each row has the same height and has spaces between them defined as a ratio of the button height. Then each row is divided evenly into columns using the same spacing as between the rows. Each row can have different numbers of columns.

Blank spaces can be created to control the layout of other buttons with buffer buttons.  Simply define a button with no label, symbol, or action function and make its color the same as the project back ground color. Examples can be seen in the second and third pages of this project.

Additionally header labels or text display boxes can be created by defining buttons without an action function. Examples of how to dynamically modify the label or any other aspect of a button using ``button_set.py``'s ``get_button_obj()`` function are shown in the button functions ``cycle_through_colors()``, ``add_amount_to_label()``, and ``set_label()`` .

# Defining New Button Action Functions

Buttons can be linked to actions by defining the function name of a button to match one of the functions contained in the file ``lib/button_action_fns.py``. Also, there are three functions in the ``ButtonSet`` Class that buttons can linked to to switch pages: ``next_page()``, ``previous_page()``, and ``jump_to_page()``. Several examples of other action functions are given in the example code, but new functions can be defined to add new functionality. To work correctly these functions have to match the standard signature. After any specific arguments a function needs, a generic ``*arg`` should be put in to prevent any runtime errors. Also, a function that doesn't take arguments should have the generic ``*arg`` put in as an argument for the same reason.

Whatever other functions are defined in the ``button_action_fns.py`` file there is a required ``initialize_other_vars()`` function. This is needed to handle the custom global variables that can be defined in the general definitions part of the JSON file. The ``initialize_other_vars()`` function is also where to put initialization code for other unique aspects of an individual project. An example of how to do this is shown by the example of how buzzer is setup in the example code.

# FunctionButton Class

An extension to the Button class to link a button to a function, draw a rounded rectangle, add text, and add an image.

Handles missing or default inputs, calculates sizes and positioning to center labels and symbols, and adds a rounded rectangle border. Contains methods for registering a button touch as a single debounced action either when a button is first touched or first released. Also contains methods for drawing and redrawing buttons.

## Attributes

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

## Methods

draw_button()

    draws button elements to be ready for a screen update

redraw_button()

    draws button elements and calls a partial screen update around the button

just_pressed()

    returns true once on the first calling after a button is touched

just_released()

    returns true once on the first calling after a button is released

# ButtonSet Class

A collection of FunctionButton objects with addresses and dynamically calculated sizes
    
Takes a list of dictionaries with button definitions for FunctionButton objects and calculates their size and location and instantiates those objects. Provides methods for getting and drawing a page of buttons, changing pages, interacting with buttons through touch and direct addressing and retrieving individual button objects for external interaction with its attribute. Assumes that another script called button_action_fns.py will exists with an initialize_other_vars()function and other action functions for each of the buttons.

## Class Variables

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
    
## Attributes

ButtonSet: dict

    a dictionary of FunctionButton objects addressed by the tuple of page, row, and column numbers

board_obj: 


    The Presto class object for the hardware interface

display:

    The PicoGraphics class object for drawing on the screen

background_color: str | list | tuple

    The background screen color to be displayed behind buttons

## Methods
    
touch_to_button_address() -> tuple

    returns the address of a button that was just touched

run_addressed_button(address: tuple)

    riggers the action of the button at address

touch_to_action()

    triggers the action of the button that was just touched

get_a_page(page_number: int) -> list

    returns a list of all the FunctionButton objects on page_number

draw_page()

    clears the screen and draws the buttons on current_page

##  Class Functions
    
next_page()

    adds one to current page if in range and sets needs_redrawing to True

previous_page()

    subtracts one to current page if in range and sets needs_redrawing to True

jump_to_page(page_number: int)

    sets current page to page_number if in range and sets needs_redrawing to True