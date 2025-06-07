# ICON [[(-22.0,-22.0),(-9.0,-22.0),(-9.0,-9.0),(-22.0,-9.0),(-22.0,-22.0)],[(-20.0,-20.0),(-11.0,-20.0),(-11.0,-11.0),(-20.0,-11.0),(-20.0,-20.0)],[(22.0,-22.0),(9.0,-22.0),(9.0,-9.0),(22.0,-9.0),(22.0,-22.0)],[(20.0,-20.0),(11.0,-20.0),(11.0,-11.0),(20.0,-11.0),(20.0,-20.0)],[(-22.0,22.0),(-9.0,22.0),(-9.0,9.0),(-22.0,9.0),(-22.0,22.0)],[(-20.0,20.0),(-11.0,20.0),(-11.0,11.0),(-20.0,11.0),(-20.0,20.0)],[(22.0,22.0),(9.0,22.0),(9.0,9.0),(22.0,9.0),(22.0,22.0)],[(20.0,20.0),(11.0,20.0),(11.0,11.0),(20.0,11.0),(20.0,20.0)],[(-7.0,9.0),(7.0,9.0),(7.0,22.0),(-7.0,22.0),(-7.0,9.0)],[(-5.0,11.0),(5.0,11.0),(5.0,20.0),(-5.0,20.0),(-5.0,11.0)],[(-7.0,-9.0),(7.0,-9.0),(7.0,-22.0),(-7.0,-22.0),(-7.0,-9.0)],[(-5.0,-11.0),(5.0,-11.0),(5.0,-20.0),(-5.0,-20.0),(-5.0,-11.0)],[(9.0,-7.0),(22.0,-7.0),(22.0,7.0),(9.0,7.0),(9.0,-7.0)],[(11.0,-5.0),(20.0,-5.0),(20.0,5.0),(11.0,5.0),(11.0,-5.0)],[(-9.0,-7.0),(-22.0,-7.0),(-22.0,7.0),(-9.0,7.0),(-9.0,-7.0)],[(-11.0,-5.0),(-20.0,-5.0),(-20.0,5.0),(-11.0,5.0),(-11.0,-5.0)],[(-7.0,-7.0),(7.0,-7.0),(7.0,7.0),(-7.0,7.0),(-7.0,-7.0)],[(-5.0,-5.0),(5.0,-5.0),(5.0,5.0),(-5.0,5.0),(-5.0,-5.0)]]
# NAME Stream Deck
# DESC App to turn the Presto into a easily customizable stream deck
# SPDX-FileCopyrightText: 2025 Brent Goode
# SPDX-License-Identifier: MIT

"""
ButtonSet.py 2025-06-02 v 1.0

Author: Brent Goode

Main script for stream deck app

"""

from presto import Presto
from button_set import ButtonSet
from utils import show_message, connect_wifi, read_input_file

board_obj = Presto(full_res=True)

show_message(board_obj,"Loading...")

#wifi = connect_wifi(board_obj)

buttons_defs, margin_ratio, default_color, background_color, \
    default_font, corner_radius, other_vars = read_input_file('button_defs.json')

buttons = ButtonSet(buttons_defs,
                    board_obj,
                    margin_ratio,
                    default_color,
                    background_color,
                    default_font,
                    corner_radius,
                    other_vars=other_vars)

buttons.draw_page()

while True:
    action_result = buttons.touch_to_action()
    
    if ButtonSet.needs_redrawing:
        buttons.draw_page()
        ButtonSet.needs_redrawing = False
