from point_sampling import get_non_dominated_points
from main import get_kink_points

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def test_algorithm():
    df = []
    for dim in range(3, 7):
        for i in range(1, 51):
            for front_type in ["random", "linear", "spherical"]:
                non_dominated_points = get_non_dominated_points(i, dim, mode=front_type)
                n_points = len(non_dominated_points)
                kink_points = get_kink_points(non_dominated_points, dim)
                n_kink_points = len(kink_points)
                df.append([dim, front_type, n_points, n_kink_points])
                print([dim, front_type, n_points, n_kink_points])
    df = pd.DataFrame(df, columns=["dim", "front_type", "n_points", "n_kink_points"])
    df.to_csv("../csv/kink_points.csv", index=False)

def plot_results():
    df = pd.read_csv("../csv/kink_points.csv")
    sns.scatterplot(data=df, x="n_points", y="n_kink_points", hue="dim", style="front_type")
    plt.show()

if __name__ == "__main__":
    test_algorithm()
    plot_results()
