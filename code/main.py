import math
from sortedcontainers import SortedList

from visualization import visualize_kink_points
from utils import weakly_dominates, state_dominates_point, strictly_dominates, get_dominated_points_bisect

inf = float('inf')

MAKE_EXPENSIVE_ASSERTS = True

def distance_to_pareto_front(pareto_front, query_point):
    dim = len(query_point)
    if not any([weakly_dominates(point, query_point) for point in pareto_front]):
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
    # print("POINTS:", list([round(float(x), 2) for x in point] for point in points))
    # print("SORTED:", list([round(float(x), 2) for x in point] for point in sorted_points))
    # print()
    for p1, p2 in zip(points, sorted_points):
        assert p1 == p2, f"points are not sorted correctly: {p1} != {p2};\n{points}\n{sorted_points}"


def assert_dimensionality(points, n_dim):
    for point in points:
        assert len(point) == n_dim, f"points must have {n_dim} dimensions; {point}"

def get_kink_points(points, n_dim):
    points = sorted(points, key=lambda x: x[n_dim - 1], reverse=True)
    return get_kink_points_rec(points, n_dim)


def get_kink_points_rec(points, d):
    if MAKE_EXPENSIVE_ASSERTS:
        assert_sorted(points, d)
        assert_dimensionality(points, d)

    if d == 3:
        return get_kink_points_rec_3d(points)

    points_state = SortedList([], key=lambda x: -x[-1])

    kp_cand = (0, ) * (d - 1)
    kink_candidates = SortedList([kp_cand])
    h = {kp_cand: math.inf}

    kink_points = []

    for point in points:
        removed = remove_dominated_nd(kink_candidates, point, "strict")
        for rem_point in removed:
            if strictly_dominates(point[:-1], rem_point) and h[rem_point] > point[-1]:
                kink_points.append(rem_point + (point[-1],))

        add_to_state(points_state, point[:-1], d)

        new_kink_points = get_kink_points_rec(points_state[:], d - 1)
        kink_candidates = SortedList(new_kink_points)
        for nkp in new_kink_points:
            if nkp not in h:
                h[nkp] = point[-1]


    for point in kink_candidates:
        kink_points.append(point + (0, ))

    return kink_points


def get_kink_points_rec_3d(points):

    points_state = SortedList([])
    kink_candidates = SortedList([(0, 0)])
    h = {(0, 0): math.inf}

    kink_points = []

    for point in points:
        # O(log(n) + #removed v)
        removed = remove_dominated_3d(kink_candidates, point[:-1], "strict")
        # O(#removed)
        for rem_point in removed:
            if strictly_dominates(point[:-1], rem_point) and h[rem_point] > point[-1]:
                kink_points.append(rem_point + (point[-1],))

        # O(log n + #removed p)
        add_to_state(points_state, point[:-1], 3)

        # O(log n)
        idx = points_state.index(point[:-1])
        p1 = (0 if idx == 0 else points_state[idx - 1][0], point[1])
        p2 = (point[0], 0 if idx == len(points_state) - 1 else points_state[idx + 1][1])

        # O(log n)
        for p in [p1, p2]:
            if p not in h:
                h[p] = point[-1]
                add_to_state(kink_candidates, p, 3)

    # O(n)
    for point in kink_candidates:
        kink_points.append(point + (0, ))

    return kink_points



def add_to_state(state, new_point, d):
    """ Adds new_point to state, while keeping the state a list of non-dominated points,
    sorted by the first dimension.
    If new_point is dominated by any point in state, it is not added.
    All the points dominated by the new_point are removed.
    """
    if d == 3:
        remove_dominated_3d(state, new_point, "weak")
    else:
        remove_dominated_nd(state, new_point, "weak")

    if not state_dominates_point(state, new_point):
        state.add(new_point)


def remove_dominated_nd(state, new_point, domination):
    """ Removes all the points in state that are dominated by new_point. """
    assert domination in ["strict", "weak"]

    removed = []
    for point in state:
        if (strictly_dominates(new_point, point) or
                (domination == "weak" and weakly_dominates(new_point, point))):
            removed.append(point)

    for point in removed:
        state.remove(point)

    return removed


def remove_dominated_3d(state, new_point, domination):
    """ Removes all the points in state that are dominated by new_point. """
    assert domination in ["strict", "weak"]
    left, right = get_dominated_points_bisect(state, new_point, domination)

    removed = state[left:right]
    del state[left:right]

    if MAKE_EXPENSIVE_ASSERTS:
        for el in removed:
            assert weakly_dominates(new_point, el), f"point doesn't dominate removed point: {new_point}, {el}"
            assert el not in state, f"removed point is still in state: {state}, {el}"

    return removed



def main():
    points = [(1.0, 0.9, 0.7), (0.4, 1.0, 0.5), (0.8, 1.0, 0.2), (0.6, 1.0, 0.4), (0.5, 0.9, 1.0), (1.0, 0.7, 1.0)]
    kp = get_kink_points(points, 3)
    visualize_kink_points(points, kp)


if __name__ == "__main__":
    main()
