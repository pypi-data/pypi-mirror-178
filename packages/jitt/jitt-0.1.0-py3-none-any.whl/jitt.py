#=======================================================
#
#	from jitt import Jitt
#	j = Jitt(delay=10.5, percent=25, precision=3).jitter
#	print(type(j))
#	print(j)
#
#=======================================================

import random

class Jitt:
	def __init__(self, delay, percent, precision):
		""" initialize delay as a float, percent as an integer, precision as an integer """
		self.delay = delay
		self.percent = percent
		self.precision = precision
		self.calculate_min_max()

	def calculate_min_max(self) -> float:
		""" calculates percent minimum and maximum ranges and returns the float value with desired precision """
		self.min = self.delay - (self.delay * (self.percent/100))
		self.max = self.delay + (self.delay * (self.percent/100))
		self.jitter = random.uniform(self.min, self.max)
		# round to given decimal places
		self.jitter = float(round(self.jitter, self.precision))