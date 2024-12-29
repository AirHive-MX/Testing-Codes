import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from objloader import OBJ

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glEnable(GL_DEPTH_TEST)
    gluPerspective(70, display[0]/display[1], 0.01, 500.0)

    glTranslatef(0.0, -1.0, 0.0)  # Mueve el modelo 1 unidad hacia arriba

    # Configura el color de fondo (blanco)
    glClearColor(1.0, 1.0, 1.0, 1.0)  # RGBA: Blanco

    # Carga tu modelo (OBJ + MTL). Asegúrate de que 'drone_final.obj' y su .mtl estén en la misma carpeta.
    obj = OBJ("./drone_final/drone_final.obj", swapyz=False)

    clock = pygame.time.Clock()
    running = True

    angle = 0
    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Limpia la pantalla (con el color definido por glClearColor)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(-1, 1, 0,  # Aleja la cámara (z positivo)
          0, 0, 0,  # Punto al que mira (centro del dron)
          0, 1, 0)  # Vector "arriba"


        # Opcional: Incremento de ángulo si se desea rotar
        angle += 1
        #glRotatef(angle, 0, 1, 0)

        # Escala del modelo
        glScalef(0.2, 0.2, 0.2)

        # Renderiza el modelo
        obj.render()

        # Actualiza la ventana
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
