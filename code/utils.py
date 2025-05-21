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

def get_dominated_points_bisect(sorted_list, point, domination):
    right = bisect_x(sorted_list, point[0], domination)
    left = bisect_y(sorted_list, point[1], domination)
    return left, right

def get_compare_fun(domination):
    if domination == "strict":
        return lambda x, y: x < y
    else:
        return lambda x, y: x <= y

def bisect_x(lst, el, domination):
    f_compare = get_compare_fun(domination)

    i, j = 0, len(lst)
    while i < j:
        mid = (i + j) // 2
        if f_compare(lst[mid][0], el):
            i = mid + 1
        else:
            j = mid
    return i

def bisect_y(lst, el, domination="strict"):
    f_compare = get_compare_fun(domination)

    i, j = 0, len(lst)
    while i < j:
        mid = (i + j) // 2
        if f_compare(lst[mid][1], el):
            j = mid
        else:
            i = mid + 1
    return i
