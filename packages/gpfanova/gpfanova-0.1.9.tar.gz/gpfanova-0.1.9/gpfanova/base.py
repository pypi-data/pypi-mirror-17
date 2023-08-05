from patsy.contrasts import Sum
from sample import SamplerContainer, Slice, Fixed, Function, FunctionDerivative
from kernel import RBF, White
import numpy as np
import scipy.stats, logging

class Base(SamplerContainer):
	"""Base for constructing functional models of the form $y(t) = X \times b(t)$

	Subclasses must implement the functions _buildDesignMatrix and priorGroups.
	_buildDesignMatrix defines the design matrix for the model, such that
	$y_i(t) = X_i b(t)$ for design matrix $X$. priorGroups returns a list of lists,
	where each list defines a grouping of functions who share a GP prior.
	"""

	def __init__(self,x,y,hyperparam_kwargs={},derivatives=False,*args,**kwargs):
		""" Construct the base functional model.

		Args:
			x: np.array (n x p), independent variables (not the design matrix!),
				where obesrvations have been made
			y: np.array (n x r), funtion observations
		"""

		self.x = x # independent variables
		self.y = y # dependent variables

		# this list will hold the strings representing the values where
		# functions are to be sampled, e.g. x_1, x_2, ...
		self._observationIndexBaseList = None

		self.n = self.x.shape[0]
		assert self.y.shape[0] == self.n, 'x and y must have same first dimension shape!'
		self.p = self.x.shape[1]
		self.m = self.y.shape[1]

		self.design_matrix = None
		self.buildDesignMatrix()

		# number of functions being estimated
		self.f = self.design_matrix.shape[1]

		if self.f > np.linalg.matrix_rank(self.design_matrix):
			logger = logging.getLogger(__name__)
			logger.error("design matrix is of rank %d, but there are %d functions!"%(np.linalg.matrix_rank(self.design_matrix),self.f))

		if np.any(np.isnan(self.y)):
			logger = logging.getLogger(__name__)
			logger.error("NaN values in observation matrix, this is not supported yet!")

		# kernel and sampler
		self.y_k = White(self,['y_sigma'],logspace=True)
		w,m = .1,10
		if 'y_sigma' in hyperparam_kwargs:
			w,m = hyperparam_kwargs['y_sigma']
		elif 'sigma' in hyperparam_kwargs:
			w,m = hyperparam_kwargs['sigma']
		samplers = [Slice('y_sigma','y_sigma',self.observationLikelihood,w,m)]

		# function priors
		self.kernels = []
		fxn_names = self.functionNames()
		for i,p in enumerate(self.priorGroups()):
			self.kernels.append(RBF(self,['prior%d_sigma'%i]+['prior%d_lengthscale%d'%(i,d) for d in range(self.p)],logspace=True))

			for f in p:
				if f in fxn_names:
					s = fxn_names[f]
				else:
					s = "f%d"%f
				samplers.append(Function('%s'%s,self.functionIndex(f),self,f,self.kernels[-1]))

				if derivatives:
					for d in range(self.p):
						samplers.append(FunctionDerivative('d%s'%s,d,self.functionIndex(f,derivative=True),self,f,self.kernels[-1]))

			w,m = .1,10
			if 'sigma' in hyperparam_kwargs:
				w,m = hyperparam_kwargs['sigma']
			samplers.append(Slice('prior%d_sigma'%i,'prior%d_sigma'%i,lambda x,p=i: self.prior_likelihood(p,x),w,m))

			w,m = .1,10
			if 'lengthscale' in hyperparam_kwargs:
				w,m = hyperparam_kwargs['lengthscale']

			for d in range(self.p):
				samplers.append(Slice('prior%d_lengthscale%d'%(i,d),'prior%d_lengthscale%d'%(i,d),lambda x,p=i,d=d: self.prior_likelihood(p=p,**{'prior%d_lengthscale%d'%(p,d):x}),w,m))
		samplers.extend(self._additionalSamplers())

		SamplerContainer.__init__(self,samplers,**kwargs)

	def _additionalSamplers(self):
		"""Additional samplers for the model, can be overwritten by subclasses."""
		return []

	def functionNames(self):
		"""Function names, can be overwritten by subclasses.

		returns:
			dict(index:name), keys indicate function index in the
				design matrix, with values representing the name to use for the
				function."""
		return {}

	def buildDesignMatrix(self):
		if self.design_matrix is None:
			self.design_matrix = self._buildDesignMatrix()

	def _buildDesignMatrix(self):
		"""Build a design matrix defining the relation between observations and underlying functions.

		The returned matrix should be shape (n,f), where n is the number observation points,
		and f is the number of functions to be estimated. f will be infered by the
		shape of the matrix returned from this function.
		"""
		raise NotImplementedError("Implement a design matrix for your model!")

	def functionIndex(self,i,derivative=False,*args,**kwargs):
		"""return the parameter_cache indices for function i"""
		if derivative:
			return ['df%d(%s)'%(i,z) for z in self._observationIndexBase()]
		return ['f%d(%s)'%(i,z) for z in self._observationIndexBase()]

	def functionPrior(self,f):
		"""return the prior index for function f."""

		priors = self.priorGroups()
		for i in range(len(priors)):
			if f in priors[i]:
				return i
		return -1

	def _observationIndexBase(self):
		"""return the base indice structure from the observations.

		returns:
			list of strings
		"""
		if self._observationIndexBaseList is None:
			self._observationIndexBaseList = ['%s'%str(z) for z in self.x]

		return self._observationIndexBaseList

	def priorGroups(self):
		raise NotImplementedError("Implement a prior grouping function for your model!")

	def _priorParameters(self,i):
		if i < 0:
			return ['y_sigma']
		if i >= len(self.priorGroups()):
			return [None]

		return ['prior%d_sigma'%i]+['prior%d_lengthscale%d'%(i,d) for d in range(self.p)]

	def functionMatrix(self,remove=[],only=[],derivative=False):
		"""return the current function values, stored in the parameter_cache."""

		functions = []

		if len(only) > 0:
			for o in only:
				functions.append(self.functionIndex(o,derivative=derivative))
		else:
			for f in range(self.f):
				if f in remove:
					functions.append(None)
				else:
					functions.append(self.functionIndex(f,derivative=derivative))

		f = np.zeros((self.n,len(functions)))

		for i,z in enumerate(functions):
			if z is None:
				f[:,i] = 0
			else:
				f[:,i] = self.parameter_cache[z]

		return f

	def functionSamples(self,f,*args,**kwargs):
		"""return the samples of function f from the parameter history."""
		return self.parameter_history[self.functionIndex(f,*args,**kwargs)]

	def residual(self,remove=[],only=[]):
		return self.y.T - np.dot(self.design_matrix,self.functionMatrix(remove,only).T)

	def functionResidual(self,f):
		"""compute the residual Y-Mb, without the function f."""
		resid = self.residual(remove=[f])

		resid = (resid.T / self.design_matrix[:,f].T).T
		resid = resid[self.design_matrix[:,f]!=0,:]

		return resid

	def offset(self):
		"""offset for the calculation of covariance matrices inverse"""
		return 1e-9

	def observationMean(self):
		"""The *conditional* mean of the observations given all functions"""
		return np.dot(self.design_matrix,self.functionMatrix().T).ravel()

	def observationLikelihood(self,sigma=None):
		"""Compute the conditional likelihood of the observations y given the design matrix and latent functions"""
		y = np.ravel(self.y.T)
		mu = self.observationMean()
		sigma = pow(10,sigma)

		# remove missing values
		mu = mu[~np.isnan(y)]
		y = y[~np.isnan(y)]

		return np.sum(scipy.stats.norm.logpdf(y-mu,0,sigma))

	def prior_likelihood(self,p,*args,**kwargs):
		"""Compute the likelihood of functions with prior p, for the current/provided hyperparameters"""

		ind = self.priorGroups()[p]

		mu = np.zeros(self.n)
		cov = self.kernels[p].K(self.x,*args,**kwargs)
		# cov += cov.mean()*np.eye(self.n)*1e-6

		# use cholesky jitter code to find PD covariance matrix
		diagA = np.diag(cov)
		if np.any(diagA <= 0.):
			raise linalg.LinAlgError("not pd: non-positive diagonal elements")
		jitter = diagA.mean() * 1e-6
		num_tries = 1
		maxtries=10
		while num_tries <= maxtries and np.isfinite(jitter):
			try:
				rv = scipy.stats.multivariate_normal(mu,cov + np.eye(cov.shape[0]) * jitter)
				break
			except:
				jitter *= 10
			finally:
				num_tries += 1

		# rv = scipy.stats.multivariate_normal(mu,cov)

		ll = 1
		for f in ind:
			try:
				ll += rv.logpdf(self.parameter_cache[self.functionIndex(f)])
			except np.linalg.LinAlgError:
				logger = logging.getLogger(__name__)
				logger.error("prior likelihood LinAlgError (%d,%d)" % (p,f))

		# print "prior_likelihood (%d): %s"%(p,str(kwargs)),ll

		return ll

	def samplePrior(self,):

		# sample the hyperparameters

		## sample the latent functions
		samples = np.zeros((self.f,self.n))
		for i in range(self.f):
			mu = np.zeros(self.n)
			cov = self.kernels[self.functionPrior(i)].K(self.x)
			samples[i,:] = scipy.stats.multivariate_normal.rvs(mu,cov)

		## put into data
		y = np.dot(self.design_matrix,samples) + np.random.normal(0,np.sqrt(pow(10,self.parameter_cache['y_sigma'])),size=(self.m,self.n))

		return y.T,samples.T
