"""
convertcolors.py provides functions for converting various color formats to (red, green, blue, alpha)
"""

RED_MASK   = 0xff000000
GREEN_MASK = 0x00ff0000
BLUE_MASK  = 0x0000ff00
ALPHA_MASK = 0x000000ff

def color_from_hex(hex_color:int)->(int,int,int,int):
    """
    Takes a hex value in either of the form 0xRRGGBBAA and returns a tuple containing the R, G, B, and A components from 0 to 255.
    """
    # this commented-out code adds ambiguity as there would be no way to have a 0 for red and also have an alpha.
    # if hex_color <= 0xffffff: # if alpha value not included
    #     # fill in the AA part with 255
    #     hex_color <<= 8
    #     hex_color |= 0xff
    return (hex_color & RED_MASK) >> 24, (hex_color & GREEN_MASK) >> 16,\
           (hex_color & BLUE_MASK) >> 8, (hex_color & ALPHA_MASK)

def get_color(color)->(int,int,int,int):
    """
    Return an R, G, B, A tuple from color, which can be any of the following formats:
    0xRRGGBBAA
    (grey,)
    (grey,alpha)
    (red,green,blue)
    (red,green,blue,alpha)
    """
    if isinstance(color, int):
        # color is a hex color
        return color_from_hex(color)
    if isinstance(color, tuple): # todo: perhaps allow all tuple-like types?
        # color is already a tuple, but may need to be formatted correctly
        if len(color) == 1: # grey scale
            return color[0],color[0],color[0],255
        if len(color) == 2: # alpha grey scale
            return color[0],color[0],color[0],color[1]
        if len(color) == 3: # R,G,B
            return color+(255,)
        if len(color) == 4: # R,G,B,A
            return color
        raise ValueError("color has invalid length")
    raise ValueError("color must be int or tuple")