import numpy as np
from gl import *

points = [
  (200, 200), (400, 200), (400, 400), (200, 400)
]

center = V2(300, 300)


move_to_center = np.matrix([
  [1, 0, -center.x],
  [0, 1, -center.y],
  [0, 0, 1]
])

a = 10
rotate_matrix = np.matrix([
  [1, 0, 0],
  [0, 1, 0],
  [0.002, 0, 1]
])

move_back = np.matrix([
  [1, 0, center.x],
  [0, 1, center.y],
  [0, 0, 1]
])


transform_matrix = move_back @ rotate_matrix @ move_to_center

# draw lines
transformed_points = []

for point in points:
  point = V2(*point)
  tpoint = transform_matrix @ [ point.x, point.y, 1 ]
  tpoint = V3(tpoint)
  npoint = V2(
    tpoint.x/tpoint.z,
    tpoint.y/tpoint.z
  )
  transformed_points.append(npoint)











r = Render(800, 800)
prev_point = transformed_points[-1]
for point in transformed_points:
  r.line(prev_point, point, WHITE)
  prev_point = point

"""
prev_point = points[-1]
for point in points:
  r.line(V2(*prev_point), V2(*point), color(0, 255, 0))
  prev_point = point
"""

r.display()

