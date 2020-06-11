import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from triangle import Triangle

def DrawPoint(pos, color, size = 2):
    glEnable(GL_POINT_SMOOTH)
    glPointSize(size)
    glBegin(GL_POINTS)
    glColor3fv(color)
    glVertex3fv(pos)
    glEnd()

def DrawTriangle(t:Triangle, color):
    glBegin(GL_LINES)
    glColor3fv(color)
    glVertex3fv(t.v1)
    glVertex3fv(t.v2)
    glVertex3fv(t.v2)
    glVertex3fv(t.v3)
    glVertex3fv(t.v3)
    glVertex3fv(t.v1)
    glEnd()

def Usage():
    print("""
    Commands:
    ---------
      <TAB> : change vertex
        <W> : move vertex up
        <S> : move vertex down
        <A> : move vertex left
        <D> : move vertex right
        <Q> : rotate triangle counter-clockwise
        <E> : rotate triangle clockwise
    <SPACE> : stop movement
        <R> : reset triangle
        <H> : display commands
    """)

def main():
    pygame.init()
    pygame.display.set_caption('AspectRatioPlay')

    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    initial_camera_pos = (0, 0, -5)

    glTranslatef(initial_camera_pos[0], initial_camera_pos[1], initial_camera_pos[2])

    T = Triangle(v1 = (0, 0, 0),
                 v2 = (1, 0, 0),
                 v3 = (0, 1, 0))

    try:
        new_aspect_ratio = T.aspect_ratio()
    except:
        new_aspect_ratio = -1
    prev_aspect_ratio = new_aspect_ratio

    valid_t = new_aspect_ratio != -1

    t_step_size = 0.0005
    t = { 'x' : 0, 'y' : 0, 'z' : 0 }
    a_step_size = 0.0005
    angle = 0
    
    ctrl_v = 1
    
    WHITE = (1, 1, 1)
    RED = (1, 0, 0)
    GREEN = (0, 1, 0)
    YELLOW = (1, 1, 0)

    Usage()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    t['x'] -= t_step_size
                if event.key == pygame.K_d:
                    t['x'] += t_step_size
                if event.key == pygame.K_w:
                    t['y'] += t_step_size
                if event.key == pygame.K_s:
                    t['y'] -= t_step_size
                if event.key == pygame.K_q:
                    angle += a_step_size
                if event.key == pygame.K_e:
                    angle -= a_step_size
                if event.key == pygame.K_SPACE:
                    t = { 'x' : 0, 'y' : 0, 'z' : 0 }
                    angle = 0
                if event.key == pygame.K_TAB:
                    if ctrl_v == 3:
                        ctrl_v = 1
                    else:
                        ctrl_v += 1
                if event.key == pygame.K_r:
                    T = Triangle(v1 = (0, 0, 0),
                                 v2 = (1, 0, 0),
                                 v3 = (0, 1, 0))
                if event.key == pygame.K_h:
                    Usage()

        """ Update shapes """
        if ctrl_v == 1:
            T.move_v1((t['x'], t['y'], t['z']))
            cur_p = T.v1
        elif ctrl_v == 2:
            T.move_v2((t['x'], t['y'], t['z']))
            cur_p = T.v2
        elif ctrl_v == 3:
            T.move_v3((t['x'], t['y'], t['z']))
            cur_p = T.v3
            
        T.rotate(angle=angle, axis='x', fixed=2)
        
        try:
            new_aspect_ratio = T.aspect_ratio()
        except:
            new_aspect_ratio = -1
        
        valid_t = new_aspect_ratio != -1

        """ Clear Screen """
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        """ Drawing stuff """
        DrawPoint(cur_p, RED, 5)

        if valid_t:
            DrawTriangle(T, WHITE)
        else:
            DrawTriangle(T, RED)
        
        """ Update screen """
        pygame.display.flip()
        pygame.time.wait(10) # milliseconds

        """ Console write stuff """
        if prev_aspect_ratio != new_aspect_ratio:
            print(f'Aspect Ratio = {new_aspect_ratio}')

        """ Finally """
        prev_aspect_ratio = new_aspect_ratio

main()