# Presto Stream Deck
Low/No Code project for creating custom stream deck controller on a Pimoroni Presto

# Overview

# Button Definitions
Each button is separately defined by a JSON object in the list under the top level "button_defs" element. These button objects have a mix of required and optional fields.

# Button Action Function Definitions
Buttons can be linked to actions by passing the name and arguments of a function contained in the file lib/button_action_fns.py. To work correctly these functions have to match the stantard signature. Also there are conditions on the arguments due to limits on what JSON can represent.
