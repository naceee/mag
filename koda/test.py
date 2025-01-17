from point_sampling import positive_sphere, get_non_dominated_points
import numpy as np
from main import get_kink_points, distance_to_pareto_front, state_dominates_point


def test_algorithm(n_points=100, dim=4, n_tests=10):

    for _ in range(n_tests):
        random_points = get_non_dominated_points(n_points, dim, mode="linear")
        kink_points = get_kink_points(random_points, dim)

        test_point = np.random.random(dim)
        while not state_dominates_point(kink_points, test_point, dim):
            test_point = np.random.random(dim)

        test_one_point(kink_points, test_point, dim)


def test_one_point(kink_points, test_point, dim, min_eps=0.001, eps=1):
    distance = distance_to_pareto_front(kink_points, test_point)
    print(f"Distance: {distance}")
    while eps > min_eps:
        check_distance = (1 + eps) * distance
        print(f"{eps:.6f} {round(check_distance, 8):.8f}: ", end="")
        m = 1
        max_m = 10e7
        found = False
        while m < max_m:
            test_points = positive_sphere(check_distance, m, dim)
            for point in test_points:
                if not state_dominates_point(kink_points, test_point + point, dim):
                    print(f"Found point with distance {check_distance}")
                    found = True
                    break
            if not found:
                print(f".", end="")
                m *= 2
            else:
                break

        if not found:
            print(f"No nondominated points found with epsilon {eps}")
            break
        else:
            eps /= 2


if __name__ == '__main__':
    test_algorithm()
