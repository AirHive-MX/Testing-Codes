import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def main():
    # 1) Inicializar pygame y el modo de video
    pygame.init()

    # 2) Crear ventana con bandera OPENGL
    display = (640, 480)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # 3) Ajustar la perspectiva
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    # 4) Bucle principal
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Dibuja un triángulo
        glBegin(GL_TRIANGLES)
        glColor3f(1,0,0)
        glVertex3f(-1, -1, 0)
        glColor3f(0,1,0)
        glVertex3f( 1, -1, 0)
        glColor3f(0,0,1)
        glVertex3f( 0,  1, 0)
        glEnd()

        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    main()

