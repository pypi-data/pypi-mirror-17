from math import exp, log, tanh
import numpy as np
from scipy.stats import invwishart

def ilogit(x):
    return 1/(1+np.exp(-x))

def logit(x):
    return np.log(x) - np.log(1 - x)

def transform_define(transform):
    """
    This function links the user's choice of transformation with the associated numpy function
    """
    if transform == 'tanh':
        return np.tanh
    elif transform == 'exp':
        return np.exp
    elif transform == 'logit':
        return ilogit
    elif transform is None:
        return np.array
    else:
        return None

def itransform_define(transform):
    """
    This function links the user's choice of transformation with its inverse
    """
    if transform == 'tanh':
        return np.arctanh
    elif transform == 'exp':
        return np.log
    elif transform == 'logit':
        return logit
    elif transform is None:
        return np.array
    else:
        return None

def itransform_name_define(transform):
    """
    This function is used for model results table, displaying any transformations performed
    """
    if transform == 'tanh':
        return 'arctanh'
    elif transform == 'exp':
        return 'log'
    elif transform == 'logit':
        return 'ilogit'
    elif transform is None:
        return ''
    else:
        return None

class Normal(object):

    def __init__(self, mu0, sigma0, transform=None):
        self.mu0 = mu0
        self.sigma0 = sigma0
        self.transform_name = transform     
        self.transform = transform_define(transform)
        self.itransform = itransform_define(transform)
        self.itransform_name = itransform_name_define(transform)
        self.covariance_prior = False

    def logpdf(self,mu):
        if self.transform is not None:
            mu = self.transform(mu)     
        return -log(float(self.sigma0)) - (0.5*(mu-self.mu0)**2)/float(self.sigma0**2)

    def pdf(self,mu):
        if self.transform is not None:
            mu = self.transform(mu)             
        return (1/float(self.sigma0))*exp(-(0.5*(mu-self.mu0)**2)/float(self.sigma0**2))

class Uniform(object):

    def __init__(self, transform=None):
        self.transform_name = transform     
        self.transform = transform_define(transform)
        self.itransform = itransform_define(transform)
        self.itransform_name = itransform_name_define(transform)
        self.covariance_prior = False

    def logpdf(self,mu):
        return 0.0


class TruncatedNormal(object):

    def __init__(self, mu0, sigma0, lower=None, upper=None, transform=None):
        self.mu0 = mu0
        self.sigma0 = sigma0
        self.transform_name = transform     
        self.transform = transform_define(transform)
        self.itransform = itransform_define(transform)
        self.itransform_name = itransform_name_define(transform)
        self.covariance_prior = False
        self.lower = lower
        self.upper = upper

    def logpdf(self, mu):
        if self.transform is not None:
            mu = self.transform(mu)     
        if mu < self.lower and self.lower is not None:
            return -10.0**6
        elif mu > self.upper and self.upper is not None:
            return -10.0**6
        else:
            return -log(float(self.sigma0)) - (0.5*(mu-self.mu0)**2)/float(self.sigma0**2)

    def pdf(self, mu):
        if self.transform is not None:
            mu = self.transform(mu)    
        if mu < self.lower and self.lower is not None:
            return 0.0
        elif mu > self.upper and self.upper is not None:
            return 0.0       
        else:
            return (1/float(self.sigma0))*exp(-(0.5*(mu-self.mu0)**2)/float(self.sigma0**2))


class Uniform(object):

    def __init__(self, transform=None):
        self.transform_name = transform     
        self.transform = transform_define(transform)
        self.itransform = itransform_define(transform)
        self.itransform_name = itransform_name_define(transform)
        self.covariance_prior = False

    def logpdf(self,mu):
        return 0.0


class InverseGamma(object):

    def __init__(self, alpha, beta, transform='exp'):
        self.alpha = alpha
        self.beta = beta
        self.transform_name = transform
        self.transform = transform_define(transform)
        self.itransform = itransform_define(transform)
        self.itransform_name = itransform_name_define(transform)
        self.covariance_prior = False

    def logpdf(self,x):
        if self.transform is not None:
            x = self.transform(x)       
        return (-self.alpha-1)*log(x) - (self.beta/float(x))

    def pdf(self,x):
        if self.transform is not None:
            x = self.transform(x)               
        return (x**(-self.alpha-1))*exp(-(self.beta/float(x)))


class InverseWishart(object):

    def __init__(self,v,Psi):
        self.v = v
        self.Psi = Psi
        self.covariance_prior = True
        self.transform_name = None     
        self.transform = transform_define(None)
        self.itransform = itransform_define(None)
        self.itransform_name = itransform_name_define(None)

    def logpdf(self,X):
        return invwishart.logpdf(X, df=self.v, scale=self.Psi)

    def pdf(self,X):
        return invwishart.pdf(X, df=self.v, scale=self.Psi)


