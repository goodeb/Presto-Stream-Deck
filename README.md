# Presto Stream Deck

Low Code project for creating custom stream deck controller on a Pimoroni Presto

# Overview

This project consists of the top level app script, a definitions JSON file, and a few library scripts with useful classes and helper functions. The heart of each custom setup is the definitions JSON file. Everything about a button--its location, appearance, and the action it triggers--can be modified in this file without changing any of the Python code. Overall setting such as the background color and default font are also defined in this file. Advanced users may want to add additional button functionality by adding functions to the button_action_fns.py library script, but changes to the other scripts in this project should not be needed.

# Getting Started

To use this project copy the main script ``stream_deck.py`` and the definitions file ``button_defs.json`` into the top level directory. Next copy the contents of the projects' lib directory to the lib directory on the Presto. Finally copy the project's art directory onto the Presto. 

First pages show the basics of setting up buttons and customizing their appearance while interacting with the Presto's hardware features. The third page shows examples of displaying both symbols and labels and making buttons interact with the appearance of other buttons.

# Button Definitions

Each button is separately defined by a JSON object in the list under the top level ``button_defs`` element. These button objects have a mix of required and optional fields.  These fields and their definitions are:
## Required
* page:
* row:
* column:
## Optional
* name: Not used by the code currently, but useful for finding the button definitions in the file
* label: The text that will be displayed on the button
* label_font: Font used for the label text. If given this overrides the default font of the rest of the project
* color: Color used for the label text and outline of the button. If not given the default will be white
* outline_color: Color used for the outline of the button. This will override color to make the outline and label have different colors
* label_color: Color used for the label text of the button. This will override color to make the outline and label have different colors
* symbol: The name of a .png file in the ``art/`` directory to be displayed on the button. 90x90 images work well. Symbol is displayed behind any text, so pick the colors carefully.
* fn: The name of the function that will be triggered when the button is pressed. Should be one of the functions defined in ``button_defs.json``
* arg: The argument for the function, or arguments if given as a list. More on arguments in the next section

## Function arguments

Because of how the code handles multiple arguments as a list, if the function needs a single list as an argument, it should be passed as a list of the list. Since JSON cannot handle tuples as a data type if a function needs a tuple as an input either a string or list should be used, and then the function should internally conger this argument. Several functions in the example code in ``button_defs.json`` do this. For example ``cycle_color()`` and  ``add_amount_to_label()``

## Other notes on button definitions

Button definitions do not have to be in order, but it may be easier to list them in this way to ease finding them later. Pages rows and columns must consist of adjacent numbers. Page numbers can be both positive and negative, but the default starting page will always be zero. Row and column numbers can only be positive and should start at 0. 

# General Definitions

In addition to the button specific definitions, some other general definitions are included in the JSON file. The standard definitions for all projects are:
* margin_ratio: The fraction of the calculated button height to be used as the margin around and between buttons
* default_color: The default color of text labels and buttons. This can be overridden for each button in its definition.
* background_color: The screen background color
* default_font: The default font for all label text. This can be overridden for each button in its definition.

It is also possible to also define custom variables that will be accessible to all the button action functions in this area. An example of how this works is shown by the ``color_cycle`` definition. This variable gets declared as Global in button_action_function.py and is used by the ``color_cycle()`` function. Triggering this action is done withe center button on the third page, the one with the heard icon.

# Notes on Layout

Button positions are calculated by first dividing each page up into rows so that each row has the same height and has spaces between then defined as a ratio of the button height. Then each row is divided evenly into columns using the same spacing as between the rows. Different rows can have different numbers of columns.

Blank spaces can be created to control the layout of other buttons and can be seen in the second and third pages of the example setup. Simply define a button with no label, symbol, or action function and make its color the same as the project back ground color.

Additionally header labels or text display boxes can be created by defining buttons without an action function. Examples of how to interact with these labels are shown 

# Button Action Function Definitions

Buttons can be linked to actions by passing the name and arguments of a function contained in the file ``lib/button_action_fns.py``. To work correctly these functions have to match the standard signature. Also there are conditions on the arguments due to limits on what JSON can represent.
 {the required initialize_other_vars fn. Can be used to do other set up as shown by the example of how buzzer is setup}
 {All functions need to have the same signature}