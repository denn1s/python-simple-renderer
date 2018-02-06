from gl import Render, color, barycentric, bbox
from collections import namedtuple

Vector2 = namedtuple('Point', ['x', 'y'])
V2 = Vector2

RED = color(255, 0, 0)
BLUE = color(0, 0, 255)
GREEN = color(0, 255, 0)
WHITE = color(255, 255, 255)


r = Render(800, 600)

def triangle_wireframe(v0, v1, v2, color = None):
    a = Vector2(*v0)
    b = Vector2(*v1)
    c = Vector2(*v2)

    r.line(a, b, color)
    r.line(b, c, color)
    r.line(c, a, color)

triangle_wireframe((20, 140), (100, 320), (140, 160), RED)
triangle_wireframe((560, 100), (400, 2), (240, 560), BLUE)
triangle_wireframe((760, 300), (640, 320), (660, 360), GREEN)


def triangle(v0, v1, v2, color = None):
    a = Vector2(*v0)
    b = Vector2(*v1)
    c = Vector2(*v2)

    if a.y > b.y:
        a, b = b, a
    if a.y > c.y:
        a, c = c, a
    if b.y > c.y:
        b, c = c, b

    dx_ac = c.x - a.x
    dy_ac = c.y - a.y
    if dy_ac == 0:
        return
    mi_ac = dx_ac/dy_ac

    dx_ab = b.x - a.x
    dy_ab = b.y - a.y

    if dy_ab != 0:
        mi_ab = dx_ab/dy_ab
        for y in range(a.y, b.y + 1):
            xi = round(a.x - mi_ac * (a.y - y)) 
            xf = round(a.x - mi_ab * (a.y - y)) 

            if xi > xf:
                xi, xf = xf, xi

            for x in range(xi, xf):
                r.point(x, y)


    dx_bc = c.x - b.x
    dy_bc = c.y - b.y
    if dy_bc:
        mi_bc = dx_bc/dy_bc

        for y in range(b.y, c.y + 1):
            xi = round(a.x - mi_ac * (a.y - y)) 
            xf = round(b.x - mi_bc * (b.y - y)) 

            if xi > xf:
                xi, xf = xf, xi

            for x in range(xi, xf):
                r.point(x, y)
        

    r.line(a, b, BLUE)
    r.line(b, c, GREEN)
    r.line(c, a, RED)


def triangle2(a, b, c, color=None):
    print(a, b, c)
    A = V2(*a)
    B = V2(*b)
    C = V2(*c)

    bbox_min, bbox_max = bbox(A, B, C)

    for x in range(bbox_min.x, bbox_max.x + 1):
      for y in range(bbox_min.y, bbox_max.y + 1):
        coords = barycentric(A, B, C, V2(x, y))
        if all(coord > 0 for coord in coords):
          r.point(x, y, color)


triangle = triangle2


triangle((20, 140), (100, 320), (140, 160), RED)
triangle((560, 100), (400, 2), (240, 560), BLUE)
triangle((760, 300), (640, 320), (660, 360), GREEN)

# triangle((600, 600), (600, 600), (600, 600), RED)
# triangle((600, 600), (600, 100), (100, 100), RED)
# triangle((100, 500), (500, 500), (100, 100), RED)

r.write('./out.bmp')



