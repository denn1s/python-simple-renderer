import numpy as np
from gl import *

points = [
  (165, 380), (185, 360), (180, 330), (207, 345), (233, 330), (230, 360), (250, 380), (220, 385), (205, 410), (193, 383)
]

pt = np.transpose(points)
center = V2(
  (min(pt[0]) + max(pt[0]))/2,
  (min(pt[1]) + max(pt[1]))/2
)

r = Render(800, 800)

a = 90
rotate_matrix = np.matrix([
  [np.cos(a),  -np.sin(a), 0],
  [np.sin(a),  np.cos(a), 0],
  [0, 0, 1]
])

play_matrix = np.matrix([
  [1, 0, 0],
  [0, 1, 0],
  [-0.01, 0, 1] 
])

translate_to_origin = np.matrix([
  [1, 0, -center.x],
  [0, 1, -center.y],
  [0, 0, 1]
])
translate_back = np.matrix([
  [1, 0, center.x],
  [0, 1, center.y],
  [0, 0, 1]
])

transform_matrix = translate_back @ play_matrix @ translate_to_origin

transformed_points = []
for point in points:
  point = V2(*point)
  tpoint = np.dot(
    transform_matrix, 
    [point.x, point.y, 1]).tolist()[0]
  tpoint = V3(*tpoint)
  point = V2(
    tpoint.x / tpoint.z,
    tpoint.y / tpoint.z
  )
  print(tpoint)
  transformed_points.append(point)
 
print(transformed_points)

prev_point = points[-1]
for point in points:
  r.line(prev_point, point, color(255, 255, 0))
  prev_point = point

prev_point = transformed_points[-1]
for point in transformed_points:
  r.line(prev_point, point, WHITE)
  prev_point = point

r.display('out.bmp')

