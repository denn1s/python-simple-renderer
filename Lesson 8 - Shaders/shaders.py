from gl import Render, color as Color
from obj import Texture


def gourad(color, intensity):
  # color = Color(255, 255, 255)
  return bytes(map(lambda b: round(b*intensity) if b*intensity > 0 else 0, color))


def heatmap(color, intensity):
  if intensity>.85:
    intensity = 1
  elif intensity>.60:
    intensity = .80
  elif intensity>.45:
    intensity = .60
  elif intensity>.30:
    intensity = .45
  elif intensity>.15: 
    intensity = .30
  else:
    intensity = 0;    
  # color = Color(255, 155, 0)
  return bytes(map(lambda b: round(b*intensity) if b*intensity > 0 else 0, color))


def heatmap(color, intensity):
  if intensity>.85:
    intensity = 1
  elif intensity>.60:
    intensity = .80
  elif intensity>.45:
    intensity = .60
  elif intensity>.30:
    intensity = .45
  elif intensity>.15: 
    intensity = .30
  else:
    intensity = 0;    
  # color = Color(255, 155, 0)
  return bytes(map(lambda b: round(b*intensity) if b*intensity > 0 else 0, color))


r = Render(800, 600)
t = Texture('./models/model.bmp')
r.load('./models/model.obj', (1, 1, 1), (300, 300, 300), texture=t, shader=gourad)
r.display('out.bmp')

