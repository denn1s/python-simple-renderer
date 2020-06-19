from gl import Render

r = Render(1000, 1000)

def line(x1, y1, x2, y2):
    dy = abs(y2 - y1)
    dx =  abs(x2 - x1)

    steep = dy > dx
    
    if  steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1 

    dy =  abs(y2 - y1)
    dx =  abs(x2 - x1)

    offset = 0 * 2 * dx
    threshold = 0.5 * 2 * dx

    y = y1
    for x in range(x1, x2 + 1):
        if steep:
            r.point(y, x)
        else:
            r.point(x, y)
        offset += dy
        if offset >= threshold:
            y += 1 if y1 < y2 else -1
            threshold += 1 * 2 * dx
 

LINE0 =  (10, 10,  510, 10)
LINE22 = (10, 10,  462, 191)
LINE45 = (10, 10,  354, 354)
LINE67 = (10, 10,  191, 462)
LINE90 = (10, 10,  10, 510)

LINE180 = (790, 590, 790, 90)  
LINE202 = (790, 590, 609, 138)
LINE225 = (790, 590, 446, 246) 
LINE247 = (790, 590, 338, 409)
LINE270 = (790, 590, 290, 590)

line(*LINE22)
line(*LINE45)
line(*LINE67)

line(*LINE202)
line(*LINE225)
line(*LINE247)


LINE0_2 =  (10, 590,  510, 590)
LINE22_2 = (10, 590,  462, 409)
LINE45_2 = (10, 590,  354, 246)
LINE67_2 = (10, 590,  191, 138)
LINE90_2 = (10, 590,  10, 90)

LINE180_2 = (790, 10, 790, 510)  
LINE202_2 = (790, 10, 609, 462)
LINE225_2 = (790, 10, 446, 354) 
LINE247_2 = (790, 10, 338, 191)
LINE270_2 = (790, 10, 290, 10)

line(*LINE22_2)
line(*LINE45_2)
line(*LINE67_2)
line(*LINE202_2)
line(*LINE225_2)
line(*LINE247_2)


line(400, 400, 400, 800)
r.display()