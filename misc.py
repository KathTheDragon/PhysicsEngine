class lazy_property(object):
    def __init__(self,fget):
        self.fget = fget
        self.func_name = fget.__name__

    def __get__(self,obj,cls):
        if obj is None:
            return None
        value = self.fget(obj)
        setattr(obj,self.func_name,value)
        return value

def binom(n, r):
	if n < r:
		return 0
	elif r == 0 or r == n:
		return 1
	elif r == 1 or r == n-1:
		return n
	else:
		if 2*r <= n:
			k = r
		else:
			k = n-r
		return binom(n-1,k-1)*n//k
