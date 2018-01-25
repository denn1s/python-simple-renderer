
class Obj(object):
    def __init__(self, filename):
        with open(filename) as f:
            self.lines = f.read().splitlines()
        self.vertices = []
        self.vfaces = []
        self.read()

    def read(self):
        for line in self.lines:
            if line:
                prefix, value = line.split(' ', 1)
                if prefix == 'v':
                    self.vertices.append(list(map(float, value.split(' '))))
                elif prefix == 'f':
                    self.vfaces.append([list(map(int, face.split('/'))) for face in value.split(' ')])


from gl import Render

width, height = 800, 600
r = Render(width, height)

model = Obj('./model.obj')

for face in model.vfaces:
    vcount = len(face)
    for j in range(vcount):
        f1 = face[j][0]
        f2 = face[(j+1)%vcount][0]

        v1 = model.vertices[f1 - 1]
        v2 = model.vertices[f2 - 1]

        scaleX = 15 # 15 # 400
        scaleY = 15 # 15 # 300 
        translateX = 25 # 25 # 1 25
        translateY = 5 # 5 # 1 5

        x1 = round((v1[0] + translateX) * scaleX); 
        y1 = round((v1[1] + translateY) * scaleY); 
        x2 = round((v2[0] + translateX) * scaleX); 
        y2 = round((v2[1] + translateY) * scaleY); 
  
        r.line((x1, y1), (x2, y2))
        

r.display()