import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from math import sin, cos, sqrt

from copy import deepcopy

def SumTuples(t1, t2):
    l1 = list(t1)
    l2 = list(t2)
    Sum = []
    for i, l1i in enumerate(l1):
        Sum.append(l1i + l2[i])
    return tuple(Sum)

def DotPTuples(t1, t2):
    l1 = list(t1)
    l2 = list(t2)
    dotP = 0
    for i, l1i in enumerate(l1):
        dotP += l1i * l2[i]
    return dotP

def CrossPTuples(t1, t2):
    l1 = list(t1)
    l2 = list(t2)
    return (
        l1[1]*l2[2] - l2[1]*l1[2],
        -(l1[0]*l2[2] - l2[0]*l1[2]),
        l1[0]*l2[1] - l2[0]*l1[1]
    )

def Norm2(t):
    return sqrt(t[0]*t[0] + t[1]*t[1] + t[2]*t[2])

def DrawPoint(pos, color, size = 2):
    glEnable(GL_POINT_SMOOTH)
    glPointSize(size)
    glBegin(GL_POINTS)
    glColor3fv(color)
    glVertex3fv(pos)
    glEnd()    

class Triangle(object):
    """ Triangle class """
    def __init__(self, v1, v2, v3):
        self.v1 = deepcopy(v1)
        self.v2 = deepcopy(v2)
        self.v3 = deepcopy(v3)
    
    def draw(self, color):
        glBegin(GL_LINES)
        glColor3fv(color)
        glVertex3fv(self.v1)
        glVertex3fv(self.v2)
        glVertex3fv(self.v2)
        glVertex3fv(self.v3)
        glVertex3fv(self.v3)
        glVertex3fv(self.v1)
        glEnd()
    
    def translate(self, t):
        self.v1 = SumTuples(self.v1, t)
        self.v2 = SumTuples(self.v2, t)
        self.v3 = SumTuples(self.v3, t)
        glTranslatef(-t[0], -t[1], -t[2])
    
    def rotate(self, angle):
        centroid = SumTuples(SumTuples(self.v1, self.v2), self.v3)
        centroid = (centroid[0]/3, centroid[1]/3, centroid[2]/3)

        self.translate((-centroid[0], -centroid[1], -centroid[2]))
        
        R1 = (cos(angle), -sin(angle), 0)
        R2 = (sin(angle), cos(angle), 0)
        R3 = (0, 0, 1)
        self.v1 = (DotPTuples(R1, self.v1), DotPTuples(R2, self.v1), DotPTuples(R3, self.v1))
        self.v2 = (DotPTuples(R1, self.v2), DotPTuples(R2, self.v2), DotPTuples(R3, self.v1))
        self.v3 = (DotPTuples(R1, self.v3), DotPTuples(R2, self.v3), DotPTuples(R3, self.v1))

        self.translate(centroid)
    
    def moveV1(self, t):
        self.v1 = SumTuples(self.v1, t)

    def moveV2(self, t):
        self.v2 = SumTuples(self.v2, t)

    def moveV3(self, t):
        self.v3 = SumTuples(self.v3, t)

    def AspectRatio(self):
        a = Norm2((self.v1[0] - self.v2[0], self.v1[1] - self.v2[1], self.v1[2] - self.v2[2]))
        b = Norm2((self.v2[0] - self.v3[0], self.v2[1] - self.v3[1], self.v2[2] - self.v3[2]))
        c = Norm2((self.v3[0] - self.v1[0], self.v3[1] - self.v1[1], self.v3[2] - self.v1[2]))
        s = (a + b + c) / 2
        return a*b*c / (8*(s-a)*(s-b)*(s-c))

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
        <H> : display commands
    """)

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    initial_camera_pos = (0, 0, -5)

    glTranslatef(initial_camera_pos[0], initial_camera_pos[1], initial_camera_pos[2])

    T = Triangle(v1 = (0, 0, 0),
                 v2 = (1, 0, 0),
                 v3 = (0, 1, 0))

    try:
        new_aspect_ratio = T.AspectRatio()
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
                if event.key == pygame.K_h:
                    Usage()

        
        """ Update shapes """
        if ctrl_v == 1:
            T.moveV1((t['x'], t['y'], t['z']))
            cur_p = T.v1
        elif ctrl_v == 2:
            T.moveV2((t['x'], t['y'], t['z']))
            cur_p = T.v2
        elif ctrl_v == 3:
            T.moveV3((t['x'], t['y'], t['z']))
            cur_p = T.v3
            
        T.rotate(angle)
        
        try:
            new_aspect_ratio = T.AspectRatio()
        except:
            new_aspect_ratio = -1
        
        valid_t = new_aspect_ratio != -1

        """ Clear Screen """
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        """ Drawing stuff """
        DrawPoint(cur_p, RED, 5)

        if valid_t:
            T.draw(WHITE)
        else:
            T.draw(RED)
        
        """ Update screen """
        pygame.display.flip()
        pygame.time.wait(10) # milliseconds

        """ Console write stuff """
        if prev_aspect_ratio != new_aspect_ratio:
            print(f'Aspect Ratio = {new_aspect_ratio}')

        """ Finally """
        prev_aspect_ratio = new_aspect_ratio

main()