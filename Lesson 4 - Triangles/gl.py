import struct
from obj import Obj
from collections import namedtuple

# ===============================================================
# Utilities
# ===============================================================

Vertex2 = namedtuple('Point', ['x', 'y'])
Vertex3 = namedtuple('Point', ['x', 'y', 'z'])


def sum(v0, v1):
  return Vertex3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)

def sub(v0, v1):
  return Vertex3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)


def mul(v0, k):
  return Vertex3(v0.x * k, v0.y * k, v0.z *k)


def dot(v0, v1):
  return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z


def cross(v0, v1):
  return Vertex3(
    v0.y * v1.z - v0.z * v1.y,
    v0.z * v1.x - v0.x * v1.z,
    v0.x * v1.y - v0.y * v1.x,
  )

def length(v0):
  return (v0.x**2 + v0.y**2 + v0.z**2)**0.5


def norm(v0):
  v0length = length(v0)
  return Vertex3(v0.x/v0length, v0.y/v0length, v0.z/v0length)

def bbox(A, B, C):
  xs = [ A.x, B.x, C.x ]
  ys = [ A.y, B.y, C.y ]
  zs = [ A.z, B.z, C.z ]

  mins = [ min(xs), min(ys), min(zs) ]
  maxs = [ max(xs), max(ys), max(zs) ]

  return mins, maxs


def barycentric(A, B, C, P):
  bary = cross(Vertex3(C.x - A.x, B.x - A.x, P.x - A.x), 
            Vertex3(C.y - A.y, B.y - A.y, P.y - A.y))

  return 1 - (bary.x + bary.y) / bary.z, (bary.y / bary.z), (bary.x / bary.z)


b = barycentric(Vertex3(0, 0, 0), 
                Vertex3(50, 50, 0), 
                Vertex3(100, 0, 0), 
                Vertex3(25, 50, 0))

print(b)









































def char(c):
  """
  Input: requires a size 1 string
  Output: 1 byte of the ascii encoded char 
  """
  return struct.pack('=c', c.encode('ascii'))

def word(w):
  """
  Input: requires a number such that (-0x7fff - 1) <= number <= 0x7fff
         ie. (-32768, 32767)
  Output: 2 bytes

  Example:  
  >>> struct.pack('=h', 1)
  b'\x01\x00'
  """
  return struct.pack('=h', w)

def dword(d):
  """
  Input: requires a number such that -2147483648 <= number <= 2147483647
  Output: 4 bytes

  Example:
  >>> struct.pack('=l', 1)
  b'\x01\x00\x00\x00'
  """
  return struct.pack('=l', d)

def color(r, g, b):
  """
  Input: each parameter must be a number such that 0 <= number <= 255
         each number represents a color in rgb 
  Output: 3 bytes

  Example:
  >>> bytes([0, 0, 255])
  b'\x00\x00\xff'
  """
  return bytes([b, g, r])


# ===============================================================
# Constants
# ===============================================================

BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)


# ===============================================================
# Renders a BMP file
# ===============================================================

class Render(object):
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.current_color = WHITE
    self.clear()

  def clear(self):
    self.pixels = [
      [BLACK for x in range(self.width)] 
      for y in range(self.height)
    ]

  def write(self, filename):
    f = open(filename, 'bw')

    # File header (14 bytes)
    f.write(char('B'))
    f.write(char('M'))
    f.write(dword(14 + 40 + self.width * self.height * 3))
    f.write(dword(0))
    f.write(dword(14 + 40))

    # Image header (40 bytes)
    f.write(dword(40))
    f.write(dword(self.width))
    f.write(dword(self.height))
    f.write(word(1))
    f.write(word(24))
    f.write(dword(0))
    f.write(dword(self.width * self.height * 3))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))

    # Pixel data (width x height x 3 pixels)
    for x in range(self.height):
      for y in range(self.width):
        f.write(self.pixels[x][y])

    f.close()

  def display(self):
    """
    Displays the image, a external library (wand) is used, but only for convenience during development
    """
    filename = 'out.bmp'
    self.write(filename)

    from wand.image import Image
    from wand.display import display

    with Image(filename=filename) as image:
      display(image)

  def set_color(self, color):
    self.current_color = color

  def point(self, x, y, color = None):
    # 0,0 was intentionally left in the bottom left corner to mimic opengl
    try:
      self.pixels[y][x] = color or self.current_color
    except:
      # To avoid index out of range exceptions
      pass
    
  def line(self, start, end, color = None):
    """
    Draws a line in the screen.
    Input: 
      start: size 2 array with x,y coordinates
      end: size 2 array with x,y coordinates
    """
    x1, y1 = start
    x2, y2 = end

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
    for x in range(x1, x2 + 1):
        if steep:
            self.point(y, x, color)
        else:
            self.point(x, y, color)
        
        offset += dy * 2
        if offset >= threshold:
            y += 1 if y1 < y2 else -1
            threshold += dx * 2

  def triangle(self, a, b, c, color=None):
    a = Vertex2(*a)
    b = Vertex2(*b)
    c = Vertex2(*c)

    if a.y > b.y:
        a, b = b, a
    if a.y > c.y:
        a, c = c, a
    if b.y > c.y: 
        b, c = c, b

    dx_ac = c.x - a.x
    dy_ac = c.y - a.y
    if dy_ac == 0:
        return
    mi_ac = dx_ac/dy_ac

    dx_ab = b.x - a.x
    dy_ab = b.y - a.y
    if dy_ab != 0:
        mi_ab = dx_ab/dy_ab

        for y in range(a.y, b.y + 1):
            xi = round(a.x - mi_ac * (a.y - y))
            xf = round(a.x - mi_ab * (a.y - y))
            if xi > xf:
                xi, xf = xf, xi
            for x in range(xi, xf + 1):
                r.point(x, y, color)

    dx_bc = c.x - b.x
    dy_bc = c.y - b.y
    if dy_bc:
        mi_bc = dx_bc/dy_bc
        for y in range(b.y, c.y + 1):
            xi = round(a.x - mi_ac * (a.y - y))
            xf = round(b.x - mi_bc * (b.y - y))
            if xi > xf:
                xi, xf = xf, xi
            for x in range(xi, xf + 1):
                r.point(x, y, color)

    
  def load(self, filename, translate=(0, 0), scale=(1, 1)):
    """
    Loads an obj file in the screen
    wireframe only
    Input: 
      filename: the full path of the obj file
      translate: (translateX, translateY) how much the model will be translated during render
      scale: (scaleX, scaleY) how much the model should be scaled
    """
    model = Obj(filename)

    import random

    for face in model.vfaces:
        vcount = len(face)

        if vcount == 3:
          f1 = face[0][0] - 1
          f2 = face[1][0] - 1
          f3 = face[2][0] - 1

          a = [ round((v+1) * 400) for v in model.vertices[f1] ][:2]
          b = [ round((v+1) * 400) for v in model.vertices[f2] ][:2]
          c = [ round((v+1) * 400) for v in model.vertices[f3] ][:2]

          self.triangle(a, b, c, color(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)))
        else:
          print('vcount is ', vcount)

        """
        for j in range(vcount):
            f1 = face[j][0]
            f2 = face[(j+1)%vcount][0]

            v1 = model.vertices[f1 - 1]
            v2 = model.vertices[f2 - 1]

            scaleX, scaleY = scale
            translateX, translateY = translate

            x1 = round((v1[0] + translateX) * scaleX); 
            y1 = round((v1[1] + translateY) * scaleY); 
            x2 = round((v2[0] + translateX) * scaleX); 
            y2 = round((v2[1] + translateY) * scaleY); 
      
            self.line((x1, y1), (x2, y2))
        """


r = Render(800, 600)
r.load('./model.obj')
r.display()