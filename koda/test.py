from point_sampling import positive_sphere, get_non_dominated_points
import numpy as np
from main import get_kink_points, state_dominates_point, dist_to_kink_points
import warnings


def test_algorithm(n_points=10, dim=3, n_tests=10):
    for _ in range(n_tests):
        non_dominated_points = get_non_dominated_points(n_points, dim, mode="linear")

        test_point = np.random.random(dim)
        while not state_dominates_point(non_dominated_points, test_point, dim):
            test_point = np.random.random(dim)

        test_one_point(non_dominated_points, test_point, dim)


def test_one_point(points, test_point, dim, min_eps=0.001, eps=1):
    kink_points = get_kink_points(points, dim)

    distance = dist_to_kink_points(kink_points, test_point, dim)
    print(f"Distance: {distance}")
    while eps > min_eps:
        check_distance = (1 + eps) * distance
        print(f"{eps:.6f} {round(check_distance, 8):.8f}: ", end="")

        found = sample_point_until_found(points, test_point, check_distance, dim)
        if not found:
            warnings.warn(f"Could not find point with distance very close to the given distance")
            break
        eps /= 2

    check_distance = distance - 10e-6
    found = sample_point_until_found(points, test_point, check_distance, dim)
    if found:
        raise Exception("ERROR: Found point with distance less than the actual distance")


def sample_point_until_found(points, test_point, max_distance, dim,
                             start_sample_size=1000, max_sample_size=10_000_000):

    while start_sample_size < max_sample_size:
        test_points = positive_sphere(max_distance, start_sample_size, dim)
        for point in test_points:
            if not state_dominates_point(points, test_point + point, dim):
                print(f"found point: {test_point + point}")
                return True

        print(f".", end="")
        start_sample_size *= 2
    return False


if __name__ == '__main__':
    test_algorithm()
