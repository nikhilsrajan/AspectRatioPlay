import math
import copy

def sum(t1, t2):
    return (t1[0] + t2[0], t1[1] + t2[1], t1[2] + t2[2])

def diff(t1, t2):
    return (t1[0] - t2[0], t1[1] - t2[1], t1[2] - t2[2])

def dot(t1, t2):
    return t1[0]*t2[0] + t1[1]*t2[1] + t1[2]*t2[2]

def norm2(t):
    return math.sqrt(t[0]*t[0] + t[1]*t[1] + t[2]*t[2])

class Triangle(object):
    """ Triangle class """
    def __init__(self, v1, v2, v3):
        self.v1 = copy.deepcopy(v1)
        self.v2 = copy.deepcopy(v2)
        self.v3 = copy.deepcopy(v3)

    def print(self):
        print('v1:', self.v1)
        print('v2:', self.v2)
        print('v3:', self.v3)
    
    def translate(self, d):
        self.v1 = sum(self.v1, d)
        self.v2 = sum(self.v2, d)
        self.v3 = sum(self.v3, d)
    
    def rotate(self, angle, axis:str='x', fixed:int=0):
        """ rotate 
            angle: radians
            axis:
            - 'x': x-axis
            - 'y': y-axis
            - 'z': z-axis
            fixed:
            - 0: centroid
            - 1: v1
            - 2: v2
            - 3: v3
        """
        if axis not in ['x', 'y', 'z'] or fixed not in [0, 1, 2, 3]:
            raise ValueError

        if axis == 'x':
            R = [
                (1, 0, 0),
                (0, math.cos(angle), -math.sin(angle)),
                (0, math.sin(angle), math.cos(angle))
            ]
        elif axis == 'y':
            R = [
                (math.cos(angle), 0, math.sin(angle)),
                (0, 1, 0),
                (-math.sin(angle), 0, math.cos(angle))
            ]
        elif axis == 'z':
            R = [
                (math.cos(angle), -math.sin(angle), 0),
                (math.sin(angle), math.cos(angle), 0),
                (0, 0, 1)
            ]
        
        if fixed == 0:
            d = (
                (self.v1[0] + self.v2[0] + self.v3[0]) / 3,
                (self.v1[1] + self.v2[1] + self.v3[1]) / 3,
                (self.v1[2] + self.v2[2] + self.v3[2]) / 3 
            )
        elif fixed == 1: d = copy.deepcopy(self.v1)
        elif fixed == 2: d = copy.deepcopy(self.v2)
        elif fixed == 3: d = copy.deepcopy(self.v3)

        self.v1 = diff(self.v1, d)
        self.v2 = diff(self.v2, d)
        self.v3 = diff(self.v3, d)

        self.v1 = (dot(R[0], self.v1), dot(R[1], self.v1), dot(R[2], self.v1))
        self.v2 = (dot(R[0], self.v2), dot(R[1], self.v2), dot(R[2], self.v2))
        self.v3 = (dot(R[0], self.v3), dot(R[1], self.v3), dot(R[2], self.v3))

        self.v1 = sum(self.v1, d)
        self.v2 = sum(self.v2, d)
        self.v3 = sum(self.v3, d)

    def area(self):
        a = norm2(diff(self.v1, self.v2))
        b = norm2(diff(self.v2, self.v3))
        c = norm2(diff(self.v3, self.v1))
        s = (a + b + c) / 2
        return math.sqrt(s*(s-a)*(s-b)*(s-c))
    
    def aspect_ratio(self):
        a = norm2(diff(self.v1, self.v2))
        b = norm2(diff(self.v2, self.v3))
        c = norm2(diff(self.v3, self.v1))
        area = self.area()
        max_e = max(a, b, c)
        min_h = area * 2 / max_e
        return max_e / (2 * min_h / math.sqrt(3))

    def move_v1(self, d):
        self.v1 = sum(self.v1, d)

    def move_v2(self, d):
        self.v2 = sum(self.v2, d)
    
    def move_v3(self, d):
        self.v3 = sum(self.v3, d)