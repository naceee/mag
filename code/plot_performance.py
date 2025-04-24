import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

def plot_time_archive_size():
    m = 1
    plt.figure(figsize=(5.5,4))
    cmap = mpl.colormaps["Paired"]
    formats = ["s-", "d-"]
    for i, dim in enumerate(range(3, 7)):
        for j, front in enumerate(["linear", "spherical"]):
            df = pd.read_csv(f"../performance_results/results_dim={dim}_front={front}_m={m}.csv")
            df = df.groupby("front_size")["time"].agg(["mean", "min", "max"]).reset_index()
            plt.plot(df["front_size"], df["mean"], formats[j],
                     label=f"{front} {dim}D", color=cmap(2 * i + j))

    plt.xscale("log")
    plt.yscale("log")
    plt.grid(True)
    plt.title("Hitrost algoritma")
    plt.xlabel("$n$")
    plt.ylabel("Čas [s]")
    plt.legend()
    plt.tight_layout()
    plt.savefig("../performance_plots/hitrost.pdf")
    plt.show()

def prepare_pgfp_plot():
    for dim in range(3, 7):
        for m in [1, 10, 100]:
            for front in ["linear", "spherical"]:
                df = pd.read_csv(f"../performance_results/results_dim={dim}_front={front}_m={m}.csv")
                df = df.groupby("front_size")["time"].agg(["mean"]).reset_index()
                df.to_csv(f"../csv/time_{front}_{dim}D_{m}.csv", index=False)


def plot_time_different_m():
    cmap = mpl.colormaps["Paired"]
    colors = [['#bdd7e7','#6baed6','#3182bd','#08519c'], ['#fcae91','#fb6a4a','#de2d26','#a50f15']]

    for i, dim in enumerate(range(3, 6)):
        plt.figure(figsize=(5.5, 4))

        for j, front in enumerate(["linear", "spherical"]):
            for k, m in enumerate([1, 10, 100]):
                df = pd.read_csv(f"../performance_results/results_dim={dim}_front={front}_m={m}.csv")
                df = df.groupby("front_size")["time"].agg(["mean", "min", "max"]).reset_index()

                plt.plot(df["front_size"], df["mean"],
                         label=f"{front} m={m}", color=colors[j][k])

        plt.xscale("log")
        plt.yscale("log")
        plt.grid(True)
        plt.title(f"Hitrost algoritma {dim}D")
        plt.xlabel("$n$")
        plt.ylabel("Čas [s]")
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"../performance_plots/hitrost_dim={dim}.pdf")
        plt.show()


if __name__ == '__main__':
    # plot_time_archive_size()
    # plot_time_different_m()
    prepare_pgfp_plot()
