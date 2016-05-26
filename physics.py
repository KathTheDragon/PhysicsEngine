class Vector():
    def __init__(self, *args):
        if len(args) == 0:
            self.x = 0
            self.y = 0
            self.z = 0
        elif len(args) == 1:
            self.x = args[0].x
            self.y = args[0].y
            self.z = args[0].z
        else:
            self.x = args[0]
            self.y = args[1]
            if len(args) == 2:
                self.z = 0
            else:
                self.z = args[2]
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
        return Vector(
            self.x + vect.x,
            self.y + vect.y,
            self.z + vect.z
        )
        
    def __sub__(self, vect):
        return Vector(
            self.x - vect.x,
            self.y - vect.y,
            self.z - vect.z
        )
        
    def __mul__(self, val):
        return Vector(
            self.x * val,
            self.y * val,
            self.z * val
        )
        
    def __rmul__(self, val):
        return Vector(
            self.x * val,
            self.y * val,
            self.z * val
        )
        
    def __div__(self, val):
        return Vector(
            self.x / val,
            self.y / val,
            self.z / val
        )
        
    def __neg__(self):
        return Vector(
            -vect.x,
            -vect.y,
            -vect.z
        )
        
    def __pos__(self):
        return Vector(
            vect.x,
            vect.y,
            vect.z
        )
    
    def mag(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5
    
    def norm(self):
        return self / self.mag()
        
    def setMag(self, mag):
        return self.norm() * mag
        
    def dot(self, vect):
        return self.x * vect.x + self.y * vect.y + self.z * vect.z
    
    def cross(self, *args):
        ans = Vector(self)
        for arg in args:
            x = ans.y*arg.z - ans.z*arg.y
            y = ans.z*arg.x - ans.x*arg.z
            z = ans.x*arg.y - ans.y*arg.x
            ans.x = x
            ans.y = y
            ans.z = z
        return ans


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

