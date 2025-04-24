import math
import warnings

from sortedcontainers import SortedList
from visualization import visualize_kink_points
from point_sampling import get_non_dominated_points
from utils import weakly_dominates, strictly_dominates_except_last, state_dominates_point

inf = float('inf')


def distance_to_pareto_front(pareto_front, query_point):
    dim = len(query_point)
    if not any([weakly_dominates(point, query_point, dim) for point in pareto_front]):
        return 0

    kink_points = get_kink_points(pareto_front, dim)
    return dist_to_kink_points(kink_points, query_point, dim)


def dist_to_kink_points(kink_points, query_point, dim):
    min_sq_dist = inf
    for point in kink_points:
        sq_dist = sum([max(point[i] - query_point[i], 0) ** 2 for i in range(dim)])
        min_sq_dist = min(min_sq_dist, sq_dist)

    return math.sqrt(min_sq_dist)


def assert_sorted(points, n_dim):
    # assert that the points are sorted by the last coordinate
    sorted_points = sorted(points, key=lambda x: x[n_dim - 1], reverse=True)
    for p1, p2 in zip(points, sorted_points):
        assert p1 == p2, f"points are not sorted correctly: {p1} != {p2};\n{points}\n{sorted_points}"


def get_kink_points(points, n_dim):
    points = sorted(points, key=lambda x: x[n_dim - 1], reverse=True)
    return get_kink_points_rec(points, n_dim)


def get_kink_points_rec(points, n_dim):
    assert_sorted(points, n_dim)

    points_state = SortedList([])
    kink_candidates = SortedList([(0, ) * (n_dim - 1) + (math.inf, )])
    kink_points = []

    for point in points:
        removed = remove_dominated(kink_candidates, point, n_dim - 1)
        for rem_point in removed:
            if strictly_dominates_except_last(point, rem_point, n_dim):
                kink_points.append(rem_point[:n_dim - 1] + (point[n_dim - 1],))

        add_to_state(points_state, point, n_dim - 1)
        # if point in points_state:
        new_candidates = get_candidates(points_state, point, n_dim - 1)
        for new_candidate in new_candidates:
            add_to_state(kink_candidates, new_candidate + (point[n_dim - 1], ), n_dim - 1)

    for point in kink_candidates:
        kink_points.append(point[:n_dim - 1] + (0, ))

    return kink_points


def get_pseudo_inf(points, n_dim):
    max_el = max([max([p for p in point]) for point in points])
    return 10 ** math.floor(math.log10(max(max_el, 1)) + 1)


def get_candidates(state, new_point, n_dim):
    """ Returns kink point candidates after adding new_point to state.
    Works by recursively calling get_kink_points with a smaller dimension until it is 2. """
    if n_dim == 2:
        idx = state.index(new_point)
        return [(0 if idx == 0 else state[idx - 1][0], new_point[1], new_point[2]),
                (new_point[0], 0 if idx == len(state) - 1 else state[idx + 1][1], new_point[2])]

    else:
        candidates = get_kink_points(state[:], n_dim)
        candidates = [c for c in candidates if any([c[i] == new_point[i] for i in range(n_dim)])]
        return candidates


def add_to_state(state, new_point, n_dim):
    """ Adds new_point to state, while keeping the state a list of non-dominated points,
    sorted by the first dimension.
    If new_point is dominated by any point in state, it is not added.
    All the points dominated by the new_point are removed.
    """
    remove_dominated(state, new_point, n_dim)

    if not state_dominates_point(state, new_point, n_dim):
        state.add(new_point)


def remove_dominated(state, new_point, n_dim):
    """ Removes all the points in state that are dominated by new_point. """
    removed = []
    for point in state:
        if weakly_dominates(new_point, point, n_dim):
            removed.append(point)
        elif new_point[0] < point[0]:
            break

    for point in removed:
        state.remove(point)

    return removed





def main():
    points = [(1, 2, 3), (2, 3, 1), (3, 1, 2)]
    kp = get_kink_points(points, 3)
    visualize_kink_points(points, kp)


if __name__ == "__main__":
    main()
