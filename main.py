# SR5-Textures
# Graficas por computadora 
# Esteban Aldana Guerra 20591

from gl import Render, color, V2, V3
from textures import Obj, Texture

import random

r = Render(1200, 1200)

t = Texture('model.bmp')

r.load('coffe.obj', (1, 0.5, 0), (600, 600, 600), texture=t)

r.glFinish('output.bmp')