from math import cos, sin, asin, atan2

class Vector():
    def __init__(self, *args):
        self.x = args[0].x if args else 0
        self.y = args[0].y if args else 0
        self.z = args[0].z if args else 0
        self.r = args[0].r if args else 0
        self.theta = args[0].theta if args else 0
        self.phi = args[0].phi if args else 0
        return
    
    def __repr__(self):
        return "Vector({}, {}, {})".format(self.x, self.y, self.z)
        
    def __str__(self):
        return "({}, {}, {})".format(self.x, self.y, self.z)
        
    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __add__(self, arg):
        if isinstance(arg, Vector):
            return CVector(
                self.x + arg.x,
                self.y + arg.y,
                self.z + arg.z
            )
        else:
            return CVector(
                self.x + arg,
                self.y + arg,
                self.z + arg
            )
        
    def __radd__(self, val):
        return CVector(
            self.x + val,
            self.y + val,
            self.z + val
        )
        
    def __sub__(self, arg):
        if isinstance(arg, Vector):
            return CVector(
                self.x - arg.x,
                self.y - arg.y,
                self.z - arg.z
            )
        else:
            return CVector(
                self.x - arg,
                self.y - arg,
                self.z - arg
            )
        
    def __rsub__(self, val):
        return CVector(
            val - self.x,
            val - self.y,
            val - self.z
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
        
    def copy(self):
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
    def __init__(self, *args, **kwargs):
        if not args and not kwargs:
            super().__init__()
        elif len(args)==1 and isinstance(args[0],Vector):
            super().__init__(*args)
        else:
            self.x = args[0] if len(args) > 0 else 0
            self.y = args[1] if len(args) > 1 else 0
            self.z = args[2] if len(args) > 2 else 0
            if "x" in kwargs: self.x = kwargs["x"]
            if "y" in kwargs: self.y = kwargs["y"]
            if "z" in kwargs: self.z = kwargs["z"]
            self.r = (self.x**2 + self.y**2 + self.z**2)**0.5
            self.theta = atan2(self.y, self.x)
            self.phi = asin(self.z / self.r) if self.z else 0
        return

class PVector(Vector):
    def __init__(self, *args, **kwargs):
        if not args and not kwargs:
            super().__init__()
        elif len(args) == 1 and isinstance(args[0], Vector):
            super().__init__(*args)
        else:
            self.r = args[0] if len(args) > 0 else 0
            self.theta = args[1] if len(args) > 1 else 0
            self.phi = args[2] if len(args) > 2 else 0
            if "r" in kwargs: self.r = kwargs["r"]
            if "theta" in kwargs: self.theta = kwargs["theta"]
            if "phi" in kwargs: self.phi = kwargs["phi"]
            self.x = self.r * cos(self.theta) * cos(self.phi)
            self.y = self.r * sin(self.theta) * cos(self.phi)
            self.z = self.r * sin(self.phi) if self.phi else 0
        return

class Body():
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], Body):
            self.m = args[0].m
            self.i = args[0].i
            self.s = Vector(args[0].s)
            self.v = Vector(args[0].v)
            self.a = Vector(args[0].a)
            self.theta = PVector(args[0].theta)
            self.omega = PVector(args[0].omega)
            self.alpha = PVector(args[0].alpha)
        else:
            self.m = args[0] if len(args) > 0 else 1
            self.i = args[1] if len(args) > 1 else 1
            self.s = Vector(args[2]) if len(args) > 2 else Vector()
            self.v = Vector(args[3]) if len(args) > 3 else Vector()
            self.a = Vector(args[4]) if len(args) > 4 else Vector()
            self.theta = PVector(args[5]) if len(args) > 5 else PVector(1)
            self.omega = PVector(args[6]) if len(args) > 6 else PVector()
            self.alpha = PVector(args[7]) if len(args) > 7 else PVector()
            if "m" in kwargs: self.m = kwargs["m"]
            if "i" in kwargs: self.i = kwargs["i"]
            if "s" in kwargs: self.s = Vector(kwargs["s"])
            if "v" in kwargs: self.v = Vector(kwargs["v"])
            if "a" in kwargs: self.a = Vector(kwargs["a"])
            if "theta" in kwargs: self.theta = PVector(kwargs["theta"])
            if "omega" in kwargs: self.omega = PVector(kwargs["omega"])
            if "alpha" in kwargs: self.alpha = PVector(kwargs["alpha"])
        return
        
    def copy(self):
        return Body(self)
    
    def move(self, force=None, moment=None):
        if force is None:
            force = Vector()
        if moment is None:
            moment = PVector()
        da = force / self.m - self.a
        dv = self.a + da / 2
        ds = self.v + dv / 2 - da / 3
        dalpha = moment / self.i - self.alpha
        domega = self.alpha + dalpha / 2
        dtheta = self.omega + domega / 2 - dalpha / 3
        self.a += da
        self.v += dv
        self.s += ds
        self.alpha += dalpha
        self.omega += domega
        self.theta += dtheta
        return

class Region():
    def __init__(self, *args):
        pass

