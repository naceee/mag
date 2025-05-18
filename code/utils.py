def strictly_dominates_except_last(p1, p2, dim):
    """ Returns True if p1 strictly dominates p2 in first dim - 1 dimensions while having
    a smaller last dimension.
    Used for edge cases in the kink point calculation. """
    return all([p1[i] > p2[i] for i in range(dim - 1)]) and p1[dim - 1] < p2[dim - 1]


def weakly_dominates(point1, point2):
    """ Returns True if p1 weakly dominates p2. """
    return all([p1 >= p2 for p1, p2 in zip(point1, point2)])

def strictly_dominates(point1, point2):
    """ Returns True if p1 strictly dominates p2. """
    return all([p1 > p2 for p1, p2 in zip(point1, point2)])


def state_dominates_point(state, point):
    """ Returns True if any point in state dominates point. """
    for state_point in state:
        if weakly_dominates(state_point, point):
            return True
    return False