# Todo

### OpenGL stroke problem 
Stroke (lines and points) in OpenGL are a pain when you use a width greater than 1 for the following reasons:
* In some implementations, it is simply impossible to have a width greater than 1.  Most, if not all implementations have some limit to the size you can use.
* Lines do not join together in line loops, so when you make a polygon with a thick stroke, there will be noticable gaps.

Currently, the second problem is fixed using an ugly hack: inserting points at every intersection, and thus covering the gaps.  This makes the polygons look a bit weird, and cross-implementation support still does not exist.

I intend on fixing this by using quads that fill up intersections instead of line loops - fixing both problems at once, but so far the problem seems quite complex and a little frustrating.  Until it is fixed, try to avoid the use of stroke widths greater than 1.

Also note that I don't intend on changing the way that line and point work - they will continue to have cross-implementation issues if you use large widths.  The reason for this is primarily peformance based.  Plus, you can always just draw circles if you want a large point and polygons or rectangles if you want a thick line.
