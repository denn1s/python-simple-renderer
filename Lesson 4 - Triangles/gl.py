import struct
import random
import numpy
from obj import Obj
from collections import namedtuple

# ===============================================================
# Utilities
# ===============================================================


V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])


def sum(v0, v1):
  return V3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)

def sub(v0, v1):
  return V3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)


def mul(v0, k):
  return V3(v0.x * k, v0.y * k, v0.z *k)


def dot3(v0, v1):
  return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z


def dot2(v0, v1):
  return v0.x * v1.x + v0.y * v1.y



def cross(v0, v1):
  return V3(
    v0.y * v1.z - v0.z * v1.y,
    v0.z * v1.x - v0.x * v1.z,
    v0.x * v1.y - v0.y * v1.x,
  )

def length3(v0):
  return (v0.x**2 + v0.y**2 + v0.z**2)**0.5

def length2(v0):
  return (v0.x**2 + v0.y**2)**0.5


def norm2(v0):
  v0length = length2(v0)

  if not v0length:
    return V2(0, 0)

  return V2(v0.x/v0length, v0.y/v0length)


def norm3(v0):
  v0length = length3(v0)

  if not v0length:
    return V3(0, 0, 0)

  return V3(v0.x/v0length, v0.y/v0length, v0.z/v0length)



def bbox(A, B, C):
  xs = [ A.x, B.x, C.x ]
  ys = [ A.y, B.y, C.y ]

  return V2(min(xs), min(ys)), V2(max(xs), max(ys))


def bbox3(A, B, C):
  xs = [ A.x, B.x, C.x ]
  ys = [ A.y, B.y, C.y ]
  zs = [ A.z, B.z, C.z ]

  mins = [ min(xs), min(ys), min(zs) ]
  maxs = [ max(xs), max(ys), max(zs) ]

  return V3(mins), V3(maxs)

# import numpy

def barycentric(A, B, C, P):
  bary = cross(
    V3(C.x - A.x, B.x - A.x, A.x - P.x), 
    V3(C.y - A.y, B.y - A.y, A.y - P.y)
  )

  if bary[2] <= 0:
    return -1, 1, 1

  return 1 - (bary[0] + bary[1]) / bary[2], bary[1] / bary[2], bary[0] / bary[2]


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


  def triangle_wireframe(self, A, B, C, color = None):
    r.line(A, B, color)
    r.line(B, C, color)
    r.line(C, A, color)


  def triangle(self, A, B, C, color=None):
    bbox_min, bbox_max = bbox(A, B, C)

    try:
      matrix = numpy.linalg.inv([
        [ A.x, B.x, C.x ], 
        [ A.y, B.y, C.y ], 
        [ 1, 1, 1 ]
      ])
    except:
      return

    for x in range(bbox_min.x, bbox_max.x + 1):
      for y in range(bbox_min.y, bbox_max.y + 1):
        # w, v, u = barycentric(A, B, C, V3(x, y, 1))
        w, v, u = numpy.dot(matrix, [x, y, 1])
        if w > 0 and v > 0 and u > 0:
          r.point(x, y, color)


  def triangle2(self, a, b, c, color = None):
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

            for x in range(xi, xf):
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

            for x in range(xi, xf):
                r.point(x, y, color)

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

          normal = norm3(cross(sub(b, a), sub(c, a)))
          intensity = dot3(normal, light)
          grey = round(255 * intensity)
          if grey < 0:
            grey = 0
          if grey > 255:
            grey = 255        
          if not grey:
            continue  
          
          self.triangle2(a, b, c, color(grey, grey, grey))
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

          normal = norm3(cross(sub(vertices[0], vertices[1]), sub(vertices[1], vertices[2])))  # no necesitamos dos normales!!
          intensity = dot3(normal, light)
          grey = round(255 * intensity)
          if grey < 0:
            grey = 0
          if grey > 255:
            grey = 255
          
          if not grey:
            continue # dont paint this face


          vertices.sort(key=lambda v: v.x + v.y)

          # print(vertices)
  
          A, B, C, D = vertices 
          # A is smallest, D is largest
        
          self.triangle2(A, B, D, color(grey, grey, grey))
          self.triangle2(A, D, C, color(grey, grey, grey))

r = Render(800, 600)
# r.load('./cube2.obj', (4, 3, 3), (100, 100, 100))
# r.load('./bears.obj', (9, 2, 0), (40, 40, 40))
r.load('./face.obj', (25, 5, 0), (15, 15, 15))
# r.load('./model.obj', (1, 1, 1), (400, 400, 400))
r.write('./out.bmp')