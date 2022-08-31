# SR5-Textures
# Graficas por computadora 
# Esteban Aldana Guerra 20591

from gl import Render, color, V2, V3
from textures import Obj, Texture

import random

r = Render(1300, 1300)

t = Texture('model.bmp')

r.load('model.obj', (1, 1, 1), (300, 300, 300), texture=t)

r.glFinish('output.bmp')