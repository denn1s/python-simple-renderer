from gl import Render

r = Render(800, 600)
# r.load('./miku/HatsuneMiku.obj', (200, 50, 0), (2, 2, 2) )
# r.load('./cubespherecone.obj', (0, 1, 1), (100, 100, 100) )
r.load('./natsuki.obj', (0.5, 0, 0), (500, 500, 300) )

r.display()