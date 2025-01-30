from point_sampling import random_sphere_points, get_non_dominated_points, sample_random_dominated_point
import numpy as np
from main import get_kink_points, dist_to_kink_points
import warnings
from utils import state_dominates_point


def test_algorithm(n_points=100, n_tests=10):
    for dim in range(3, 11):
        for test_idx in range(n_tests):
            non_dominated_points = get_non_dominated_points(n_points, dim, mode="random")
            test_point = sample_random_dominated_point(non_dominated_points, dim)

            print(f"({dim}.{test_idx})", end=" ")
            test_one_point(non_dominated_points, test_point, dim)


def test_one_point(points, test_point, dim, min_eps=0.001, eps=1):
    kink_points = get_kink_points(points, dim)

    distance = dist_to_kink_points(kink_points, test_point, dim)
    print(f"CALCULATED DISTANCE: {distance:.6f}")
    print(f"   eps    |   dist   | found |  n points  |")
    print(f"-------------------------------------------")
    while eps > min_eps:
        check_distance = (1 + eps) * distance
        print(f" {eps:.6f} | {round(check_distance, 8):.6f} |", end="")

        found = sample_point_until_found(points, test_point, check_distance, dim)
        if not found:
            warnings.warn(f"Could not find point with distance very close to the given distance")
            break
        eps /= 2

    eps = -10e-6
    check_distance = (1 + eps) * distance
    print(f"-------------------------------------------")
    print(f"{eps:.6f} | {round(check_distance, 8):.6f} |", end="")
    found = sample_point_until_found(points, test_point, check_distance, dim)
    if found:
        raise Exception("ERROR: Found point with distance less than the actual distance")
    print()


def sample_point_until_found(points, test_point, max_distance, dim,
                             start_sample_size=1, max_sample_size=1_000_000):

    while start_sample_size < max_sample_size:
        test_points = random_sphere_points(max_distance, start_sample_size, dim)
        for point in test_points:
            if not state_dominates_point(points, test_point + point, dim):
                print(f" \033[92myes\033[0m   | {2*start_sample_size:10d} |")
                return True

        start_sample_size *= 2

    print(f" \033[91mno\033[0m    | {start_sample_size:10d} |")
    return False


if __name__ == '__main__':
    test_algorithm()
