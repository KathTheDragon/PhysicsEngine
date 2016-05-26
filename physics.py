from math import cos, sin, asin, atan2

class Vector():
    def __init__(self, *args):
        if len(args) == 0:
            self.x = 0
            self.y = 0
            self.z = 0
            self.r = 0
            self.theta = 0
            self.phi = 0
        else:
            self.x = args[0].x
            self.y = args[0].y
            self.z = args[0].z
            self.r = args[0].r
            self.theta = args[0].theta
            self.phi = args[0].phi
        return
    
    def __repr__(self):
        return "Vector({}, {}, {})".format(self.x, self.y, self.z)
        
    def __str__(self):
        return "({}, {}, {})".format(self.x, self.y, self.z)
        
    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __add__(self, vect):
        return CVector(
            self.x + vect.x,
            self.y + vect.y,
            self.z + vect.z
        )
        
    def __sub__(self, vect):
        return CVector(
            self.x - vect.x,
            self.y - vect.y,
            self.z - vect.z
        )
        
    def __mul__(self, arg):
        if isinstance(arg, Vector):
            return CVector(
                self.y*arg.z - self.z*arg.y,
                self.z*arg.x - self.x*arg.z,
                self.x*arg.y - self.y*arg.x
            )
        else:
            return PVector(
                self.r * arg,
                self.theta,
                self.phi
            )
        
    def __rmul__(self, val):
        return PVector(
            self.r * val,
            self.theta,
            self.phi
        )
        
    def __div__(self, val):
        return PVector(
            self.r / val,
            self.theta,
            self.phi
        )
        
    def __neg__(self):
        return PVector(
            -self.r,
            self.theta,
            self.phi
        )
        
    def __pos__(self):
        return Vector(self)
    
    def mag(self):
        return self.r
    
    def norm(self):
        return PVector(
            1,
            self.theta,
            self.phi
        )
        
    def setMag(self, mag):
        return PVector(
            mag,
            self.theta,
            self.phi
        )
        
    def dot(self, vect):
        return self.x * vect.x + self.y * vect.y + self.z * vect.z

class CVector(Vector):
    def __init__(self, *args):
        if len(args) > 1:
            self.x = args[0]
            self.y = args[1]
            self.r = self.x**2 + self.y**2
            self.theta = atan2(self.y, self.x)
            if len(args) == 2 or not args[2]:
                self.z = 0
                self.r **= 0.5
                self.phi = 0
            else:
                self.z = args[2]
                self.r = (self.r + self.z**2)**0.5
                self.phi = asin(self.z / self.r)
        else:
            super().__init__(*args)
        return

class PVector(Vector):
    def __init__(self, *args):
        if len(args) > 1:
            self.r = args[0]
            self.theta = args[1]
            self.x = self.r * cos(self.theta)
            self.y = self.r * sin(self.theta)
            if len(args) == 2 or not args[2]:
                self.phi = 0
                self.z = 0
            else:
                self.phi = args[2]
                self.x *= cos(self.phi)
                self.y *= cos(self.phi)
                self.z = self.r * sin(self.phi)
        else:
            super().__init__(*args)
        return

class Body():
    def __init__(self, *args):
        if len(args) == 4:
            self.m = args[0]
            self.s = Vector(args[1])
            self.v = Vector(args[2])
            self.a = Vector(args[3])
        elif len(args) == 1:
            self.m = args[0].m
            self.s = Vector(args[0].s)
            self.v = Vector(args[0].v)
            self.a = Vector(args[0].a)
        else:
            self.m = 1
            self.s = Vector()
            self.v = Vector()
            self.a = Vector()
        return
    
    def move(self, force=None):
        if force is None:
            force = Vector()
        da = force / self.m - self.a
        dv = self.a + da / 2
        ds = self.v + dv / 2 - da / 3
        self.a += da
        self.v += dv
        self.s += ds
        return

class Region():
    def __init__(self, *args):
        pass

