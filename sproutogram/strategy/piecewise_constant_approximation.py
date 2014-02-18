import numpy as np


def full_piecewise_constants(signal):
    u = primal_dual_hybrid_gradient(signal)
    indices = np.unique(u, return_index=True)[1]
    return u, u[sorted(indices)]


def approximate_piecewise_constants(signal):
    u = primal_dual_hybrid_gradient(signal)
    indices = np.unique(u, return_index=True)[1]
    return u[sorted(indices)]


def primal_dual_hybrid_gradient(signal, alpha=0.5, delta=0.5, mu=10, maxiter=5000):
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
        p = projection(p_old + delta * forward_difference(u_old), mu)

        # u update
        u = (1 / (1 + alpha)) * \
            (u_old + alpha * \
                (signal - backward_difference(p)))

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


def forward_difference(u):
    """Forward difference operator. """
    first_derivative = np.zeros(len(u))
    for i in range(len(u) - 1):
        first_derivative[i] = u[i + 1] - u[i]
    first_derivative[len(u) - 1] = first_derivative[len(u) - 2]
    return first_derivative


def backward_difference(u):
    """Backwards difference operator."""
    backwards_difference = np.zeros(len(u))
    for i in range(1, len(u)):
        backwards_difference[i] = -(u[i] - u[i - 1])
    backwards_difference[0] = backwards_difference[1]
    return backwards_difference
