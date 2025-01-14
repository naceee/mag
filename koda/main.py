from state2d import State2d
from statend import StateNd
from visualization import visualize_kink_points
from point_sampling import get_non_dominated_points

inf = float('inf')


def get_kink_points(points):
    points = sorted(points, key=lambda x: x[2], reverse=True)

    points_state = State2d([(0, inf), (inf, 0)])
    kink_candidates = State2d([(0, 0, inf)])
    kink_points = []

    for point in points:
        removed = kink_candidates.remove_dominated(point)
        for rem_point in removed:
            if point[0] > rem_point[0] and point[1] > rem_point[1] and point[2] < rem_point[2]:
                kink_points.append((rem_point[0], rem_point[1], point[2]))

        new_candidates = points_state.add_and_get_candidates(point)
        for new_candidate in new_candidates:
            kink_candidates.add(new_candidate)

    for point in kink_candidates:
        kink_points.append((point[0], point[1], 0))

    return kink_points


def main():
    # points = get_non_dominated_points(6, n_dim=3, mode="linear")
    points = [
        (1, 2, 3),
        (2, 3, 1),
        (3, 1, 2),
    ]

    kink_points = get_kink_points(points)
    visualize_kink_points(points, kink_points)


if __name__ == "__main__":
    main()
