import struct
import random
import numpy as np
from obj import Obj, Texture
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
    Input: 1 size 3 vector and a scakar
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
  v0 = V3(*v0)
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

def barycentric(A, B, C, P):
  """
    Input: 3 size 2 vectors and a point
    Output: 3 barycentric coordinates of the point in relation to the triangle formed
            * returns -1, -1, -1 for degenerate triangles
  """  
  bary = cross(
    V3(C.x - A.x, B.x - A.x, A.x - P.x), 
    V3(C.y - A.y, B.y - A.y, A.y - P.y)
  )

  if abs(bary[2]) < 1:
    return -1, -1, -1   # this triangle is degenerate, return anything outside

  return (
    1 - (bary[0] + bary[1]) / bary[2], 
    bary[1] / bary[2], 
    bary[0] / bary[2]
  )

def ndc(point):
  point = V3(*point)
  return V3(
    point.x / point.z,
    point.y / point.z,
    point.z / point.z
  )


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
    self.texture = None
    self.shader = None
    self.normalmap = None

  def clear(self):
    self.pixels = [
      [BLACK for x in range(self.width)] 
      for y in range(self.height)
    ]
    self.zbuffer = [
      [-float('inf') for x in range(self.width)]
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
      start: size n array with x,y coordinates
      end: size n array with x,y coordinates
    """
    start = V2(*start[:2])
    end = V2(*end[:2])
    x1, y1 = int(start.x), int(start.y)
    x2, y2 = int(end.x), int(end.y)

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


  def triangle(self, A, B, C, color=None, texture_coords=(), varying_normals=()):
    bbox_min, bbox_max = bbox(A, B, C)

    for x in range(bbox_min.x, bbox_max.x + 1):
      for y in range(bbox_min.y, bbox_max.y + 1):
        w, v, u = barycentric(A, B, C, V2(x, y))
        if w < 0 or v < 0 or u < 0:  # 0 is actually a valid value! (it is on the edge)
          continue
        
        color = self.shader(self,
            triangle=(A, B, C),
            bar=(w, v, u),
            varying_normals=varying_normals,
            texture_coords=texture_coords)

        z = A.z * w + B.z * v + C.z * u

        if x < len(self.zbuffer) and y < len(self.zbuffer[x]) and z > self.zbuffer[x][y]:
          self.point(x, y, color)
          self.zbuffer[x][y] = z

  def transform(self, vertex, translate=(0, 0, 0), scale=(1, 1, 1)):
    
    View = self.View  # transforms model coordinates to eye coordinates
    Projection = self.Projection  # deforma la escena para crear una proyección (clip coordinates)
    Viewport = self.ViewPort  # transforms clip coordinates to screen coordinates

    augmented_vertex = [
      vertex.x,
      vertex.y,
      vertex.z,
      1
    ]

    transformed_vertex = np.dot(
      Viewport @ Projection @ View,
      augmented_vertex
    ).tolist()[0]

    return V3(
      round(transformed_vertex[0] / transformed_vertex[3]),
      round(transformed_vertex[1] / transformed_vertex[3]),
      round(transformed_vertex[2] / transformed_vertex[3])
    )

  def lookAt(self, eye, center, up):
    z = norm(sub(eye, center))
    x = norm(cross(up, z))
    y = norm(cross(z, x))

    self.View = np.matrix([
      [x.x, x.y, x.z, -center.x],
      [y.x, y.y, y.z, -center.y],
      [z.x, z.y, z.z, -center.z],
      [0, 0, 0, 1]
    ])

    self.projection(-1/(length(sub(eye, center))))
    self.viewport()

  def projection(self, coeff):
    self.Projection = np.matrix([
      [1, 0, 0, 0],
      [0, 1, 0, 0],
      [0, 0, 1, 0],
      [0, 0, coeff, 1]
    ])

  def viewport(self):
    self.ViewPort = np.matrix([
      [200, 0, 0, 400],
      [0, 200, 0, 300],
      [0, 0, 128, 128],
      [0, 0, 0, 1]
    ])
    
  def load(self, filename, translate=(0, 0, 0), scale=(1, 1, 1), 
            texture=None, shader=None, normalmap=None):
    """
    Loads an obj file in the screen
    Input: 
      filename: the full path of the obj file
      translate: (translateX, translateY) how much the model will be translated during render
      scale: (scaleX, scaleY) how much the model should be scaled
      texture: texture file to use
    """
    model = Obj(filename)
    self.light = norm(self.light)
    self.texture = texture
    self.shader = shader
    self.normalmap = normalmap

    for face in model.faces:
        vcount = len(face)

        if vcount == 3:
          f1 = face[0][0] - 1
          f2 = face[1][0] - 1
          f3 = face[2][0] - 1

          a = self.transform(V3(*model.vertices[f1]), translate, scale)
          b = self.transform(V3(*model.vertices[f2]), translate, scale)
          c = self.transform(V3(*model.vertices[f3]), translate, scale)

          n1 = face[0][2] - 1
          n2 = face[1][2] - 1
          n3 = face[2][2] - 1      
          nA = V3(*model.normals[n1])
          nB = V3(*model.normals[n2])
          nC = V3(*model.normals[n3])

          t1 = face[0][1] - 1
          t2 = face[1][1] - 1
          t3 = face[2][1] - 1
          tA = V3(*model.tvertices[t1])
          tB = V3(*model.tvertices[t2])
          tC = V3(*model.tvertices[t3])

          self.triangle(a, b, c, texture_coords=(tA, tB, tC), varying_normals=(nA, nB, nC))
          
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
        
          self.triangle(A, B, C, color(grey, grey, grey))
          self.triangle(A, C, D, color(grey, grey, grey))

