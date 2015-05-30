"""
primitives.py defines functions for drawing the primitives to batches

color types
    You can choose any of the following color formats when the argument type is `color`:
    0xRRGGBBAA
    (grey,)
    (grey,alpha)
    (red,green,blue)
    (red,green,blue,alpha)
    for convenience, a large number of color names are defined in primivepyg.colors

`options` for primitives
    Each primitive function takes the following keyword arguments:
    batch:pyglet.graphics.Batch is the batch the primitive is added to.
        If undefined, a new batch is created and used

    fill:color is the color used to fill the primitive.
        If set to None, the primitive will not be filled.  If undefined, the fill will default to white

    stroke:color is the color used on the border of the primitive
        If set to None, the primitive will not have a stroke.  If undefined, the stroke will default to black

    stroke_width:float is the width of the border around the primitive
        If undefined, the width will default to 1
"""

import primitivepyg.group as group
import primitivepyg.utils as utils
import pyglet as pyg
import math

VERT_TYPE = "v2f" # 2d float vertex

# should this be moved, perhaps to utils.py?
def mk_batch(options)->pyg.graphics.Batch:
    """
    This function simply creates a new batch if the given argument `batch` is None
    """
    return options.get("batch", pyg.graphics.Batch())

#todo: better documentation, perhaps less documentation (I went a little crazy)
def polygon_flat_points(points:list, **options)->pyg.graphics.Batch:
    """
    Draws a polygon from a flat list to a pyglet batch

    Parameters
        points:list is a flat list - that is a list in the form [x1, y1, x2, y2, ...]
        For the available `options` keywords see the docstring of primitivepyg.primitives

    returns the batch specified in `options` with a polygon added to it.
    """
    batch = mk_batch(options)
    fill_group, stroke_group = group.mk_groups(batch, options)
    num_points = len(points)//2
    if not fill_group.color_is_disabled():
        # ugly fill
        batch.add(num_points, pyg.gl.GL_TRIANGLE_FAN, fill_group, (VERT_TYPE, points))
        # AA line around the fill to cover up the ugliness
        batch.add(num_points, pyg.gl.GL_LINE_LOOP, fill_group, (VERT_TYPE, points))
    if not stroke_group.color_is_disabled():
        # AA stroke
        batch.add(num_points, pyg.gl.GL_LINE_LOOP, stroke_group, (VERT_TYPE, points))
        # points at the intersections of the stroke to cover up gaps
        batch.add(num_points, pyg.gl.GL_POINTS, stroke_group, (VERT_TYPE, points))
    return batch

def polygon(*points:tuple, **options)->pyg.graphics.Batch:
    """
    Draws a polygon from a set of coordinate tuples

    Parameters
        Each positional argument is a tuple representing a point on the polygon
        For the available `options` keywords see the docstring of primitivepyg.primitives

    returns the batch specified in `options` with a polygon added to it.
    """
    return polygon_flat_points(list(utils.flatten(points)), **options)

def ellipse(xy:tuple, xyr:tuple, **options)->pyg.graphics.Batch:
    """
    Draws an ellipse to a pyglet batch

    Parameters
        xy is a tuple containing the coordinates of the center of the ellipse
        xyr is a tuple containing the x and y radii of the ellipse
        For the available `options` keywords see the docstring of primitivepyg.primitives

    returns the batch specified in `options` with an ellipse added to it.
    """
    stroke_width = options.get("stroke_width", group.DEFAULT_STROKE_WIDTH)
    return polygon_flat_points(list(utils.ellipse_points(xy, xyr, stroke_width)), **options)

def circle(xy:tuple, radius:float, **options)->pyg.graphics.Batch:
    """
    A convenience function for drawing ellipses with equal radii

    Parameters
        xy is a tuple containing the coordinates of the center of the circle
        radius is the radius of the circle
        For the available `options` keywords see the docstring of primitivepyg.primitives

    returns the batch specified in `options` with a circle added to it.
    """
    return ellipse(xy, (radius, radius), **options)

def _base_arc(xy:tuple, xyr:tuple, start_stop:tuple, extra_points:tuple, **options):
    """
    _base_arch is a general case of partial ellipses that allows a number of extra points to be added to the ellipse
    these points are useful in forming shapes like the arc, but are not intended in use outside of such functions
    """
    start, stop = start_stop
    if start >= stop:
        # if there is no circle, return back the batch (or a batch if it doesn't exist) as there is nothing to be drawn
        return mk_batch(options)
    if stop - start >= 2 * math.pi:
        # if the circle is bigger than a full circle, just draw a full circle
        return ellipse(xy, xyr, **options)
    stroke_width = options.get("stroke_width", group.DEFAULT_STROKE_WIDTH)
    return polygon_flat_points(
        list(utils.ellipse_points(xy, xyr, stroke_width, start_stop, extra_points)),
        **options
    )

def arc(xy:tuple, xyr:tuple, start_stop:tuple, **options)->pyg.graphics.Batch:
    """
    Draws an elliptical arc to a pyglet batch

    Parameters
        xy is a tuple containing the center coordinate of the arc
        xyr is a tuple containing the x and y radii of the arc
        start_stop is a tuple containing the start and stop angles of the arc in radians
        For the available `options` keywords see the docstring of primitivepyg.primitives

    returns the batch specified in `options` with an arc added to it.
    """
    # arcs have an extra point in their centers
    return _base_arc(xy, xyr, start_stop, extra_points=xy, **options)

def pie(xy:tuple, radius:float, start_stop:tuple, **options)->pyg.graphics.Batch:
    """
    A convenience function for drawing arcs with equal radii

    Parameters
        xy is a tuple containing the center coordinate of the pie
        radius is the radius of the pie
        start_stop is a tuple containing the start and stop angles of the pie in radians
        For the available `options` keywords see the docstring of primitivepyg.primitives

    returns the batch specified in `options` with a pie added to it.
    """
    # circular arc
    return arc(xy, (radius, radius), start_stop, **options)

def chord(xy:tuple, xyr:tuple, start_stop:tuple, **options)->pyg.graphics.Batch:
    """
    Chords are ellipses with a segment cut off of them

    Parameters
        xy is a tuple containing the center coordinate of the chord
        xyr is a tuple containing the x and y radii of the chord
        start_stop is a tuple containing the angles where the chord cutoff begins and ends in radians
        For the available `options` keywords see the docstring of primitivepyg.primitives

    returns the batch specified in `options` with a chord added to it.

    note that unlike other elliptical functions, there is no circle counterpart to chord
    """
    # chords need no extra points
    return _base_arc(xy, xyr, start_stop, extra_points=(), **options)

def rectangle(xy:tuple, wh:tuple, **options)->pyg.graphics.Batch:
    """
    Draws a rectangle to a pyglet batch

    Parameters
        xy is a tuple containing the center coordinate of the rectangle
        wh is a tuple containing the width and height of the rectangle
        For the available `options` keywords see the docstring of primitivepyg.primitives

    returns the batch specified in `options` with a rectangle added to it.
    """
    x,y = xy
    w,h = wh
    return polygon((x-w/2, y-h/2), (x+w/2, y-h/2), (x+w/2, y+h/2), (x-w/2, y+h/2), **options)

def square(xy:tuple, side:float, **options)->pyg.graphics.Batch:
    """
    A convenience function for drawing rectangles with equal side lengths

    Parameters
        xy is a tuple containing the center coordinate of the square
        side is the side length of the square
        For the available `options` keywords see the docstring of primitivepyg.primitives

    returns the batch specified in `options` with a square added to it.
    """
    return rectangle(xy, (side, side), **options)

def line(xy1:tuple, xy2:tuple, **options)->pyg.graphics.Batch:
    """
    Draws a line to a pyglet batch

    Parameters
        xy1 is a tuple containing the first endpoint coordinate of the line
        xy2 is a tuple containing the second endpoint coordinate of the line
        For the available `options` keywords see the docstring of primitivepyg.primitives

    returns the batch specified in `options` with a line added to it.

    note that lines are unfilled, so the fill option will do nothing
    """
    batch = mk_batch(options)
    _, stroke_group = group.mk_groups(batch, options)
    if not stroke_group.color_is_disabled():
        batch.add(2, pyg.gl.GL_LINES, stroke_group, (VERT_TYPE, list(utils.flatten([xy1, xy2]))))
    return batch

def point(xy:tuple, **options)->pyg.graphics.Batch:
    """
    Draws a point to a pyglet batch

    Parameters
        xy is a tuple containing the coordinate to draw the point
        For the available `options` keywords see the docstring of primitivepyg.primitives

    returns the batch specified in `options` with a point added to it.

    note that points are unfilled, so the fill option will do nothing
    """
    batch = mk_batch(options)
    _, stroke_group = group.mk_groups(batch, options)
    if not stroke_group.color_is_disabled():
        batch.add(1, pyg.gl.GL_POINTS, stroke_group, (VERT_TYPE, xy))
    return batch