from state import State

inf = float('inf')


def get_kink_points(points, ref_point):
    points = sorted(points, key=lambda x: x[2])

    points_state = State([(ref_point[0], -inf), (-inf, ref_point[1])])
    kink_candidates = State([ref_point])
    kink_points = []

    for point in points:
        # add the point to the kink state to get the dominated kink points, then take it out
        removed, _ = kink_candidates.add(point)
        for removed_point in removed:
            if point[0] < removed_point[0] and point[1] < removed_point[1] and removed_point[2] < point[2]:
                kink_points.append([removed_point[0], removed_point[1], point[2]])
        kink_candidates.remove(point)

        # add the point to the point state, and get two new kink point candidates
        _, idx = points_state.add(point[:2])
        for i in range(2):
            new_kink_candidate = (points_state[idx + i][0], points_state[idx - 1 + i][1], point[2])
            kink_candidates.add(new_kink_candidate)

    # add all the remaining kink points to the list
    for point in kink_candidates:
        kink_points.append((point[0], point[1], ref_point[2]))

    return kink_points


def main():
    points = [(1, 2, 3), (4, 3, 2), (0, 5, 1), (5, 4, 0)]
    ref_point = (6, 6, 6)

    kink_points = get_kink_points(points, ref_point)
    print(kink_points)


if __name__ == "__main__":
    main()
