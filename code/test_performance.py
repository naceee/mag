import time
import numpy as np
import pandas as pd

from point_sampling import get_non_dominated_points, sample_random_dominated_point
from main import get_kink_points, dist_to_kink_points


def test_all():
    dims = [3, 4, 5, 6]
    front_types = ["linear", "spherical"]
    time_limit = 100
    n_repeats = 10

    for dim in dims:
        for front_type in front_types:
            for m in [1, 10, 100]:
                print(f"Testing {dim}-dim {front_type} front m={m}")
                test_algorithm(dim, front_type, m=m, n_repeats=n_repeats, time_limit=time_limit)


def test_algorithm(dim, front_type, m=1, n_repeats=10, time_limit=1):

    results = []
    front_size = 1
    time_exceeded = False

    while not time_exceeded:
        print(".", end="")
        times = np.zeros(n_repeats)
        n_kink_points = np.zeros(n_repeats)
        for test_idx in range(n_repeats):
            non_dominated_points = get_non_dominated_points(front_size, dim, mode=front_type)
            test_points = [sample_random_dominated_point(non_dominated_points, dim) for _ in range(m)]

            t, nkp = measure_time(non_dominated_points, test_points, dim)
            times[test_idx] = t
            n_kink_points[test_idx] = nkp
            if t > time_limit:
                time_exceeded = True
                break

        if not time_exceeded:
            for i, (t, nkp) in enumerate(zip(times, n_kink_points)):
                results.append((front_size, i, t, nkp))
            front_size *= 2

    results = pd.DataFrame(results, columns=["front_size", "idx", "time", "n_kink_points"])
    results.to_csv(f"../performance_results/results_dim={dim}_front={front_type}_m={m}.csv", index=False)
    print()


def measure_time(front, test_points, dim):
    t0 = time.time()
    kink_points = get_kink_points(front, dim)
    distances = [dist_to_kink_points(kink_points, point, dim) for point in test_points]
    t1 = time.time()
    t = max(round(t1 - t0, 5), 10e-5)
    return t, len(kink_points)


if __name__ == '__main__':
    test_all()
