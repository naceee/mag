import unittest
import numpy as np
from scipy.spatial import cKDTree

from point_sampling import epsilon_net, spherical_front, epsilon_net_from_square


class MyTestCase(unittest.TestCase):
    def test_epsilon_net(self):

        for d in range(2, 7):
            h = 0.1
            r = 5
            net = epsilon_net_from_square(r, h, d)
            print(f"Max min dist for {d}D ({len(net)} points):", end=" ")

            pts = spherical_front(r, 1000 * 2 ** d, d)
            # find the min distance for each of the points to the net
            tree = cKDTree(net)
            min_dists, _ = tree.query(pts, k=1)
            max_min_dist = np.max(min_dists)

            self.assertLessEqual(max_min_dist, h)

            print(f"{max_min_dist:.6f}")


if __name__ == '__main__':
    unittest.main()
