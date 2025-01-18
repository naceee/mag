import math

from sortedcontainers import SortedList
from visualization import visualize_kink_points
from point_sampling import get_non_dominated_points

inf = float('inf')


def distance_to_pareto_front(pareto_front, query_point, kink_points=None):
    dim = len(query_point)
    if not any([weakly_dominates(point, query_point, dim) for point in pareto_front]):
        # query point is not dominated by the pareto front
        return 0

    if kink_points is None:
        kink_points = get_kink_points(pareto_front, dim)
    return dist_to_kink_points(kink_points, query_point, dim)


def dist_to_kink_points(kink_points, query_point, dim):
    min_sq_dist = inf
    for point in kink_points:
        sq_dist = sum([max(point[i] - query_point[i], 0) ** 2 for i in range(dim)])
        min_sq_dist = min(min_sq_dist, sq_dist)

    return math.sqrt(min_sq_dist)


def get_kink_points(points, n_dim):
    points = [point for point in points if all([p > 0 for p in point[:n_dim]])]
    points = sorted(points, key=lambda x: x[n_dim - 1], reverse=True)

    points_state, kink_candidates = get_initial_states(points, n_dim)
    kink_points = []

    for point in points:
        removed = remove_dominated(kink_candidates, point, n_dim - 1)
        for rem_point in removed:
            if strictly_dominates_except_last(point, rem_point, n_dim):
                kink_points.append(rem_point[:n_dim - 1] + (point[n_dim - 1],))

        add_to_state(points_state, point, n_dim - 1)
        if point in points_state:
            new_candidates = get_candidates(points_state, point, n_dim - 1)
            for new_candidate in new_candidates:
                add_to_state(kink_candidates, new_candidate + (point[n_dim - 1], ), n_dim - 1)

    for point in kink_candidates:
        kink_points.append(point[:n_dim - 1] + (0, ))

    return kink_points


def get_initial_states(points, n_dim):
    m = max([max([p for p in point]) for point in points])
    pseudo_inf = 10 ** math.floor(math.log10(max(m, 1)) + 1)
    points_state = SortedList([((0, ) * i + (pseudo_inf, ) + (0, ) * (n_dim - i - 1))
                               for i in range(n_dim)])
    kink_candidates = SortedList([(0, ) * (n_dim - 1) + (pseudo_inf, )])
    return points_state, kink_candidates


def get_candidates(state, new_point, n_dim):
    if n_dim == 2:
        idx = state.index(new_point)
        candidates = [
            (state[idx - 1][0], state[idx][1], new_point[2]),
            (state[idx][0], state[idx + 1][1], new_point[2])
        ]
        return candidates

    else:
        candidates = get_kink_points([p for p in state], n_dim)
        candidates = [c for c in candidates if any([c[i] == new_point[i] for i in range(n_dim)])]
        return candidates


def add_to_state(state, new_point, n_dim):
    # remove dominated points
    remove_dominated(state, new_point, n_dim)

    # TODO: make this more efficient
    for point in state:
        if weakly_dominates(point, new_point, n_dim):
            return -1

    state.add(new_point)


def remove_dominated(state, new_point, n_dim):
    removed = []
    for point in state:
        if weakly_dominates(new_point, point, n_dim):
            removed.append(point)
        elif new_point[0] < point[0]:
            break

    for point in removed:
        state.remove(point)

    return removed


def strictly_dominates_except_last(p1, p2, dim):
    return all([p1[i] > p2[i] for i in range(dim - 1)]) and p1[dim - 1] < p2[dim - 1]


def weakly_dominates(p1, p2, dim):
    return all([p1[i] >= p2[i] for i in range(dim)])


def state_dominates_point(state, point, n_dim):
    for p in state:
        if weakly_dominates(p, point, n_dim):
            return True
    return False


def main():
    # points = [(1, 2, 3), (2, 3, 1), (3, 1, 2)]
    # points = get_non_dominated_points(8, n_dim=3, mode="linear")
    points = [(1, 2, 3, 4, 5, 6), (6, 5, 4, 3, 2, 1)]

    p = get_kink_points(points, 6)
    print(p)

    # visualize_kink_points(points, get_kink_points(points, 3))
    # visualize_kink_points(points[:-1], get_kink_points(points[:-1]))


if __name__ == "__main__":
    main()
