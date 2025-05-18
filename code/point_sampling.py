import math
import numpy as np

from utils import weakly_dominates, state_dominates_point


def get_non_dominated_points(n_points, n_dim=3, mode='spherical', distance=1):
    """ Returns a list of non-dominated points:
     - n_points: number of points
     - n_dim: number of dimensions
     - mode: 'spherical', 'linear' or 'random'

     in case of 'random' mode, the n_points parameter refers to the number of
     all points sampled, and not to the number of non-dominated points that are returned.
    """
    if mode == "random":
        return remove_dominated_points(np.random.random((n_points, n_dim)))
    elif mode == "linear":
        front = linear_front(distance, n_points, n_dim)
        return [tuple(v) for v in front]
    elif mode == "spherical":
        front = spherical_front(distance, n_points, n_dim)
        return [tuple(v) for v in front]
    else:
        raise ValueError("Invalid mode")


def linear_front(distance, num_points, dim):
    """ Returns a list of points non-dominated points on the linear front """
    array = np.hstack([
        np.zeros((num_points, 1)),
        distance * np.random.rand(num_points, dim - 1),
        distance * np.ones((num_points, 1))])
    array = np.sort(array, axis=1)
    vectors = np.diff(array, axis=1)
    return vectors


def spherical_front(distance, num_points, dim):
    """ Returns a list of non-dominated points on the n-D sphere """
    vectors = np.random.normal(0, 1, (num_points, dim))
    vectors = np.abs(vectors)
    vectors = vectors / np.linalg.norm(vectors, axis=1)[:, np.newaxis]
    vectors = vectors * distance
    return vectors


def epsilon_net(radius, epsilon, dim):
    """ Returns a list of non-dominated points on the n-D sphere """
    h = (2 * epsilon) / (radius * np.power((dim - 1), 1 / 2)) # TODO: preveri...
    net = epsilon_net_rec(h, dim, np.pi / 2, np.array([[1.0]]))
    return [[radius * p for p in point] for point in net]


def epsilon_net_rec(h, dim, area, vectors):
    """ Returns a list of non-dominated points on the n-D sphere """
    phi_space = np.linspace(0, np.pi / 2, math.ceil(area / h + 1))

    if dim == 2:
        new_vectors = [get_new_vectors(vectors, phi) for phi in phi_space]
        return np.vstack(new_vectors)

    new_vectors = [epsilon_net_rec(h, dim - 1, np.cos(phi) * area, get_new_vectors(vectors, phi))
                   for phi in phi_space]
    return np.vstack(new_vectors)


def get_new_vectors(vectors, phi):
    x0 = vectors[:, 0] * np.cos(phi)
    x1 = vectors[:, 0] * np.sin(phi)
    rest = vectors[:, 1:]
    new_vectors = np.column_stack((x0, x1, rest))
    return new_vectors


def remove_dominated_points(points):
    """ Removes dominated points from a list of points """
    non_dominated_points = []
    for p1 in points:
        dominated = False
        for p2 in points:
            if weakly_dominates(p2, p1) and not np.array_equal(p1, p2):
                dominated = True
                break
        if not dominated:
            non_dominated_points.append(tuple(p1))
    return non_dominated_points


def sample_random_dominated_point(front, dim):
    """ Randomly samples point until it is dominated by at least one point from the front """
    random_point = np.random.random(dim)
    while not state_dominates_point(front, random_point):
        random_point = np.random.random(dim)
    return tuple(random_point)
