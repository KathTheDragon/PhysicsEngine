class Vector():
    def __init__(self, *args):
        if len(args) == 3:
            self.x = args[0]
            self.y = args[1]
            self.z = args[2]
        elif len(args) == 1:
            self.x = args[0].x
            self.y = args[0].y
            self.z = args[0].z
        else:
            self.x = 0
            self.y = 0
            self.z = 0
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
            self.z - vect.z,
        )
        
    def __mul__(self, vect):
        return Vector(
            self.x * vect.x,
            self.y * vect.y,
            self.z * vect.z,
        )
        
    def __div__(self, vect):
        return Vector(
            self.x / vect.x,
            self.y / vect.y,
            self.z / vect.z,
        )
    
    def mag(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5
    
    def norm(self):
        return self / self.mag()
        
    def setMag(self, mag):
        return self.norm() * mag
        
    def dot(self, vec):
        return self.x * vec.x + self.y * vec.y + self.z * vec.z
    
    def cross(self, *args):
        ans = Vector(self)
        for arg in args:
            x = ans.y*arg.z - ans.z*arg.y
            y = ans.z*arg.x - ans.x*arg.z
            z = ans.x*arg.y - ans.y*arg.x
            ans.x = x
            ans.y = y
            ans.z = z
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
    
    def move(self, vect=None, dt=0.1):
        if vect is None:
            vect = Vector()
        da = vect.div(self.m).sub(self.a)
        dv = self.a.add(da.div(2)).mult(dt)
        ds = self.v.add(dv.div(2), da.mult(-dt/3)).mult(dt)
        self.a = self.a.add(da)
        self.v = self.v.add(dv)
        self.s = self.s.add(ds)
