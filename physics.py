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
		if isinstance(other, Vector):
			return self.x==other.x and self.y==other.y and self.z==other.z
		else:
			return False
	
	def add(self, *args):
		ans = Vector(self)
		for arg in args:
			ans.x += arg.x
			ans.y += arg.y
			ans.z += arg.z
		return
		
	def sub(self, *args):
		ans = Vector(self)
		for arg in args:
			ans.x -= arg.x
			ans.y -= arg.y
			ans.z -= arg.z
		return
		
	def mult(self, *args):
		ans = Vector(self)
		for arg in args:
			ans.x *= arg
			ans.y *= arg
			ans.z *= arg
		return
		
	def div(self, *args):
		ans = Vector(self)
		for arg in args:
			if arg:
				ans.x /= arg
				ans.y /= arg
				ans.z /= arg
		return
	
	def mag(self):
		return (self.x**2 + self.y**2 + self.z**2)**0.5
	
	def norm(self):
		return self.div(self.mag())
		
	def setMag(self, mag):
		return self.norm().mult(mag)
		
	def dot(self, vec):
		return self.x*vec.x + self.y*vec.y + self.z*vec.z
	
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
	
	def move(self, F=Vector(), dt=0.1):
		da = F.div(m).sub(self.a)
		dv = self.a.add(da.div(2)).mult(dt)
		ds = self.v.add(dv.div(2),da.mult(-dt/3)).mult(dt)
		self.a = self.a.add(da)
		self.v = self.v.add(dv)
		self.s = self.s.add(ds)
	
	
