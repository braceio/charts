
import random
import math

def _exp(width):
	spread = random.choice(range(10))
	return lambda n: math.exp(n*math.e/(width*(1.1+spread/10.0)))-1

def _flat(width):
	offset = random.random()*5.0
	return lambda n: offset

def _bell(width):
	return lambda n: 10/(math.exp((n-width*0.5+0.5)**2))

def _hockey(width):
	spread = random.choice(range(10))
	return lambda n: math.pow(n*math.e/(width*(1.16)), math.e*(1.1+spread/40.0))

FUNC_MAP = {
	'lorem_exp': _exp,
	'lorem_flat': _flat,
	'lorem_rand': _flat,
	'lorem_bell': _bell,
	'lorem_hockey': _hockey,
}

def loremdata(kind, width=10):
	fn = FUNC_MAP.get(kind, _exp)(width)
	values = [fn(n) for n in range(0,width)]
	scale = (max(values) - min(values))/10.0 or 1
	return [round(n+random.random()*scale,1) for n in values]

