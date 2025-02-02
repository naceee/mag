import unittest
import math
import numpy as np

from point_sampling import epsilon_net, random_sphere_points


class MyTestCase(unittest.TestCase):
    def test_epsilon_net(self):

        for d in range(2, 11):
            h = 0.2
            net = epsilon_net(h, d)
            net = np.array(net)

            pts = random_sphere_points(1, 10000, d)

            # find the min distance for each of the points to the net
            min_dists = []
            for p in pts:
                dists = np.linalg.norm(net - p, axis=1)
                min_dists.append(np.min(dists))

            max_min_dist = max(min_dists)
            self.assertLessEqual(max_min_dist, h / 2)
            print(f"Max min dist for {d}D ({len(net)} points): {max_min_dist:.6f}")


if __name__ == '__main__':
    unittest.main()
