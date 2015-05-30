"""
group.py defines "group classes" - subclasses of pyglet's OrderedGroup that are essentially context managers that can be used with vertex lists in batches.
These group classes allow style settings (such as anti-aliasing and colors) to be applied to the vertex lists that make up primitives.
"""

import pyglet as pyg
import pyglet.gl as gl
from operator import attrgetter
import primitivepyg.colors as colors
from primitivepyg.convertcolors import get_color

DEFAULT_COLOR = None
DEFAULT_FILL = colors.white
DEFAULT_STROKE = colors.black
DEFAULT_STROKE_WIDTH = 1


class GLGroup(pyg.graphics.OrderedGroup):
    """
    A group that pushes and pops gl settings, allowing settings to be temporarily changed for its members.
    """
    def set_state(self):
        gl.glPushAttrib(gl.GL_ALL_ATTRIB_BITS)
    def unset_state(self):
        gl.glPopAttrib()
        
class AntiAliasedGroup(GLGroup):
    """
    A group that enables alpha colors and anti-aliasing for its members
    """
    def __init__(self, quality=gl.GL_DONT_CARE, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.quality = quality
    def set_state(self):
        super().set_state()

        # enable alpha colors
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        # enable anti-aliasing
        gl.glEnable(gl.GL_POINT_SMOOTH)
        gl.glEnable(gl.GL_LINE_SMOOTH)
        gl.glEnable(gl.GL_POLYGON_SMOOTH)
        gl.glHint(gl.GL_POINT_SMOOTH_HINT, self.quality)
        gl.glHint(gl.GL_LINE_SMOOTH_HINT, self.quality)
        gl.glHint(gl.GL_POLYGON_SMOOTH_HINT, self.quality)

class ColoredGroup(AntiAliasedGroup):
    """
    A group that changes the color of its members
    """
    def __init__(self, options, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = options.get("color", DEFAULT_COLOR)
    def color_is_disabled(self)->bool:
        return self.color is None
    def set_state(self):
        super().set_state()
        if not self.color_is_disabled():
            gl.glColor4ub(*get_color(self.color))

class StrokeGroup(ColoredGroup):
    """
    The stroke group styles points and lines drawn with it
    """
    def __init__(self, options, *args, **kwargs):
        super().__init__(options, *args, **kwargs)
        self.width = options.get("stroke_width", DEFAULT_STROKE_WIDTH)
        self.color = options.get("stroke", DEFAULT_STROKE)
    def set_state(self):
        super().set_state()
        gl.glLineWidth(self.width)
        gl.glPointSize(self.width)

class FillGroup(ColoredGroup):
    """
    The fill group changes the color primitives are drawn with
    """
    def __init__(self, options, *args, **kwargs):
        super().__init__(options, *args, **kwargs)
        self.color = options.get("fill", DEFAULT_FILL)


def top_order(batch:pyg.graphics.Batch, base:int=0)->int:
    """
    Returns the order of the highest ordered OrderedGroup in batch `batch`
    `base` is the value returned if there are no ordered groups in the batch
    """
    # we need to get rid of non OrderedGroups, so we filter out everything that isn't an instance of OrderedGroup from batch.top_groups which is a list of all the groups used in the batch
    ordered_groups = list(filter(lambda g: isinstance(g, pyg.graphics.OrderedGroup), batch.top_groups))
    if len(ordered_groups) > 0:
        return max(ordered_groups, key=attrgetter("order")).order
    return base

def mk_groups(batch:pyg.graphics.Batch, options:dict)->(FillGroup, StrokeGroup):
    """
    This is meant to be used as setup for the primitive drawing functions
    It creates two OrderedGroups, a FillGroup and a StrokeGroup with an order slightly higher than the highest order in the batch
    """
    base_order = top_order(batch)
    return (
        # the fill group needs to have a lower order than the stroke so it doesn't cover it up, which is a problem that bothered be relentlessly before I learned about OrderedGroups.
        FillGroup(options, order=base_order+1),
        StrokeGroup(options, order=base_order+2)
    )