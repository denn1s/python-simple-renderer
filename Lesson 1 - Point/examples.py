import sys
import random
from gl import Render, color


def single_point():
    """
    Draws a single point in the screen (upper left corner)
    """
    r = Render(800, 600)
    r.point(10, 590)
    r.write('out.bmp')


def square():
    """
    Draws a square (to test correct dimensions)
    """
    width = 800
    height = 600
    r = Render(width, height)

    padding = 10
    square_w = width - padding
    square_h = height - padding

    # horizontal lines
    for x in range(width):
        if (x > padding and x < square_w):
            r.point(x, square_h)
            r.point(x, padding)

    # vertical lines
    for y in range(height):
        if (y > padding and y < square_h):
            r.point(square_w, y)
            r.point(padding, y)

    r.write('out.bmp')



def diagonal():
    """
    Draws a perfectly diagonal line
    """
    width = 800
    height = 600
    r = Render(width, height)

    # very inefficient
    for x in range(width):
        for y in range(height):
            if x == y:
                r.point(x, y)

    r.write('out.bmp')


def static():
    """
    Draws static noise in B/W
    """
    width = 800
    height = 600
    r = Render(width, height)

    # very inefficient
    for x in range(width):
        for y in range(height):
            if random.random() > 0.5:  # 50/50 chance
                r.point(x, y)

    r.write('out.bmp')


def color_static():
    """
    Draws static noise in color
    """
    width = 800
    height = 600
    r = Render(width, height)

    # very inefficient
    for x in range(width):
        for y in range(height):
            r.point(x, y, color(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            ))

    r.write('out.bmp')


def stars():
    """
    Randomly draws stars
    """
    width = 800
    height = 600
    r = Render(width, height)

    def star(x, y, size):
        """
        Draws a star.
        Size 1: small
        Size 2: medium
        Size 3: big
        """
        c = random.randint(0, 255)
        r.set_color(color(c, c, c)) # 3 identical colors will always be gray

        if size == 1:
            r.point(x, y)
        elif size == 2:  # 4 points
            r.point(x, y)
            r.point(x+1, y)
            r.point(x, y+1)
            r.point(x+1, y+1)
        elif size == 3:  # 9 points
            r.point(x, y)
            r.point(x+1, y)
            r.point(x, y+1)
            r.point(x-1, y)
            r.point(x, y-1)
            # remove the corners 
            # r.point(x+1, y+1)
            # r.point(x-1, y-1)
            # r.point(x-1, y+1)
            # r.point(x+1, y-1)

    # leaves a 2 pixel padding to avoid OOB
    for x in range(width - 4):
        for y in range(height - 4):
            if random.random() < 0.001:  # 0.1% only 0.1 chance of actually rendering a star 
                star(x + 2, y + 2, random.randint(1, 3))

    r.write('out.bmp')    


if __name__ == "__main__":
    example = sys.argv[1]
    if example == "single_point":
        single_point()
    elif example == "square":
        square()
    elif example == "diagonal":
        diagonal()
    elif example == "static":
        static()
    elif example == "color_static":
        color_static()
    elif example == "stars":
        stars()
    else:
        print("Usage: python3 examples.py <example>")
        print("\nExample can be one of:\n")
        print("single_point: ", single_point.__doc__)
        print("square: ", square.__doc__)
        print("diagonal: ", diagonal.__doc__)
        print("static: ", static.__doc__)
        print("color_static: ", color_static.__doc__)
        print("stars: ", stars.__doc__)