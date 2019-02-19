import struct
import random
import numpy
from obj import Obj
from collections import namedtuple

# ===============================================================
# Math
# ===============================================================

V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])


def sum(v0, v1):
  """
    Input: 2 size 3 vectors
    Output: Size 3 vector with the per element sum
  """
  return V3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)

def sub(v0, v1):
  """
    Input: 2 size 3 vectors
    Output: Size 3 vector with the per element substraction
  """
  return V3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)

def mul(v0, k):
  """
    Input: 2 size 3 vectors
    Output: Size 3 vector with the per element multiplication
  """  
  return V3(v0.x * k, v0.y * k, v0.z *k)

def dot(v0, v1):
  """
    Input: 2 size 3 vectors
    Output: Scalar with the dot product
  """
  return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

def cross(v0, v1):
  """
    Input: 2 size 3 vectors
    Output: Size 3 vector with the cross product
  """
  return V3(
    v0.y * v1.z - v0.z * v1.y,
    v0.z * v1.x - v0.x * v1.z,
    v0.x * v1.y - v0.y * v1.x,
  )

def length(v0):
  """
    Input: 1 size 3 vector
    Output: Scalar with the length of the vector
  """  
  return (v0.x**2 + v0.y**2 + v0.z**2)**0.5

def norm(v0):
  """
    Input: 1 size 3 vector
    Output: Size 3 vector with the normal of the vector
  """  
  v0length = length(v0)

  if not v0length:
    return V3(0, 0, 0)

  return V3(v0.x/v0length, v0.y/v0length, v0.z/v0length)

def bbox(*vertices):
  """
    Input: n size 2 vectors
    Output: 2 size 2 vectors defining the smallest bounding rectangle possible
  """  
  xs = [ vertex.x for vertex in vertices ]
  ys = [ vertex.y for vertex in vertices ]
  xs.sort()
  ys.sort()

  return V2(xs[0], ys[0]), V2(xs[-1], ys[-1])

# ===============================================================
# Utils
# ===============================================================


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

  def display(self, filename='out.bmp'):
    """
    Displays the image, a external library (wand) is used, but only for convenience during development
    """
    self.write(filename)

    try:
      from wand.image import Image
      from wand.display import display

      with Image(filename=filename) as image:
        display(image)
    except ImportError:
      pass  # do nothing if no wand is installed

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
    x1, y1 = start.x, start.y
    x2, y2 = end.x, end.y

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

  def triangle1(self, A, B, C, color=None):
    # paso 1, ordenamos los vertices en orden ascendiente
    if A.y > B.y:
      A, B = B, A
    if A.y > C.y:
      A, C = C, A
    if B.y > C.y:
      B, C = C, B

    self.line(A, B, color)
    self.line(B, C, color)
    self.line(C, A, color)

  def triangle2(self, A, B, C, color=None):
    # paso 2, partimos el triangulo a la mitad
    if A.y > B.y:
      A, B = B, A
    if A.y > C.y:
      A, C = C, A
    if B.y > C.y:
      B, C = C, B

    dx_ac = C.x - A.x
    dy_ac = C.y - A.y

    mi_ac = dx_ac/dy_ac

    dx_ab = B.x - A.x
    dy_ab = B.y - A.y

    mi_ab = dx_ab/dy_ab

    for y in range(A.y, B.y + 1):
        xi = round(A.x - mi_ac * (A.y - y))
        xf = round(A.x - mi_ab * (A.y - y))

        self.point(xi, y)
        self.point(xf, y)

  def triangle3(self, A, B, C, color=None):
    # paso 3, llenemos el triangulo!
    if A.y > B.y:
      A, B = B, A
    if A.y > C.y:
      A, C = C, A
    if B.y > C.y:
      B, C = C, B

    dx_ac = C.x - A.x
    dy_ac = C.y - A.y

    mi_ac = dx_ac/dy_ac

    dx_ab = B.x - A.x
    dy_ab = B.y - A.y

    mi_ab = dx_ab/dy_ab

    for y in range(A.y, B.y + 1):
        xi = round(A.x - mi_ac * (A.y - y))
        xf = round(A.x - mi_ab * (A.y - y))

        if xi > xf:
            xi, xf = xf, xi
        for x in range(xi, xf + 1):
            self.point(x, y, color)


  def triangle(self, A, B, C, color=None):
    if A.y > B.y:
      A, B = B, A
    if A.y > C.y:
      A, C = C, A
    if B.y > C.y: 
      B, C = C, B

    dx_ac = C.x - A.x
    dy_ac = C.y - A.y
    if dy_ac == 0:
        return
    mi_ac = dx_ac/dy_ac

    dx_ab = B.x - A.x
    dy_ab = B.y - A.y
    if dy_ab != 0:
        mi_ab = dx_ab/dy_ab

        for y in range(A.y, B.y + 1):
            xi = round(A.x - mi_ac * (A.y - y))
            xf = round(A.x - mi_ab * (A.y - y))

            if xi > xf:
                xi, xf = xf, xi
            for x in range(xi, xf + 1):
                self.point(x, y, color)

    dx_bc = C.x - B.x
    dy_bc = C.y - B.y
    if dy_bc:
        mi_bc = dx_bc/dy_bc

        # dacx = C.x - A.x
        # dacy = C.y - A.y
        # miac = dacx/dacy  // we have mi_ac already!

        for y in range(B.y, C.y + 1):
            xi = round(A.x - mi_ac * (A.y - y))
            xf = round(B.x - mi_bc * (B.y - y))

            if xi > xf:
                xi, xf = xf, xi
            for x in range(xi, xf + 1):
                self.point(x, y, color)

  def transform(self, vertex, translate=(0, 0, 0), scale=(1, 1, 1)):
    # returns a vertex 3, translated and transformed
    return V3(
      round((vertex[0] + translate[0]) * scale[0]),
      round((vertex[1] + translate[1]) * scale[1]),
      round((vertex[2] + translate[2]) * scale[2])
    )

  def load(self, filename, translate=(0, 0, 0), scale=(1, 1, 1)):
    """
    Loads an obj file in the screen
    wireframe only
    Input: 
      filename: the full path of the obj file
      translate: (translateX, translateY) how much the model will be translated during render
      scale: (scaleX, scaleY) how much the model should be scaled
    """
    model = Obj(filename)

    light = V3(0,0,1)

    for face in model.vfaces:
        vcount = len(face)

        if vcount == 3:
          f1 = face[0][0] - 1
          f2 = face[1][0] - 1
          f3 = face[2][0] - 1

          a = self.transform(model.vertices[f1], translate, scale)
          b = self.transform(model.vertices[f2], translate, scale)
          c = self.transform(model.vertices[f3], translate, scale)

          self.triangle(a, b, c, color(255 * random.random(), 255 * random.random(), 255 * random.random()))
        else:
          # assuming 4
          f1 = face[0][0] - 1
          f2 = face[1][0] - 1
          f3 = face[2][0] - 1
          f4 = face[3][0] - 1   

          vertices = [
            self.transform(model.vertices[f1], translate, scale),
            self.transform(model.vertices[f2], translate, scale),
            self.transform(model.vertices[f3], translate, scale),
            self.transform(model.vertices[f4], translate, scale)
          ]

          normal = norm(cross(sub(vertices[0], vertices[1]), sub(vertices[1], vertices[2])))  # no necesitamos dos normales!!
          intensity = dot(normal, light)
          grey = round(255 * intensity)
          if grey < 0:
            continue # dont paint this face

          # vertices are ordered, no need to sort!
          # vertices.sort(key=lambda v: v.x + v.y)

          A, B, C, D = vertices

          self.triangle2(A, B, C, color(grey, grey, grey))
          self.triangle2(A, C, D, color(grey, grey, grey))

