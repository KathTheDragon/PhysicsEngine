from math import cos, acos, sin, asin, atan2
from misc import lazy_property, binom

class Vector():
    def __init__(self, *args):
        if not args or len(args)==1 and isinstance(args[0],Vector):
            self.x = args[0].x if args else 0
            self.y = args[0].y if args else 0
            self.z = args[0].z if args else 0
            self.r = args[0].r if args else 0
            self.theta = args[0].theta if args else 0
            self.phi = args[0].phi if args else 0
            return
        else:
            self.__init__()
    
    def __repr__(self):
        return "Vector" + str(self)
    
    def __str__(self):
        return "({}, {}, {})".format(self.x, self.y, self.z)
    
    def __eq__(self, other):
        return isinstance(other, Vector) and hash(self) == hash(other)
    
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
            return Quaternion(arg, self)
    
    def __radd__(self, val):
        return Quaternion(val, self)
    
    def __sub__(self, arg):
        if isinstance(arg, Vector):
            return CVector(
                self.x - arg.x,
                self.y - arg.y,
                self.z - arg.z
            )
        else:
            return Quaternion(-arg, self)
    
    def __rsub__(self, val):
        return Quaternion(val, -self)
    
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
    
    def __matmul__(self, vect):
        return self.x * vect.x + self.y * vect.y + self.z * vect.z
    
    def __pow__(self, val):
        if not val % 2:
            return (self@self)**(val/2)
        else:
            return self*(self@self)**((val-1)/2)
    
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
    
    @lazy_property
    def mag(self):
        return self.r
    
    @lazy_property
    def unit(self):
        return PVector(
            1,
            self.theta,
            self.phi
        )
    
    def setMag(self, val):
        return PVector(
            val,
            self.theta,
            self.phi
        )
    
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
        return
    
    def __repr__(self):
        return "CVector({}, {}, {})".format(self.x, self.y, self.z)
    
    @lazy_property
    def r(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5
    
    @lazy_property
    def theta(self):
        return atan2(self.y, self.x)
    
    @lazy_property
    def phi(self):
        return asin(self.z / self.r) if self.z else 0
    
    def __mul__(self, arg):
        if isinstance(arg, Vector):
            return CVector(
                self.y*arg.z - self.z*arg.y,
                self.z*arg.x - self.x*arg.z,
                self.x*arg.y - self.y*arg.x
            )
        else:
            return CVector(
                self.x * arg,
                self.y * arg,
                self.z * arg
            )
    
    def __rmul__(self, val):
        return CVector(
            self.x * val,
            self.y * val,
            self.z * val
        )
    
    def __div__(self, val):
        return CVector(
            self.x / val,
            self.y / val,
            self.z / val
        )
    
    def __neg__(self):
        return CVector(
            -self.x,
            -self.y,
            -self.z
        )
    
    @lazy_property
    def unit(self):
        return self / self.r
    
    def setMag(self, mag):
        return self.unit() * mag

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
        return
    
    def __repr__(self):
        return "PVector" + str(self)
    
    def __str__(self):
        return "({}, {}, {})".format(self.r, self.theta, self.phi)
    
    @lazy_property
    def x(self):
        return self.r * cos(self.theta) * cos(self.phi)
    
    @lazy_property
    def y(self):
        return self.r * sin(self.theta) * cos(self.phi)
    
    @lazy_property
    def z(self):
        return self.r * sin(self.phi) if self.phi else 0

class Quaternion():
    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], Quaternion):
            self.s = args[0].s
            self.v = Vector(args[0].v)
        else:
            self.s = args[0] if len(args) > 0 else 0
            self.v = Vector(args[1]) if len(args) > 1 else Vector()
        return
    
    def __repr__(self):
        return "Quaternion" + str(self)
    
    def __str__(self):
        return "({}, {}, {}, {})".format(self.s, self.v.x, self.v.y, self.v.z)
    
    def __eq__(self, other):
        return isinstance(other, Quaternion) and hash(self) == hash(other)
    
    def __hash__(self):
        return hash((self.s, self.v.x, self.v.y, self.v.z))
    
    def __add__(self, arg):
        if isinstance(arg,Quaternion):
            return (self.s + arg.s) + (self.v + arg.v)
        elif isinstance(arg,Vector):
            return self.s + (self.v + arg)
        else:
            return (self.s + arg) + self.v
    
    def __radd__(self, arg):
        if isinstance(arg,Vector):
            return self.s + (self.v + arg)
        else:
            return (self.s + arg) + self.v
    
    def __sub__(self, arg):
        if isinstance(arg,Quaternion):
            return (self.s - arg.s) + (self.v - arg.v)
        elif isinstance(arg,Vector):
            return self.s + (self.v - arg)
        else:
            return (self.s - arg) + self.v
    
    def __rsub__(self, arg):
        if isinstance(arg,Vector):
            return -self.s + (arg - self.v)
        else:
            return (arg - self.s) - self.v
        
    def __mul__(self, arg):
        if isinstance(arg, Quaternion):
            return Quaternion(
                self.s*arg.s - self.v@arg.v,
                self.s*arg.v + arg.s*self.v + self.v*arg.v
            )
        elif isinstance(arg, Vector):
            return (-self.v@arg) + (self.s*arg + self.v*arg)
        else:
            return (arg * self.s) + (arg * self.v)
    
    def __rmul__(self, arg):
        if isinstance(arg, Vector):
            return (-arg@self.v) + (self.s*arg + arg*self.v)
        else:
            return (arg * self.s) + (arg * self.v)
    
    def __div__(self, val):
        return (self.s / val) + (self.v / val)
    
    def __pow__(self, val):
        ans = 0
        for r in range(val+1):
            ans += (-1)**((r//2)%2)*binom(val,r)*q.s**(val-r)*q.v**r
        return ans
    
    def __neg__(self):
        return (-self.s) - self.v
    
    def __pos__(self):
        return Quaternion(self)
    
    def copy(self):
        return Quaternion(self)
    
    @lazy_property
    def mag(self):
        return (self.s**2 + self.v.r**2)**0.5
    
    @lazy_property
    def unit(self):
        return self / self.mag
    
    def setMag(self, val):
        return self.unit * val
    
    @lazy_property
    def conj(self):
        return self.s - self.v
    
    @lazy_property
    def inv(self):
        return self.conj / self.mag**2
    
class Rotation():
    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], Rotation):
            self.q = args[0].q
        elif len(args) == 1 and isinstance(args[0], Quaternion):
            self.q = args[0].unit
        else:
            self.theta = args[0] if len(args) > 0 else 0
            self.axis = Vector(args[1]) if len(args) > 1 else Vector(1,0,0)
            self.q = cos(self.theta) + self.axis.setMag(sin(self.theta))
        return
    
    @lazy_property
    def theta(self):
        return atan2(self.q.v.r, self.q.w)
    
    @lazy_property
    def axis(self):
        self.q.v
    
    def __add__(self, rot):
        return Rotation(rot.q * self.q)
    
    def __radd__(self, vect):
        w = self.q.s
        u = self.q.v
        v = vect
        return w*w*v + 2*w*u*v + u*(u@v) + u*(u*v)
        
    def __sub__(self, rot):
        return Rotation(rot.q.conj * self.q)
    
    def __rsub__(self, vect):
        w = self.q.s
        u = self.q.v
        v = vect
        return w*w*v - 2*w*u*v + u*(u@v) + u*(u*v)
    
    def __mul__(self, val):
        return Rotation(
            self.theta*arg,
            self.axis
        )
    
    def __rmul__(self, arg):
        return Rotation(
            self.theta*arg,
            self.axis
        )
    
    def __div__(self, arg):
        return Rotation(
            self.theta/arg,
            self.axis
        )
    
    def __neg__(self):
        return Rotation(self.q.conj)
    
    def __pos__(self):
        return Rotation(self)
    
    def copy(self):
        return Rotation(self)

class Body():
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], Body):
            self.m = args[0].m
            self.s = Vector(args[0].s)
            self.v = Vector(args[0].v)
            self.a = Vector(args[0].a)
            self.i = args[0].i
            self.theta = Rotation(args[0].theta)
            self.omega = Rotation(args[0].omega)
            self.alpha = Rotation(args[0].alpha)
        else:
            self.m = args[0] if len(args) > 0 else 1
            self.s = Vector(args[1]) if len(args) > 1 else Vector()
            self.v = Vector(args[2]) if len(args) > 2 else Vector()
            self.a = Vector(args[3]) if len(args) > 3 else Vector()
            self.i = args[4] if len(args) > 4 else 1
            self.theta = Rotation(args[5]) if len(args) > 5 else Rotation()
            self.omega = Rotation(args[6]) if len(args) > 6 else Rotation()
            self.alpha = Rotation(args[7]) if len(args) > 7 else Rotation()
            if "m" in kwargs: self.m = kwargs["m"]
            if "i" in kwargs: self.i = kwargs["i"]
            if "s" in kwargs: self.s = Vector(kwargs["s"])
            if "v" in kwargs: self.v = Vector(kwargs["v"])
            if "a" in kwargs: self.a = Vector(kwargs["a"])
            if "theta" in kwargs: self.theta = Rotation(kwargs["theta"])
            if "omega" in kwargs: self.omega = Rotation(kwargs["omega"])
            if "alpha" in kwargs: self.alpha = Rotation(kwargs["alpha"])
        return
        
    def copy(self):
        return Body(self)
    
    def move(self, force=None, moment=None):
        if force is None:
            force = Vector()
        da = force / self.m - self.a
        dv = self.a + da / 2
        ds = self.v + dv / 2 - da / 3
        self.a += da
        self.v += dv
        self.s += ds
        if moment is None:
            moment = Rotation()
        dalpha = moment / self.i - self.alpha
        domega = self.alpha + dalpha / 2
        dtheta = self.omega + domega / 2 - dalpha / 3
        self.alpha += dalpha
        self.omega += domega
        self.theta += dtheta
        return

class Region():
    def __init__(self, *args):
        pass

#To do: (maybe) consider rotations greater than 2pi
