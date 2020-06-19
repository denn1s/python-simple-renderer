import sys
import random
from gl import Render


def cube():
    """
    Draws a cube at an angle so it is more interesting
    """
    r = Render(800, 600)
    r.load('./models/cube2.obj', (4, 3, 3), (100, 100, 100))
    r.display('out.bmp')

def face():
    """
    Draws a cute face, now 30% less creepy!
    """
    r = Render(800, 600)
    r.load('./models/face.obj', (25, 5, 0), (15, 15, 15))
    r.display('out.bmp')


def model():
    r = Render(800, 600)
    r.load('./models/model.obj', (1, 1, 1), (300, 300, 300))
    r.display('out.bmp')

def figures():
    """
    Draws a cute face, now 30% less creepy!
    """
    r = Render(800, 600)
    r.load('./models/figures.obj', (3, 1, 1), (100, 100, 100))
    r.display('out.bmp')

if __name__ == "__main__":
    example = sys.argv[1] if len(sys.argv) > 1 else ""

    if example == "cube":
        cube()
    elif example == "face":
        face()
    elif example == "model":
        model()
    elif example == "figures":
        figures()
    else:
        print("Usage: python3 examples.py <example>")
        print("\nExample can be one of:\n")
        print("cube: ", cube.__doc__)
        print("face: ", face.__doc__)
        
