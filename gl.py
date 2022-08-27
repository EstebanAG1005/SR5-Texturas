import struct
import random
from textures import Texture, Obj
from collections import namedtuple

V2 = namedtuple('Vertex2', ['x', 'y'])
V3 = namedtuple('Vertex3', ['x', 'y', 'z'])

# -------------------------------------------- Utils ---------------------------------------------------

# 1 byte
def char(c):
    return struct.pack('=c', c.encode('ascii'))

# 2 bytes
def word(c):
    return struct.pack('=h', c)

# 4 bytes 
def dword(c):
    return struct.pack('=l', c)

# Funcion de Color
def color(r, g, b):
    return bytes([int(b * 255), int(g * 255), int(r * 255)])

# Funcion que ayuda a convertir floats para poder usar los colores
def FloatRGB(array):
    return [round(i*255) for i in array]

# ----------------------------- Parte de Operaciones Matematicas -----------------------------------------

# Coordenadas Baricentricas
def barycentric(A, B, C, P):
    bary = cross(
        V3(C.x - A.x, B.x - A.x, A.x - P.x), 
        V3(C.y - A.y, B.y - A.y, A.y - P.y)
    )

    if abs(bary[2]) < 1:
        return -1, -1, -1  

    return (
        1 - (bary[0] + bary[1]) / bary[2], 
        bary[1] / bary[2], 
        bary[0] / bary[2]
    )

# Resta
def sub(v0, v1):
    return V3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)

# producto punto
def dot(v0, v1):
    return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

# Obtiene 2 valores de 3 vectores y devuelve un vector 3 con el producto punto
def cross(v0, v1):
    return V3(
    v0.y * v1.z - v0.z * v1.y,
    v0.z * v1.x - v0.x * v1.z,
    v0.x * v1.y - v0.y * v1.x,
)

# Regresa el largo del vector
def length(v0):
    return (v0.x**2 + v0.y**2 + v0.z**2)**0.5

# Normal del vector 
def norm(v0):
    v0length = length(v0)

    if not v0length:
        return V3(0, 0, 0)

    return V3(v0.x/v0length, v0.y/v0length, v0.z/v0length)

# 2 vectores de tamaño 2 que definen el rectángulo delimitador más pequeño posible
def bbox(*vertices): 
    xs = [ vertex.x for vertex in vertices ]
    ys = [ vertex.y for vertex in vertices ]
    xs.sort()
    ys.sort()

    return V2(xs[0], ys[0]), V2(xs[-1], ys[-1])

# --------------------------------------------------------------------------------------------------------------------

# Se definen colores Negro y Blanco para nuestro programa
BLACK = color(0,0,0)
WHITE = color(1,1,1)

class Render(object):
 
  # Se inicializan valores
  def __init__(self, width, height):
        self.current_color = WHITE
        self.clear_color = BLACK
        self.glCreateWindow(width, height)
        self.light = V3(0,0,1)
        self.active_texture = None
  
  # Se crea el margen con el cual se va a trabajar
  def glCreateWindow(self, width, height):
      self.width = width
      self.height = height
      self.glClear()
      self.glViewport(0,0, width, height)

  # Se crea el Viewport
  def glViewport(self, x, y, width, height):
      self.VP_IX = x
      self.VP_IY = y
      self.VP_W = width
      self.VP_H = height
      self.VP_FX = x + width
      self.VP_FY = x + height

  # Se definen colores con los cuales trabajar
  def glClear(self):
      self.framebuffer = [
      [self.clear_color for x in range(self.width)] 
      for y in range(self.height)
      ]
      self.zbuffer = [
        [-float('inf') for x in range(self.width)]
        for y in range(self.height)
      ]

  # Se revisa el vertex dentro del viewport en el cual vamos a trabajar
  def glVertextInViewport(self, x,y):
      return (x >= self.VP_IX and
          x <= self.VP_FX) and (
          y >= self.VP_IY and
          y <= self.VP_FY)

  # Se definen los colores del BMP para poderlos incluir en el OBJ
  def glClearColor(self, r, g, b):
      array_colors = FloatRGB([r,g,b])
      self.clear_color = color(array_colors[0], array_colors[1], array_colors[2])

  # Se genera el vertex
  def glVertex(self, x, y, color = None):
      pixelX = ( x + 1) * (self.vpWidth  / 2 ) + self.vpX
      pixelY = ( y + 1) * (self.vpHeight / 2 ) + self.vpY
      try:
          self.framebuffer[round(pixelY)][round(pixelX)] = color or self.current_color
      except:
          pass
  
  # Se definen puntos dentro del Margen establecido
  def glPoint(self, x, y, color = None):
      if x >= self.width or x < 0 or y >= self.height or y < 0:
          return
      try:
          self.framebuffer[y][x] = color or self.current_color
      except:
          pass
  
  # Se definen colores a utilizar
  def glColor(self, r, g, b):
      array_colors = FloatRGB([r,g,b])
      self.clear_color = color(array_colors[0], array_colors[1], array_colors[2])
      
  # Se Genera archivo .BMP
  def glFinish(self, filename):
      f = open(filename, 'bw')

      #file header
      f.write(char('B'))
      f.write(char('M'))
      f.write(dword(14 + 40 + self.width * self.height * 3))
      f.write(dword(0))
      f.write(dword(14 + 40))

      #image header
      f.write(dword(40))
      f.write(dword(self.width))
      f.write(dword(self.height))
      f.write(word(1))
      f.write(word(24))
      f.write(dword(0))
      f.write(dword(self.width * self.height * 3))
      f.write(dword(0))
      f.write(dword(0))
      f.write(dword(0))
      f.write(dword(0))
      
      # pixel data

      for x in range(self.height):
          for y in range(self.width):
              f.write(self.framebuffer[x][y])

      f.close()

  # Funcion para crear lineas
  def glLine(self, v0, v1, color = None):
      x0 = v0.x
      x1 = v1.x
      y0 = v0.y
      y1 = v1.y

      steep = abs(y1 - y0) > abs(x1 - x0)

      if steep:
          x0, y0 = y0, x0
          x1, y1 = y1, x1
      if x0 > x1:
          x0, x1 = x1, x0
          y0, y1 = y1, y0

      dx, dy = abs(x1 - x0), abs(y1 - y0)      
      
      offset = 0
      limit =  0.5
      y = y0
  
      try:
          m = dy/dx
      except ZeroDivisionError:
          pass
          
      for x in range(x0, x1+1):
          self.glPoint(y, x, color) if steep else self.glPoint(x, y, color)
          
          offset += 2*dy

          if offset >= limit:
              y += 1 if y0 < y1 else -1
              limit += 2*dx        
  
  # Funcion de Transformacion 
  def transform(self, vertex, translate=V3(0,0,0), scale=V3(1,1,1)):
      return V3(round(vertex[0] * scale.x + translate.x),
                round(vertex[1] * scale.y + translate.y),
                round(vertex[2] * scale.z + translate.z))


  # Se carga el Modelo
  def loadModel(self, filename, translate = V3(0,0,0), scale = V3(1,1,1), isWireframe = False):
      model = Obj(filename)

      light = V3(0,0,1)

      for face in model.faces:

          vcount = len(face)

          if isWireframe:
              for vert in range(vcount):
                  v0 = model.vertices[ face[vert][0] - 1 ]
                  v1 = model.vertices[ face[(vert + 1) % vcount][0] - 1]
                  v0 = V2(round(v0[0] * scale.x  + translate.x),round(v0[1] * scale.y  + translate.y))
                  v1 = V2(round(v1[0] * scale.x  + translate.x),round(v1[1] * scale.y  + translate.y))
                  self.glLine(v0, v1)

          else:
              v0 = model.vertices[ face[0][0] - 1 ]
              v1 = model.vertices[ face[1][0] - 1 ]
              v2 = model.vertices[ face[2][0] - 1 ]
              if vcount > 3:
                  v3 = model.vertices[ face[3][0] - 1 ]

              v0 = self.transform(v0,translate, scale)
              v1 = self.transform(v1,translate, scale)
              v2 = self.transform(v2,translate, scale)
              if vcount > 3:
                  v3 = self.transform(v3,translate, scale)

              if self.active_texture:
                  vt0 = model.texcoords[face[0][1] - 1]
                  vt1 = model.texcoords[face[1][1] - 1]
                  vt2 = model.texcoords[face[2][1] - 1]
                  vt0 = V2(vt0[0], vt0[1])
                  vt1 = V2(vt1[0], vt1[1])
                  vt2 = V2(vt2[0], vt2[1])
                  if vcount > 3:
                      vt3 = model.texcoords[face[3][1] - 1]
                      vt3 = V2(vt3[0], vt3[1])
              else:
                  vt0 = V2(0,0) 
                  vt1 = V2(0,0) 
                  vt2 = V2(0,0) 
                  vt3 = V2(0,0)

              normal = cross(sub(v1,v0), sub(v2,v0))
              intensity = dot(norm(normal), norm(light))

              if intensity >=0:
                  self.triangle_bc(v0,v1,v2, texture=self.active_texture, texcoords=(vt0,vt1, vt2), intensity=intensity)

                  # Manage square rendering
                  if vcount > 3:
                      v3 = model.vertices[ face[3][0] - 1 ]
                      v3 = self.transform(v3,translate, scale)
                      if intensity >=0:
                          self.triangle_bc(v0,v2,v3, color(intensity, intensity, intensity))

  # Coordenadas baricentricas
  def triangle_bc(self, A, B, C, texture, _color= WHITE,texcoords = (), intensity = 1):
      #bounding box
      minX = min(A.x, B.x, C.x)
      minY = min(A.y, B.y, C.y)
      maxX = max(A.x, B.x, C.x)
      maxY = max(A.y, B.y, C.y)

      for x in range(minX, maxX + 1):
          for y in range(minY, maxY + 1):
              if x >= self.width or x < 0 or y >= self.height or y < 0:
                  continue

              u, v, w = barycentric(A, B, C, V2(x, y))

              if u >= 0 and v >= 0 and w >= 0:

                  z = A.z * u + B.z * v + C.z * w
                  if z > self.zbuffer[y][x]:

                      b, g, r = _color
                      b/= 255
                      g/= 255
                      r/= 255

                      b*= intensity
                      g*= intensity
                      r*= intensity

                      if texture:
                          ta, tb, tc = texcoords

                          tx = ta.x * u + tb.x * v + tc.x*w
                          ty = ta.y * u + tb.y * v + tc.y*w

                          texColor = texture.getColor(tx,ty)
                          b*=texColor[0] /255
                          g*=texColor[1] /255
                          r*=texColor[2] /255

                      self.glPoint(x, y, color(r,g,b))
                      self.zbuffer[y][x] = z


