import pygame
from OpenGL.GL import *

def MTL(filename):
    contents = {}
    mtl = None
    for line in open(filename, "r"):
        # Ignoramos comentarios y líneas vacías
        if line.startswith('#'):
            continue
        values = line.split()
        if not values:
            continue

        if values[0] == 'newmtl':
            # Creamos un diccionario para cada material nuevo
            mtl = contents[values[1]] = {}
        elif mtl is None:
            # En Python 3, la forma correcta de lanzar la excepción es:
            raise ValueError("mtl file doesn't start with newmtl stmt")
        elif values[0] == 'map_Kd':
            # Cargamos la textura difusa
            mtl[values[0]] = values[1]
            surf = pygame.image.load(mtl['map_Kd'])
            image = pygame.image.tostring(surf, 'RGBA', 1)
            ix, iy = surf.get_rect().size

            texid = mtl['texture_Kd'] = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texid)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA,
                         GL_UNSIGNED_BYTE, image)

        else:
            # Aquí convertimos a float
            # En Python 2, map(...) devolvía lista directamente,
            # en Python 3 hay que envolverlo en list(...)
            mtl[values[0]] = list(map(float, values[1:]))

    return contents

class OBJ:
    def __init__(self, filename, swapyz=False):
        """Loads a Wavefront OBJ file."""
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []
        self.mtl = {}

        material = None

        for line in open(filename, "r"):
            # Ignorar comentarios / líneas vacías
            if line.startswith('#'):
                continue
            values = line.split()
            if not values:
                continue

            if values[0] == 'v':
                # v x y z
                # Convertir a float y, si swapyz=True, intercambiar ejes
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = [v[0], v[2], v[1]]
                self.vertices.append(v)

            elif values[0] == 'vn':
                # vn x y z (normales)
                vn = list(map(float, values[1:4]))
                if swapyz:
                    vn = [vn[0], vn[2], vn[1]]
                self.normals.append(vn)

            elif values[0] == 'vt':
                # vt u v (coordenadas de textura)
                vt = list(map(float, values[1:3]))
                self.texcoords.append(vt)

            elif values[0] in ('usemtl', 'usemat'):
                # Cambiamos de material
                material = values[1]

            elif values[0] == 'mtllib':
                # Cargamos el MTL
                self.mtl = MTL(values[1])

            elif values[0] == 'f':
                # f v1/vt1/vn1 v2/vt2/vn2 ...
                face_vertices = []
                face_normals = []
                face_texcoords = []
                for v in values[1:]:
                    w = v.split('/')
                    # Índices en .obj empiezan en 1
                    vi = int(w[0])
                    face_vertices.append(vi)

                    if len(w) > 1 and w[1]:
                        ti = int(w[1])
                        face_texcoords.append(ti)
                    else:
                        face_texcoords.append(0)

                    if len(w) > 2 and w[2]:
                        ni = int(w[2])
                        face_normals.append(ni)
                    else:
                        face_normals.append(0)

                self.faces.append((face_vertices, face_normals, face_texcoords, material))

        # Ahora creamos la lista de dibujo
        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glEnable(GL_TEXTURE_2D)
        glFrontFace(GL_CCW)

        for face in self.faces:
            vertices, normals, texture_coords, mat = face

            # Obtenemos el diccionario del material actual
            mtl = self.mtl.get(mat, {})
            if 'texture_Kd' in mtl:
                glBindTexture(GL_TEXTURE_2D, mtl['texture_Kd'])
            else:
                # si no hay textura, usamos Kd como color difuso
                # Kd (r, g, b) o (r, g, b, a)
                if 'Kd' in mtl:
                    glColor3fv(mtl['Kd'])
                else:
                    glColor3f(1, 1, 1)

            glBegin(GL_POLYGON)
            for i in range(len(vertices)):
                if normals[i] > 0:
                    # Recuerda que vn = self.normals[índice - 1]
                    glNormal3fv(self.normals[normals[i] - 1])
                if texture_coords[i] > 0:
                    glTexCoord2fv(self.texcoords[texture_coords[i] - 1])
                glVertex3fv(self.vertices[vertices[i] - 1])
            glEnd()

        glDisable(GL_TEXTURE_2D)
        glEndList()

    def render(self):
        """ Llama a la lista de dibujo generada. """
        glCallList(self.gl_list)
