import sys
import random
from gl import Render, V2, color


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
    """
    Draws a face, now 30% less cute
    """
    r = Render(800, 600)
    r.load('./models/model.obj', (25, 5, 0), (15, 15, 15))
    r.display('out.bmp')


def triangle():
    """
    Draws triangles
    """
    r = Render(200, 200)
    r.triangle(V2(10, 70),  V2(50, 160), V2(70, 80), color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    r.triangle(V2(180, 50), V2(150, 1),  V2(70, 180), color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    r.triangle(V2(180, 150), V2(120, 160), V2(130, 180), color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    r.display('out.bmp')


if __name__ == "__main__":
    example = sys.argv[1] if len(sys.argv) > 1 else ""

    if example == "cube":
        cube()
    elif example == "face":
        face()
    elif example == "model":
        model()
    elif example == "triangle":
        triangle()
    else:
        print("Usage: python3 examples.py <example>")
        print("\nExample can be one of:\n")
        print("cube: ", cube.__doc__)
        print("face: ", face.__doc__)
        
