# SR5-Textures
# Graficas por computadora 
# Esteban Aldana Guerra 20591

from gl import Render, color, V2, V3
from textures import Obj, Texture

import random

r = Render(1300, 1300)

t = Texture('coca.bmp')

r.load('cocacola.obj', (-5, 1.5, 0), (100, 100, 100), texture=t)

r.glFinish('output.bmp')