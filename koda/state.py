import bisect
inf = float('inf')


class State(list):
    def __init__(self, lst):
        super().__init__(sorted(lst))

    def add(self, el):
        idx = bisect.bisect_left(self, el)

        if self.dominates(idx - 1, el) or self.dominates(idx, el):
            print(self, el)
            # raise ValueError("Element is dominated by the state")

        if idx == len(self) or el[1] > self[idx][1]:
            self.insert(idx, el)
            return idx

        idx2 = idx + 1
        while idx2 < len(self) and el[1] >= self[idx2][1]:
            idx2 += 1
        self[idx] = el

        del self[idx + 1:idx2]
        return idx

    def remove_dominated(self, el):
        idx = bisect.bisect_left(self, el)

        if self.dominates(idx - 1, el) or self.dominates(idx, el):
            print(self, el)
            # raise ValueError("Element is dominated by the state")

        if idx == len(self) or el[1] > self[idx][1]:
            return []

        idx2 = idx + 1
        while idx2 < len(self) and el[1] >= self[idx2][1]:
            idx2 += 1

        removed = self[idx:idx2]
        del self[idx:idx2]
        return removed

    def dominates(self, idx, f_pair):
        if idx < 0 or idx >= len(self):
            return None
        if self[idx][0] >= f_pair[0] and self[idx][1] >= f_pair[1]:
            return True
        return False
