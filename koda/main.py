from state import State
from visualization import visualize_kink_points
from point_sampling import get_non_dominated_points

inf = float('inf')


def get_kink_points(points):
    points = sorted(points, key=lambda x: x[2])

    points_state = State([(0, inf), (inf, 0)])
    kink_candidates = State([(0, 0, 0)])
    kink_points = []

    for point in points:
        removed = kink_candidates.remove_dominated(point)
        for removed_point in removed:
            if point[0] > removed_point[0] and point[1] > removed_point[1] and removed_point[2] > point[2]:
                kink_points.append((removed_point[0], removed_point[1], point[2]))

        idx = points_state.add(point[:2])
        for i in range(2):
            new_kink_candidate = (points_state[idx + i][0], points_state[idx - 1 + i][1], point[2])
            kink_candidates.add(new_kink_candidate)

    # add all the remaining kink points to the list
    for point in kink_candidates:
        kink_points.append((point[0], point[1], 0))

    return kink_points


def main():
    # points = get_non_dominated_points(6, n_dim=3, mode="linear")
    points = [
        (0.1, 0.2, 0.3),
        (0.2, 0.3, 0.1),
        (0.3, 0.1, 0.2)
    ]

    kink_points = get_kink_points(points)
    visualize_kink_points(points, kink_points)


if __name__ == "__main__":
    main()
