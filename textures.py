# SR5-Textures
# Graficas por computadora 
# Esteban Aldana Guerra 20591

import struct

def color(r, g, b):
    return bytes([b, g, r])

class Obj(object):
    def __init__(self, filename):
        
        with open(filename, "r") as file:
            self.lines = file.read().splitlines()

        self.vertices = []
        self.texcoords = []
        self.normals = []
        self.faces = []

        self.read()


    def read(self):
        for line in self.lines:
            if line:
                prefix, value = line.split(' ', 1)

                if prefix == 'v': # Vertices
                    self.vertices.append(list(map(float, value.split(' '))))
                elif prefix == 'vt': #Texture Coordinates
                    self.texcoords.append(list(map(float, value.split(' '))))
                elif prefix == 'vn': #Normales
                    self.normals.append(list(map(float, value.split(' '))))
                elif prefix == 'f': #Caras
                    self.faces.append( [ list(map(int, vert.split('/'))) for vert in value.split(' ')] )

class Texture(object):
  def __init__(self, path):
        self.path = path
        self.width = 0
        self.heigth = 0
        self.read()

  def read(self):
    with open(self.path, "rb") as image:
        image.seek(10)
        header_size = struct.unpack("=l", image.read(4))[0]
        image.seek(18)
        self.width = struct.unpack("=l", image.read(4))[0]
        self.heigth = struct.unpack("=l", image.read(4))[0]
        image.seek(header_size)
        self.pixels = []

        for y in range(self.heigth):
            self.pixels.append([])
            for x in range(self.width):
                b = ord(image.read(1))
                g = ord(image.read(1))
                r = ord(image.read(1))

                self.pixels[y].append(color(r, g, b))

  def get_color(self, tx, ty):
    x = round(tx*self.width)
    y = round(ty*self.heigth)

    return self.pixels[y][x]

  def intensity(self, tx, ty, intensity):
    x = round(tx*(self.width-1))
    y = round(ty*(self.heigth-1))

    b = round(self.pixels[y][x][0]*intensity)
    g = round(self.pixels[y][x][1]*intensity)
    r = round(self.pixels[y][x][2]*intensity)

    return color(r, g, b)