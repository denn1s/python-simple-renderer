import random
import numpy
from numpy import matrix, cos, sin, tan
from obj import Obj, Texture
from lib import *

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
    self.light = V3(0,0,1)
    self.active_texture = None
    self.active_vertex_array = []

  def clear(self):
    self.pixels = [
      [BLACK for x in range(self.width)]
      for y in range(self.height)
    ]
    self.zbuffer = numpy.full((self.height, self.width), -numpy.inf)

  def write(self, filename):
    writebmp(filename, self.width, self.height, self.pixels)

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

  def triangle(self):
    A = next(self.active_vertex_array)
    B = next(self.active_vertex_array)
    C = next(self.active_vertex_array)

    if self.active_texture:
      tA = next(self.active_vertex_array)
      tB = next(self.active_vertex_array)
      tC = next(self.active_vertex_array)

    nA = next(self.active_vertex_array)
    nB = next(self.active_vertex_array)
    nC = next(self.active_vertex_array)

    bbox_min, bbox_max = bbox(A, B, C)

    normal = norm(cross(sub(B, A), sub(C, A)))
    intensity = dot(normal, self.light)
    if intensity < 0:
      return

    for x in range(bbox_min.x, bbox_max.x + 1):
      for y in range(bbox_min.y, bbox_max.y + 1):
        w, v, u = barycentric(A, B, C, V2(x, y))
        if w < 0 or v < 0 or u < 0:  # 0 is actually a valid value! (it is on the edge)
          continue

        if self.active_texture:
          tx = tA.x * w + tB.x * v + tC.x * u
          ty = tA.y * w + tB.y * v + tC.y * u

        color = self.active_shader(
            self,
            triangle=(A, B, C),
            bar=(w, v, u),
            texture_coords=(tx, ty),
            varying_normals=(nA, nB, nC)
        )

        # color = self.active_texture.get_color(tx, ty, intensity)

        z = A.z * w + B.z * v + C.z * u

        if x < 0 or y < 0:
          continue

        if x < len(self.zbuffer) and y < len(self.zbuffer[x]) and z > self.zbuffer[x][y]:
          self.point(x, y, color)
          self.zbuffer[x][y] = z

  def transform(self, vertex):
    augmented_vertex = [
      vertex.x,
      vertex.y,
      vertex.z,
      1
    ]
    tranformed_vertex = self.Viewport @ self.Projection @ self.View @ self.Model @ augmented_vertex

    tranformed_vertex = tranformed_vertex.tolist()[0]

    tranformed_vertex = [
      (tranformed_vertex[0]/tranformed_vertex[3]),
      (tranformed_vertex[1]/tranformed_vertex[3]),
      (tranformed_vertex[2]/tranformed_vertex[3])
    ]
    print(V3(*tranformed_vertex))
    return V3(*tranformed_vertex)

  def load(self, filename, translate=(0, 0, 0), scale=(1, 1, 1), rotate=(0, 0, 0)):
    self.loadModelMatrix(translate, scale, rotate)

    model = Obj(filename)
    vertex_buffer_object = []

    for face in model.faces:
        for facepart in face:
          vertex = self.transform(V3(*model.vertices[facepart[0]]))
          vertex_buffer_object.append(vertex)

        if self.active_texture:
          for facepart in face:
            tvertex = V3(*model.tvertices[facepart[1]])
            vertex_buffer_object.append(tvertex)

          for facepart in face:
            nvertex = V3(*model.normals[facepart[2]])
            vertex_buffer_object.append(nvertex)

    self.active_vertex_array = iter(vertex_buffer_object)

  def loadModelMatrix(self, translate=(0, 0, 0), scale=(1, 1, 1), rotate=(0, 0, 0)):
    translate = V3(*translate)
    scale = V3(*scale)
    rotate = V3(*rotate)

    translation_matrix = matrix([
      [1, 0, 0, translate.x],
      [0, 1, 0, translate.y],
      [0, 0, 1, translate.z],
      [0, 0, 0, 1],
    ])


    a = rotate.x
    rotation_matrix_x = matrix([
      [1, 0, 0, 0],
      [0, cos(a), -sin(a), 0],
      [0, sin(a),  cos(a), 0],
      [0, 0, 0, 1]
    ])

    a = rotate.y
    rotation_matrix_y = matrix([
      [cos(a), 0,  sin(a), 0],
      [     0, 1,       0, 0],
      [-sin(a), 0,  cos(a), 0],
      [     0, 0,       0, 1]
    ])

    a = rotate.z
    rotation_matrix_z = matrix([
      [cos(a), -sin(a), 0, 0],
      [sin(a),  cos(a), 0, 0],
      [0, 0, 1, 0],
      [0, 0, 0, 1]
    ])

    rotation_matrix = rotation_matrix_x @ rotation_matrix_y @ rotation_matrix_z

    scale_matrix = matrix([
      [scale.x, 0, 0, 0],
      [0, scale.y, 0, 0],
      [0, 0, scale.z, 0],
      [0, 0, 0, 1],
    ])

    self.Model = translation_matrix @ rotation_matrix @ scale_matrix

  def loadViewMatrix(self, x, y, z, center):
    M = matrix([
      [x.x, x.y, x.z,  0],
      [y.x, y.y, y.z, 0],
      [z.x, z.y, z.z, 0],
      [0,     0,   0, 1]
    ])

    O = matrix([
      [1, 0, 0, -center.x],
      [0, 1, 0, -center.y],
      [0, 0, 1, -center.z],
      [0, 0, 0, 1]
    ])

    self.View = M @ O

  def loadProjectionMatrix(self, coeff):
    self.Projection =  matrix([
      [1, 0, 0, 0],
      [0, 1, 0, 0],
      [0, 0, 1, 0],
      [0, 0, coeff, 1]
    ])

  def loadViewportMatrix(self, x = 0, y = 0):
    self.Viewport =  matrix([
      [self.width/2, 0, 0, x + self.width/2],
      [0, self.height/2, 0, y + self.height/2],
      [0, 0, 128, 128],
      [0, 0, 0, 1]
    ])

  def lookAt(self, eye, center, up):
    z = norm(sub(eye, center))
    x = norm(cross(up, z))
    y = norm(cross(z, x))
    self.loadViewMatrix(x, y, z, center)
    self.loadProjectionMatrix(-1 / length(sub(eye, center)))
    self.loadViewportMatrix()

  def draw_arrays(self, polygon):
    if polygon == 'TRIANGLES':
      try:
        while True:
          self.triangle()
      except StopIteration:
        print('Done.')


