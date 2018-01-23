import sys
import random
from gl import Render, color


r = Render(800, 600)

# ejemplo 1, cuadrado

def line0(x1, y1, x2, y2):
    for x in range(x1, x2):
        for y in range(y1, y2):
            # if x == y:
            r.point(x, y)


# ejemplo 2, y - mx + b
# se pierden puntos si la pendiente es muy empinada, por eso revertimos la grafica despues

def line1(x1, y1, x2, y2):
    dy = y2 - y1
    dx = x2 - x1
    m = dy/dx

    for x in range(x1, x2):
        y = y1 - m * (x1 - x)
        r.point(round(x), round(y))


# ejemplo 3: intercambiar x y y si dy > dx, recalcular pendiente (hay implementaciones distintas)

def line2(x1, y1, x2, y2):
    dy = y2 - y1
    dx = x2 - x1
    m = dy/dx

    steep = dy > dx

    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    dy = y2 - y1
    dx = x2 - x1
    m = dy/dx

    points = []
    for x in range(x1, x2 + 1):
        y = y1 - m * (x1 - x)

        if steep:
            points.append((int(y), int(x)))
        else:
            points.append((int(x), int(y)))

    for point in points: # ya no importa
        r.point(*point)


# ejemplo 4: mostrar imagenes
# es posible reescribir y como funcion de la pendiente (literalmente y1 + la pendiente)

def line3(x1, y1, x2, y2):
    dy = y2 - y1
    dx = x2 - x1
    m = dy/dx

    steep = dy > dx

    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    dy = y2 - y1
    dx = x2 - x1
    m = dy/dx

    offset = 0

    y = y1
    points = []
    for x in range(x1, x2 + 1):
        if steep:
            points.append((y, x))
        else:
            points.append((x, y))
        
        # y = y + 1 # linea 0

        offset += m
        y = y1 + round(offset)

    for point in points:
        r.point(*point)


# round es un poco costoso, por lo que que modificamos el algoritmo
# resulta que y sube 1 cada vez que la pendiente pasa de un threshold 0.5, luego 1.5, luego 2.5, etc

def line4(x1, y1, x2, y2):
    dy = y2 - y1
    dx = x2 - x1
    m = dy/dx

    steep = dy > dx

    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    dy = y2 - y1
    dx = x2 - x1
    m = dy/dx

    offset = 0
    threshold = 0.5

    y = y1
    points = []
    for x in range(x1, x2 + 1):
        if steep:
            points.append((y, x))
        else:
            points.append((x, y))
        
        offset += m
        if offset >= threshold:
            y += 1
            threshold += 1

    for point in points:
        r.point(*point)
            

# solo nos falta deshacernos de los decimales, esto normalmente es mas costoso que trabajar con enteros
# y de todas maneras solo tenemos pixeles y numeros redondos
# multiplicamos threshold y offset * 2 primero para eliminar el 0.5
# luego multiplicamos por dx para eliminar la pendiente


def line5(x1, y1, x2, y2):
    dy = y2 - y1
    dx = x2 - x1

    steep = dy > dx

    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    dy = y2 - y1
    dx = x2 - x1

    offset = 0 * 2 * dx
    threshold = 0.5 * 2 * dx

    y = y1
    points = []
    for x in range(x1, x2 + 1):
        if steep:
            points.append((y, x))
        else:
            points.append((x, y))
        
        offset += (dy/dx) * 2 * dx
        if offset >= threshold:
            y += 1
            threshold += 1 * 2 * dx

    for point in points:
        r.point(*point)



# ya terminamos, solo nos falta un caso que hemos ignorado, cuando las lineas van para abajo
# podemos trabajar al rededor de el si cambiamos x1 por x2 en el caso donde x1 > x2 (para empezar siempre en el menor)
# adicionalmente, tneemos que considerar que las lineas van bajando, no subiendo si y1 > y2, por lo que se le resta 1
# a y en lugar de sumarle (el offset y el threshold funcionan bien por el abs) 


def line6(x1, y1, x2, y2):
    dy = abs(y2 - y1)
    dx = abs(x2 - x1)
 
    steep = dy > dx
    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dy = abs(y2 - y1)
    dx = abs(x2 - x1)

    offset = 0 * 2 * dx
    threshold = 0.5 * 2 * dx

    y = y1
    points = []

    for x in range(x1, x2 + 1):
        if steep:
            points.append((y, x))
        else:
            points.append((x, y))
        
        offset += dy * 2
        if offset >= threshold:
            y += 1 if y1 < y2 else -1
            threshold += 1 * 2 * dx

    for point in points:
        r.point(*point)



line = line3



#  http://www.wolframalpha.com/input/?i=SAA+500,+5%C2%BA,+90%C2%BA


LINE0 =  (10, 10,  510, 10)
# LINE5 =  (10, 10,  498, 44)   
LINE22 = (10, 10,  462, 191)
LINE45 = (10, 10,  354, 354)
LINE67 = (10, 10,  191, 462)
LINE90 = (10, 10,  10, 510)

# http://www.wolframalpha.com/input/?i=rotate+(10,+510)+by+180+degrees+center+(300,400)+anticlockwise

LINE180 = (790, 590, 790, 90)  
LINE202 = (790, 590, 609, 138)
LINE225 = (790, 590, 446, 246) 
LINE247 = (790, 590, 338, 409)
LINE270 = (790, 590, 290, 590)

# line(*LINE0)
line(*LINE22)
line(*LINE45)
line(*LINE67)
# line(*LINE90)
# line(*LINE180)
line(*LINE202)
line(*LINE225)
line(*LINE247)
# line(*LINE270)

# reversed lines

LINE0_2 =  (10, 590,  510, 590)
# LINE5_2 =  (10, 590,  498, 556)   
LINE22_2 = (10, 590,  462, 409)
LINE45_2 = (10, 590,  354, 246)
LINE67_2 = (10, 590,  191, 138)
LINE90_2 = (10, 590,  10, 90)


LINE180_2 = (790, 10, 790, 510)  
LINE202_2 = (790, 10, 609, 462)
LINE225_2 = (790, 10, 446, 354) 
LINE247_2 = (790, 10, 338, 191)
LINE270_2 = (790, 10, 290, 10)



# line(*LINE0_2)
# line(*LINE5_2)
line(*LINE22_2)
line(*LINE45_2)
line(*LINE67_2)
# line(*LINE90_2)
# line(*LINE180_2)
line(*LINE202_2)
line(*LINE225_2)
line(*LINE247_2)
# line(*LINE270_2)



r.display()



# line(*LINE5)
