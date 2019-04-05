from gl import *



def gourad(render, **kwargs):
  # barycentric
  w, v, u = kwargs['bar']
  # texture
  tx, ty = kwargs['texture_coords']
  tcolor = render.active_texture.get_color(tx, ty)
  # normals
  nA, nB, nC = kwargs['varying_normals']

  # light intensity
  iA, iB, iC = [ dot(n, render.light) for n in (nA, nB, nC) ]
  intensity = w*iA + v*iB + u*iC

  return color(
      int(tcolor[2] * intensity) if tcolor[0] * intensity > 0 else 0,
      int(tcolor[1] * intensity) if tcolor[1] * intensity > 0 else 0,
      int(tcolor[0] * intensity) if tcolor[2] * intensity > 0 else 0
    )


import random

def fragment(render, **kwargs):
  # barycentric
  w, v, u = kwargs['bar']
  # texture
  tx, ty = kwargs['texture_coords']
  # tcolor = render.active_texture.get_color(tx, ty)
  grey = int(ty * 256)
  tcolor = color(grey, 100, 100)
  # normals
  nA, nB, nC = kwargs['varying_normals']

  # light intensity
  iA, iB, iC = [ dot(n, render.light) for n in (nA, nB, nC) ]
  intensity = w*iA + v*iB + u*iC

  if (intensity>0.85):
    intensity = 1
  elif (intensity>0.60):
    intensity = 0.80
  elif (intensity>0.45):
    intensity = 0.60
  elif (intensity>0.30):
    intensity = 0.45
  elif (intensity>0.15):
    intensity = 0.30
  else:
    intensity = 0

  return color(
      int(tcolor[2] * intensity) if tcolor[0] * intensity > 0 else 0,
      int(tcolor[1] * intensity) if tcolor[1] * intensity > 0 else 0,
      int(tcolor[0] * intensity) if tcolor[2] * intensity > 0 else 0
    )



r = Render(800, 800)
t = Texture('./models/model.bmp')
r.light = V3(0, 1, 1)

r.active_texture = t
r.active_shader = fragment

r.lookAt(V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0))
r.load('./models/model.obj', translate=(0, 0, 0), scale=(1, 1, 1), rotate=(0, 0, 0))
r.draw_arrays('TRIANGLES')
r.display('out.bmp')

