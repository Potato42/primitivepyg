import math

MIN_ELLIPSE_VERTICES = 50
MAX_ELLIPSE_VERTICES = 5000
FULL_CIRCLE = (0, 2*math.pi)

def constrain(n:float, minimum:float=None, maximum:float=None)->float:
    if minimum is not None and n < minimum: return minimum
    if maximum is not None and n > maximum: return maximum
    return n

def flatten(iterable):
    """
    Generator to flatten an iterable by one level
    """
    for i in iterable:
        yield from i

def ellipse_coord(xy:tuple, xyr:tuple, theta:float)->(float,float):
    """
    Return the cartesian coordinates of point on an ellipse from its angle around the ellipse
    """
    x, y = xy
    xr, yr = xyr
    return x + xr*math.cos(theta), y + yr*math.sin(theta)

def num_ellipse_segments(xyr:tuple, stroke_width:float)->int:
    """
    Return a good number of segments to use with a ellipse with the given parameters
    """
    xr, yr = xyr
    if xr == yr: # circle
        circumference = 2 * math.pi * xr
    else: # ellipse (approximation)
        circumference = math.pi * (3*(xr + yr) - math.sqrt((3*xr + yr) * (xr + 3*yr)))
    return int(constrain(circumference/stroke_width, MIN_ELLIPSE_VERTICES, MAX_ELLIPSE_VERTICES))

def ellipse_points(xy:tuple, xyr:tuple, stroke_width:float, start_stop:tuple=FULL_CIRCLE, extra_points:tuple=()):
    """
    A generator that returns the points that make up an ellipse with the given parameters
    As a list, the result would look like this [x1, y1, x2, y2, ...]
    Also can generate more complicated ellipse-like shapes such as arcs using the start_stop and extra_points parameters
    """
    start, stop = start_stop
    angle_change = stop - start
    # we use ceil because we want a point even if angle_change is very small
    segments = math.ceil(num_ellipse_segments(xyr, stroke_width) * angle_change / (2*math.pi))

    yield from extra_points
    for s in range(segments):
        theta = 2 * math.pi * s / segments
        # this will only change theta if start_stop isn't (0, 2pi)
        theta = start + theta*angle_change / (2*math.pi)
        yield from ellipse_coord(xy, xyr, theta)