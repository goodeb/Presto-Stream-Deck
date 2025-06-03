# ICON []
# NAME Stream Deck
# DESC App to turn the Presto into a easily customizable stream deck
# SPDX-FileCopyrightText: 2025 Brent Goode
# SPDX-License-Identifier: MIT

"""
ButtonSet.py 2025-06-02 v 1.0

Author: Brent Goode

Class libraries for ButtonSet and FunctionButton objects

"""

from presto import Presto
from button_set import ButtonSet
from utils import show_message, connect_wifi, read_input_file

presto = Presto(full_res=True)

show_message(presto,"Loading...")

wifi = connect_wifi(presto)

buttons_defs, margin_ratio, background_color, font_file, other_vars = read_input_file('button_defs.json')

buttons = ButtonSet(buttons_defs,presto,margin_ratio,background_color,font_file,other_vars=other_vars)

buttons.redraw_page()

while True:
    buttons.touch_to_action()
    
    if ButtonSet.needs_redrawing:
        buttons.redraw_page()
        ButtonSet.needs_redrawing = False
