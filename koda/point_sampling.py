import math
import random
import numpy as np

from utils import weakly_dominates, state_dominates_point


def get_non_dominated_points(n_points, n_dim=3, mode='spherical'):
    """ Returns a list of non-dominated points:
     - n_points: number of points
     - n_dim: number of dimensions
     - mode: 'spherical' or 'linear' """
    if mode == "random":
        return remove_dominated_points(np.random.random((n_points, n_dim)), n_dim)
    elif mode == "linear":
        return linear_front_nd(1, n_points, n_dim)
    elif mode == "spherical":
        if n_dim == 2:
            return spherical_front_2d(1, n_points)
        if n_dim == 3:
            return spherical_front_3d(1, n_points)
        elif n_dim == 4:
            return spherical_front_4d(1, n_points)
        else:
            raise ValueError("Invalid number of dimensions")
    else:
        raise ValueError("Invalid mode")


def spherical_front_2d(distance, num_points):
    """ Returns a list of non-dominated points on the 2D spherical front """
    vectors = []
    while len(vectors) < num_points:
        phi = random.random() * math.pi / 2
        vectors.append((1 - distance * math.cos(phi), 1 - distance * math.sin(phi)))

    return vectors


def spherical_front_3d(distance, num_points):
    """ Returns a list of non-dominated points on the 3D spherical front """
    vectors = []
    while len(vectors) < num_points:
        x, y, z = 1, 1, 1

        while (math.sqrt(x * x + y * y + z * z) > 1) or (x < 0.5 and y < 0.5 and z < 0.5):
            x = next_gaussian_double()
            y = next_gaussian_double()
            z = next_gaussian_double()

        r1 = math.sqrt(x * x + y * y + z * z)
        alpha = math.acos(z / r1)
        beta = math.atan2(y, x)

        vect = (1 - distance * math.sin(alpha) * math.cos(beta),
                1 - distance * math.sin(alpha) * math.sin(beta),
                1 - distance * math.cos(alpha))
        vectors.append(vect)

    return vectors


def linear_front_nd(distance, num_points, dim):
    array = np.hstack([
        np.zeros((num_points, 1)),
        distance * np.random.rand(num_points, dim - 1),
        distance * np.ones((num_points, 1))])
    array = np.sort(array, axis=1)
    vectors = 1 - np.diff(array, axis=1)
    return [tuple(v) for v in vectors]


def spherical_front_4d(distance, num_points):
    """ Returns a list of non-dominated points on the 4D spherical front """
    vectors = []
    while len(vectors) < num_points:
        x, y, z, w = 1, 1, 1, 1

        while (math.sqrt(x * x + y * y + z * z + w * w) > 1) or \
                (x < 0.5 and y < 0.5 and z < 0.5 and w < 0.5):
            x = next_gaussian_double()
            y = next_gaussian_double()
            z = next_gaussian_double()
            w = next_gaussian_double()

        alpha = math.atan(math.sqrt(y * y + z * z + w * w) / x)
        beta = math.atan(math.sqrt(z * z + w * w) / y)
        gamma = 2 * math.atan(z / (math.sqrt(z * z + w * w) + w))

        vectors.append((
            distance * math.cos(alpha),
            distance * math.sin(alpha) * math.cos(beta),
            distance * math.sin(alpha) * math.sin(beta) * math.cos(gamma),
            distance * math.sin(alpha) * math.sin(beta) * math.sin(gamma)
        ))

    return vectors


def positive_sphere(distance, num_points, dim):
    """ Returns a list of non-dominated points on the n-D sphere """
    vectors = np.random.normal(0, 1, (num_points, dim))
    vectors = np.abs(vectors)
    vectors = vectors / np.linalg.norm(vectors, axis=1)[: , np.newaxis]
    vectors = vectors * distance
    return vectors


def next_gaussian_double():
    factor = 2.0
    while True:
        result = random.gauss(0, 1)
        if result < -factor:
            continue
        if result > factor:
            continue
        if result >= 0:
            result = result / (2 * factor)
        else:
            result = (2 * factor + result) / (2 * factor)
        return result


def remove_dominated_points(points, dim):
    """ Removes dominated points from a list of points """
    non_dominated_points = []
    for p1 in points:
        dominated = False
        for p2 in points:
            if weakly_dominates(p2, p1, dim) and not np.array_equal(p1, p2):
                dominated = True
                break
        if not dominated:
            non_dominated_points.append(tuple(p1))
    return non_dominated_points


def random_dominated_point(points, dim):
    """ Randomly samples point until it is dominated by at least one point in points """
    random_point = np.random.random(dim)
    while not state_dominates_point(points, random_point, dim):
        random_point = np.random.random(dim)
    return tuple(random_point)


if __name__ == "__main__":
    ps = linear_front_nd(1, 1000, 3)

    import plotly.graph_objects as go
    fig = go.Figure()
    fig.add_trace(go.Scatter3d(
        x=[p[0] for p in ps],
        y=[p[1] for p in ps],
        z=[p[2] for p in ps],
        mode='markers',
        marker=dict(size=4)
    ))
    fig.show()
