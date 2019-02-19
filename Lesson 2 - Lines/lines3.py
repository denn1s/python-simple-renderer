from gl import Render

r = Render(100, 100)

def line(x1, y1, x2, y2):
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
    
    offset = 0
    threshold = dx

    y = y1
    inc = 1 if y2 > y1 else -1
    for x in range(x1, x2 + 1):
        if steep:
            r.point(y, x)
        else:
            r.point(x, y)
        
        offset += dy * 2
        if offset >= threshold:
            y += inc
            threshold += 2 * dx


line(30, 80, 10, 10)
r.display()
