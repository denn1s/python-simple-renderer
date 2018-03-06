from gl import Render, color as Color
from obj import Texture, NormalMap


def gourad(color, intensity):
  return bytes(map(lambda b: round(b*intensity) if b*intensity > 0 else 0, color))



r = Render(800, 600)
t = Texture('./models/model.bmp')
n = NormalMap('./models/normal.bmp')
r.load('./models/model.obj', (1, 1, 1), (300, 300, 300), 
      texture=t, shader=gourad, normalmap=n)
r.display('out.bmp')

