import bisect
inf = float('inf')


class State2d(list):
    def __init__(self, lst):
        super().__init__(sorted(lst))

    def add(self, el):
        idx = bisect.bisect_left(self, el)

        if self.dominates(idx - 1, el) or self.dominates(idx, el):
            return False

        if idx == 0 or el[1] < self[idx - 1][1]:
            self.insert(idx, el)
            return idx

        idx0 = idx - 1
        while idx0 >= 0 and el[1] >= self[idx0][1]:
            idx0 -= 1
        self[idx - 1] = el

        del self[idx0 + 1:idx - 1]
        return idx0 + 1

    def remove_dominated(self, el):
        idx = bisect.bisect_left(self, el)

        if self.dominates(idx - 1, el) or self.dominates(idx, el):
            return []

        if idx == 0 or el[1] < self[idx - 1][1]:
            return []

        idx0 = idx - 1
        while idx0 >= 0 and el[1] >= self[idx0][1]:
            idx0 -= 1

        removed = self[idx0 + 1:idx]
        del self[idx0 + 1:idx]
        return removed

    def add_and_get_candidates(self, el):
        idx = self.add(el)
        candidates = []
        for i in range(2):
            candidates.append((self[idx + i - 1][0], self[idx + i][1], el[2]))
        return candidates

    def dominates(self, idx, el):
        if idx < 0 or idx >= len(self):
            return None
        if self[idx][0] >= el[0] and self[idx][1] >= el[1]:
            return True
        return False
