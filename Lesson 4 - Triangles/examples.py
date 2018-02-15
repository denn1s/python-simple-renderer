import sys
import random
from gl import Render


def cube():
    """
    Draws a cube at an angle so it is more interesting
    """
    r = Render(800, 600)
    r.load('./cube2.obj', (4, 3, 3), (100, 100, 100))
    # r.display()
    r.write('out.bmp')


def bears():
    """
    Draws some bears on top of each other (doesn't work)
    """
    r = Render(800, 600)
    r.load('./bears.obj', (9, 2, 0), (40, 40, 40))
    # r.display()
    r.write('out.bmp')


def face():
    """
    Draws a cute face, now 30% less creepy!
    """
    r = Render(800, 600)
    r.load('./face.obj', (25, 5, 0), (15, 15, 15))
    # r.display()
    r.write('out.bmp')


if __name__ == "__main__":
    example = sys.argv[1] if len(sys.argv) > 1 else ""

    elif example == "cube":
        cube()
    elif example == "bears":
        bears()
    elif example == "face":
        face()
    else:
        print("Usage: python3 examples.py <example>")
        print("\nExample can be one of:\n")
        print("simple_cube: ", simple_cube.__doc__)
        print("cube: ", cube.__doc__)
        print("bears: ", bears.__doc__)
        print("face: ", face.__doc__)
        
