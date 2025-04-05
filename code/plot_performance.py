import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def plot_time_archive_size():
    front = "linear"
    m = 1
    plt.figure(figsize=(8,6))
    dfs = []
    for dim in range(3, 11):
        df = pd.read_csv(f"../performance_results/results_dim={dim}_front={front}_m={m}.csv")
        df["dim"] = dim
        dfs.append(df)
    dfs = pd.concat(dfs)
    sns.lineplot(data=dfs, x="front_size", y="time", hue="dim", style="dim", markers=True, dashes=False,
                 palette="colorblind")
    plt.xscale("log")
    plt.yscale("log")
    plt.grid(True)
    plt.xlabel("Size of set P")
    plt.ylabel("Time [s]")
    plt.show()


def plot_time_output_size():
    front = "linear"
    m = 1
    plt.figure(figsize=(8,6))
    dfs = []
    for dim in range(3, 11):
        df = pd.read_csv(f"../performance_results/results_dim={dim}_front={front}_m={m}.csv")
        df["dim"] = dim
        dfs.append(df)
    dfs = pd.concat(dfs)
    sns.lineplot(data=dfs, x="front_size", y="n_kink_points", hue="dim", style="dim", markers=True, palette="colorblind")
    plt.xscale("log")
    plt.yscale("log")
    plt.grid(True)
    plt.xlabel("Size of set P")
    plt.ylabel("Time [s]")
    plt.show()



if __name__ == '__main__':
    plot_time_output_size()
