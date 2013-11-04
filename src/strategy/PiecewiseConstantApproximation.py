import scipy as sp
import numpy as np
import matplotlib.pyplot as plt

def fullPWConstants(signal):
	u = PDHG(signal)
	indices = np.unique(u, return_index=True)[1]
	return u, u[sorted(indices)]

def appxPWConstants(signal):
	u = PDHG(signal)
	indices = np.unique(u, return_index=True)[1]
	return u[sorted(indices)]

def PDHG(signal, alpha=0.5, delta=0.5, mu=10, maxiter=5000):
	"""
	Primal-Dual Hybrid Gradient method for solving for piecewise
	constant approximations of a discrete, 1D signal.
	"""
	n = len(signal)
	p = np.zeros(len(signal), dtype=np.float64)
	u = np.zeros(len(signal), dtype=np.float64)

	energy = float('inf')
	for i in range(maxiter):
		p_old = p
		u_old = u

		# p update
		p = projection(p_old + delta * forwardDifference(u_old), mu)

		# u update
		u = (1 / (1 + alpha)) * \
			(u_old + alpha * \
				(signal - backwardDifference(p)))

		energy = np.linalg.norm(u - u_old) / np.linalg.norm(u)

		# convergence check
		if energy == 0:
			break
	# print '\tEnergy: %.2f' % energy
	return u

def projection(vector, mu):
	"""
	Projects a specified vector into a box bounded by mu.
	"""
	return np.divide(vector, np.maximum(abs(vector) / mu, 1))

def forwardDifference(u):
	"""Forward difference operator. """
	firstDerivative = np.zeros(len(u))
	for i in range(len(u) - 1):
		firstDerivative[i] = u[i + 1] - u[i]
	firstDerivative[len(u) - 1] = firstDerivative[len(u) - 2]
	return firstDerivative
		
def backwardDifference(u):
	"""Backwards difference operator."""
	backwardDifference = np.zeros(len(u))
	for i in range(1, len(u)):
		backwardDifference[i] = -(u[i] - u[i - 1])
	backwardDifference[0] = backwardDifference[1]
	return backwardDifference
