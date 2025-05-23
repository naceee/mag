from point_sampling import get_non_dominated_points
from main import get_kink_points

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np



def test_algorithm():
    df = []
    for dim in range(3, 7):
        for i in range(1, 65):
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
    plt.grid(True)
    sns.scatterplot(data=df, x="n_points", y="n_kink_points", hue="dim", style="front_type")
    plt.xscale("log")
    plt.yscale("log")
    plt.show()

def find_exponent():
    for dim in range(3, 7):
        for front in ["random", "spherical", "linear"]:
            df = pd.read_csv("../csv/kink_points.csv")
            df = df[df["front_type"] == front]
            df = df[df["dim"] == dim]
            df = df.sort_values("n_points")
            x = df["n_points"].values
            y = df["n_kink_points"].values
            coeffs = np.polyfit(np.log(x), np.log(y), 1)
            print(f"{dim}D {front:9}: {round(coeffs[0], 3)}")


if __name__ == "__main__":
    # test_algorithm()
    plot_results()
    find_exponent()