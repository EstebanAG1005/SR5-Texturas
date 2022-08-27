from gl import Render, color, V2, V3
from textures import Obj, Texture

import random

r = Render(1000,1000)
r.active_texture = Texture('model.bmp')

r.loadModel('model.obj', V3(500,500,0), V3(300,300,300))

r.glFinish('output.bmp')