import primitivepyg as pp
import pyglet as pyg

def make_batch(win):
    batch = pp.polygon(
        (200,100), (100,400), (5,5), (100,20),
        fill=0x000066ff,
        stroke=(0,100,0),
        stroke_width=10
    )

    batch = pp.polygon(
        (300,200), (400,120), (100,120),
        fill=(255,0,0),
        stroke=None,
        batch=batch
    )

    # resetting the batch like we did last time is actually not needed because it will be modified inside the function
    pp.ellipse(
        (win.width/2, win.height/2), (20, 30),
        fill=pp.colors.aquamarine,
        stroke=pp.colors.blue_violet,
        batch=batch
    )

    pp.square(
        (win.width-52.5, 52.5), 100,
        fill=pp.colors.aquamarine,
        stroke=pp.colors.dark_orange,
        stroke_width=5,
        batch=batch
    )

    pp.line(
        (10, 10), (win.width-10, win.height-10),
        stroke=pp.colors.dark_orange,
        stroke_width=5,
        batch=batch
    )

    pp.ellipse(
        (win.width/2, win.height/2), (win.width/2 - 5, win.height/2 - 5),
        fill=None,
        stroke=pp.colors.dark_orange,
        stroke_width=5,
        batch=batch
    )

    pp.point(
        (2.5, win.height-2.5),
        stroke=pp.colors.dark_orange,
        stroke_width=5,
        batch=batch
    )

    # here we are saving a style for use in the arc, chord, and pie we draw later on
    arc_style = dict(
        fill=pp.colors.rosy_brown,
        stroke=pp.colors.midnight_blue,
        stroke_width=3
    )
    pp.arc((500,400), (50,30), (0.5, 5.2), batch=batch, **arc_style)
    pp.chord((500,330), (50,30), (0.5,5.2), batch=batch, **arc_style)
    pp.pie((600,350), 30, (1.5,6.3), batch=batch, **arc_style)
    return batch


window = pyg.window.Window()
b = make_batch(window)

@window.event
def on_draw():
    window.clear()
    b.draw()

pyg.app.run()
