import random as pyrandom
import pandas as pd
import scipy, time

class Sampler(object):

	def __init__(self,name,_type,parameters,current_param_dependent=False,*args,**kwagrs):
		"""
		Args:
			current_param_dependent: does the _sample function depend on the current parameter estimate? e.g. slice sampling, MH
		"""
		self.name = name
		self.type = _type
		self.current_param_dependent = current_param_dependent

		if type(parameters) == str:
			self.parameters = [parameters]
		else:
			self.parameters = parameters

		self.container = None

	def setContainer(self,c):
		self.container = c

	def sample(self,*args,**kwargs):
		args = []
		if self.current_param_dependent:
			args = [self.container.get(p) for p in self.parameters]
			
			# just use the parameter value if length one
			# if len(args) == 1:
			# 	param = param[0]
			#
			# args += [param]

		return self._sample(*args,**kwargs)

	def _sample(self,*args,**kwargs):
		raise NotImplemented("implement this function for your sampler!")

	def __repr__(self):
		if len(self.parameters) < 3:
			return "%s (%s): %s" % (self.name, self.type, ', '.join(self.parameters))
		return "%s (%s): %s, ..." % (self.name, self.type, ', '.join(self.parameters[:3]))
