import math
import numpy as np
import matplotlib.pyplot as plt

from point_sampling import epsilon_net, spherical_front
from tikz_3d_visualization import transform


def test_epsilon_net():
    for d in range(2, 11):
        h = 1
        r = 10
        net = epsilon_net(r, h, d)
        net = np.array(net)
        print(f"net calculated: {net.shape}")
        pts = spherical_front(r, 2000, d)


        # find the min distance for each of the points to the net
        min_dists = []
        for p in pts:
            dists = np.linalg.norm(net - p, axis=1)
            min_dists.append(np.min(dists))

        max_min_dist = max(min_dists)
        n_bins = 20
        bins = np.linspace(0, h, n_bins+1)
        print(bins)
        ticks = [f"{round(b1, 2)}-{round(b2, 2)}" for b1, b2 in zip(bins[:-1], bins[1:])]
        min_dist_hist = np.histogram(min_dists, bins=bins)
        plt.bar(range(n_bins), min_dist_hist[0])
        plt.xticks(range(n_bins), ticks, rotation=90)
        plt.title(f"h={h}, r={r}, d={d}, n={len(net)}, max min dist={round(max_min_dist, 4)}")
        plt.tight_layout()
        plt.show()
        print(f"Max min dist for {d}D ({len(net)} points): {max_min_dist:.6f}")

