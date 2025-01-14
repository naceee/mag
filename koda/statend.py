inf = float('inf')


class StateNd(list):
    def __init__(self, lst, dim=None):
        super().__init__(sorted(lst))
        self.dim = len(lst[0]) if dim is None else dim

    def add(self, el):
        """ Adds el to self (if it is not dominated by any other element in self)
        and removes dominated elements from self."""

        self.remove_dominated(el)
        for point in self:
            if self.dominates(point, el):
                return None

        self.append(el)

    def remove_dominated(self, el):
        """ Removes all elements from self that are dominated by el. """
        removed = []
        for point in self:
            if self.dominates(el, point):
                removed.append(point)

        for point in removed:
            self.remove(point)

        return removed

    def dominates(self, el1, el2):
        """ Returns True if el1 dominates el2, False otherwise. """
        return all([el1[i] >= el2[i] for i in range(self.dim)])
