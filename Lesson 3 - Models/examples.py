import sys
import random
from gl import Render


def simple_cube():
    """
    Draws a cube, but an orthogonal cube, so a square
    """
    r = Render(800, 600)
    r.load('./models/cube.obj', (4, 3), (100, 100))
    # r.display()
    r.display('out.bmp')


def cube():
    """
    Draws a cube at an angle so it is more interesting
    """
    r = Render(800, 600)
    r.load('./models/cube2.obj', (4, 3), (100, 100))
    # r.display()
    r.display('out.bmp')


def bears():
    """
    Draws some bears on top of each other
    """
    r = Render(800, 600)
    r.load('./models/bears.obj', (9, 2), (40, 40))
    # r.display()
    r.display('out.bmp')


def face():
    """
    Draws a cute face, but in wireframe it just looks creepy
    """
    r = Render(800, 600)
    r.load('./models/face.obj', (25, 5), (15, 15))
    r.display()
    r.display('out.bmp')


if __name__ == "__main__":
    example = sys.argv[1] if len(sys.argv) > 1 else ""
    if example == "simple_cube":
        simple_cube()
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
        
