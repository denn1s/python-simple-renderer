import sys
import random
from gl import Render, color


def single_line():
    """
    Draws a single line in the screen (lower left corner)
    """
    r = Render(800, 600)
    r.line((10, 10),  (510, 10))
    r.write('out.bmp')


def multi_line():
    """
    Draws lines from every corner
    """
    r = Render(800, 600)
    r.line((10, 10), (510, 10))
    r.line((10, 10), (462, 191))
    r.line((10, 10), (354, 354))
    r.line((10, 10), (191, 462))
    r.line((10, 10), (10, 510))
    r.line((790, 590), (790, 90))  
    r.line((790, 590), (609, 138))
    r.line((790, 590), (446, 246))
    r.line((790, 590), (338, 409))
    r.line((790, 590), (290, 590))
    r.line((10, 590), (510, 590))
    r.line((10, 590), (462, 409))
    r.line((10, 590), (354, 246))
    r.line((10, 590), (191, 138))
    r.line((10, 590), (10, 90))
    r.line((790, 10), (790, 510))  
    r.line((790, 10), (609, 462))
    r.line((790, 10), (446, 354))
    r.line((790, 10), (338, 191))
    r.line((790, 10), (290, 10))
    r.write('out.bmp')


def cube():
    """
    Draws a cube 
    """
    r = Render(400, 400)

    r.line((100, 100), (200, 100))
    r.line((100, 100), (100, 200))
    r.line((200, 100), (200, 200))
    r.line((100, 200), (200, 200))

    r.line((150, 150), (250, 150))
    r.line((150, 150), (150, 250))
    r.line((250, 150), (250, 250))
    r.line((150, 250), (250, 250))

    r.line((100, 100), (150, 150))
    r.line((100, 200), (150, 250))
    r.line((200, 100), (250, 150))
    r.line((200, 200), (250, 250))

    r.write('out.bmp')


def isometric_cube():
    """
    Draws a isometric cube
    """
    r = Render(600, 600)

    r.line((200, 200), (287, 250))
    r.line((200, 200), (113, 250))
    r.line((200, 200), (200, 300))
    r.line((287, 250), (287, 350))
    r.line((113, 250), (113, 350))
    r.line((200, 300), (287, 350))
    r.line((200, 300), (113, 350))
    r.line((287, 350), (200, 400))
    r.line((113, 350), (200, 400))

    r.write('out.bmp')


if __name__ == "__main__":
    example = sys.argv[1] if len(sys.argv) > 1 else ""
    if example == "single_line":
        single_line()
    elif example == "multi_line":
        multi_line()
    elif example == "cube":
        cube()
    elif example == "isometric_cube":
        isometric_cube()
    else:
        print("Usage: python3 examples.py <example>")
        print("\nExample can be one of:\n")
        print("single_line: ", single_line.__doc__)
        print("multi_line: ", multi_line.__doc__)
        print("cube: ", cube.__doc__)
        print("isometric_cube: ", isometric_cube.__doc__)
