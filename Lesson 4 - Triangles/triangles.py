from gl import Render, color
from collections import namedtuple


r = Render(800, 600)


RED = color(255, 0, 0)
GREEN = color(0, 255, 0)
BLUE = color(0, 0, 255)
WHITE = color(255, 255, 255)


Vertex2 = namedtuple('Point', ['x', 'y'])


# ejercicio: dado este bloque de codigo, como podemos rellenar todos los triangulos

def triangle1(v0, v1, v2, color):
    r.line(v0, v1, color) 
    r.line(v1, v2, color) 
    r.line(v2, v0, color)


# pista:

# 1. El algoritmo debe ser simple y rapido
# 2. El algoritmo debe funcionar sin importar el orden de los vertices
# 3. Si dos triangulos comparten un vertice, no deben quedar agujeros entre ellos (los vamos a usar para los modelos)


# 30 minutos para enviar el ejercicio

def triangle2(v0, v1, v2, color):
    # paso 0, sintaxis
    a = Vertex2(*v0)
    b = Vertex2(*v1)
    c = Vertex2(*v2)
    
    # Paso 1, ordenamos el triangulo de abajo para arriba (bubbles!)
    if a.y > b.y:
        a, b = b, a

    # a es el menor entre a y b
    
    if a.y > c.y:
        a, c = c, a

    # a es el menor entre a y c
         
    if b.y > c.y: 
        b, c = c, b

    # b es el menor entre b y c
    
    # osea, a es el que esta mas abajo, b esta en medio y c esta hasta arriba

    r.line(a, b, BLUE)
    r.line(b, c, GREEN)
    r.line(c, a, RED)

# lo que nos interesa es la linea roja
# no queremos usar el algoritmo de lineas
# vamos a hacer lineas horizontales (de abajo para arriba), por lo que solo vamos a tener un valor de X para cada Y

def triangle3(v0, v1, v2, color):
    # paso 0, sintaxis
    a = Vertex2(*v0)
    b = Vertex2(*v1)
    c = Vertex2(*v2)

    if a.y > b.y:
        a, b = b, a
    if a.y > c.y:
        a, c = c, a
    if b.y > c.y: 
        b, c = c, b

    """
    for y in range(a.y, b.y + 1):
        xi = a.x
        xf = b.x
        # dibujar triangulo en el pizarron de xi a xf
        for x in range(xi, xf + 1):
            r.point(x, y)

    debemos swapear los valores de xi y xf si xf < xi
    """

    """
    dabx = b.x - a.x
    daby = b.y - a.y
    miab = dabx/daby

    for y in range(a.y, b.y + 1):
        xi = round(a.x - miab * (a.y - y))
        xf = b.x
        # dibujar triangulo en el pizarron de xi a xf

        if xi > xf:
            xi, xf = xf, xi
        for x in range(xi, xf + 1):
            r.point(x, y)
    """

    dabx = b.x - a.x
    daby = b.y - a.y
    miab = dabx/daby

    dacx = c.x - a.x
    dacy = c.y - a.y
    miac = dacx/dacy

    for y in range(a.y, b.y + 1):
        xi = round(a.x - miab * (a.y - y))
        xf = round(a.x - miac * (a.y - y))
        # dibujar triangulo en el pizarron de xi a xf

        if xi > xf:
            xi, xf = xf, xi
        for x in range(xi, xf + 1):
            r.point(x, y)
            

# mitad de arriba, dejarla como ejercicio?

def triangle4(v0, v1, v2, color):
    # paso 0, sintaxis
    a = Vertex2(*v0)
    b = Vertex2(*v1)
    c = Vertex2(*v2)

    if a.y > b.y:
        a, b = b, a
    if a.y > c.y:
        a, c = c, a
    if b.y > c.y: 
        b, c = c, b

    """
    for y in range(a.y, b.y + 1):
        xi = a.x
        xf = b.x
        # dibujar triangulo en el pizarron de xi a xf
        for x in range(xi, xf + 1):
            r.point(x, y)

    debemos swapear los valores de xi y xf si xf < xi
    """

    """
    dabx = b.x - a.x
    daby = b.y - a.y
    miab = dabx/daby

    for y in range(a.y, b.y + 1):
        xi = round(a.x - miab * (a.y - y))
        xf = b.x
        # dibujar triangulo en el pizarron de xi a xf

        if xi > xf:
            xi, xf = xf, xi
        for x in range(xi, xf + 1):
            r.point(x, y)
    """

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
            # dibujar triangulo en el pizarron de xi a xf

            if xi > xf:
                xi, xf = xf, xi
            for x in range(xi, xf + 1):
                r.point(x, y)

    dx_bc = c.x - b.x
    dy_bc = c.y - b.y
    if dy_bc:
        mi_bc = dx_bc/dy_bc

        # dacx = c.x - a.x
        # dacy = c.y - a.y
        # miac = dacx/dacy  WE HAVE MIAC ALREADY

        for y in range(b.y, c.y + 1):
            xi = round(a.x - mi_ac * (a.y - y))
            xf = round(b.x - mi_bc * (b.y - y))
            # dibujar triangulo en el pizarron de xi a xf

            if xi > xf:
                xi, xf = xf, xi
            for x in range(xi, xf + 1):
                r.point(x, y)

"""
triangle = triangle4

triangle((20, 140), (100, 320), (140, 160), RED)
triangle((560, 100), (400, 2), (240, 560), BLUE)
triangle((760, 300), (640, 320), (660, 360), GREEN)


triangle = triangle2

triangle((20, 140), (100, 320), (140, 160), RED)
triangle((560, 100), (400, 2), (240, 560), BLUE)
triangle((760, 300), (640, 320), (660, 360), GREEN)

"""

triangle = triangle4



# triangle((20, 140), (100, 320), (140, 160), RED)
# triangle((560, 100), (400, 2), (240, 560), BLUE)
# triangle((760, 300), (640, 320), (660, 360), GREEN)

triangle((600, 600), (600, 600), (600, 600), RED)
# triangle((600, 600), (600, 100), (100, 100), RED)
triangle((100, 500), (500, 500), (100, 100), RED)




r.write('out.bmp')


r.load('./model.obj')
r.write('out.bmp')