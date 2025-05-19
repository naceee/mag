from point_sampling import (remove_dominated_points, get_non_dominated_points,
                            sample_random_dominated_point, epsilon_net)
import numpy as np
from main import get_kink_points, dist_to_kink_points
from utils import state_dominates_point


def test_algorithm(n_points=100, n_tests=20, round_decimals=1):

    pts = [(1.0, 0.9, 0.7), (0.4, 1.0, 0.5), (0.8, 1.0, 0.2), (0.6, 1.0, 0.4), (0.5, 0.9, 1.0), (1.0, 0.7, 1.0)]
    test_point = (0.745, 0.355, 0.395)
    test_one_point(pts, test_point, 3)

    for dim in range(3, 11):
        for test_idx in range(n_tests):
            non_dominated_points = get_non_dominated_points(n_points, dim, mode="random")
            non_dominated_points = [[round(float(x), round_decimals) for x in pt]
                                    for pt in non_dominated_points]
            non_dominated_points = [pt for pt in non_dominated_points if all([x > 0 for x in pt])]
            non_dominated_points = remove_dominated_points(non_dominated_points)

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

        found = sample_epsilon_net_until_found(points, test_point, check_distance, dim, should_find=True)
        if not found:
            break
        eps /= 2

    eps = -10e-6
    check_distance = (1 + eps) * distance
    print(f"-------------------------------------------")
    print(f"{eps:.6f} | {round(check_distance, 8):.6f} |", end="")
    found = sample_epsilon_net_until_found(points, test_point, check_distance, dim, should_find=False)
    if found:
        print(points)
        print(test_point)
        raise Exception("ERROR: Found point with distance less than the actual distance")
    print()


def sample_epsilon_net_until_found(points, test_point, max_distance, dim,
                                   start_net_epsilon=1, max_sample_size=1_000_00, should_find=True):
    test_point = np.array(test_point)
    net_size = 0
    while net_size < max_sample_size:
        test_points = epsilon_net(max_distance, start_net_epsilon, dim)
        net_size = len(test_points)

        for point in test_points:
            if not state_dominates_point(points, test_point + point):
                if should_find:
                    print(f" \033[92myes\033[0m   | {net_size:10d} |")
                else:
                    print(f" \033[91myes\033[0m   | {net_size:10d} |")
                return True
        start_net_epsilon /= 2

    if should_find:
        print(f" \033[91mno\033[0m    | {net_size:10d} |")
    else:
        print(f" \033[92mno\033[0m    | {net_size:10d} |")

    return False


if __name__ == '__main__':
    test_algorithm()
