import sys
import random
from gl import Render
from obj import Texture

def model():
    """
    Draws a cube at an angle so it is more interesting
    """
    r = Render(800, 600)
    t = Texture('./models/model.bmp')
    r.active_texture = t
    r.load('./models/model.obj', (1, 1, 1), (300, 300, 300))
    r.draw_arrays('TRIANGLES')
    r.display('out.bmp')


if __name__ == "__main__":
    model()
