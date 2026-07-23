"""Generate one example PNG per vizlib chart type, plus a combined showcase.

Run from the repo root:

    python examples/generate.py

Outputs land in examples/ next to this script.
"""

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(OUT))  # repo root, so `import vizlib` works anywhere

import vizlib


def save(fig, name):
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, name), facecolor="white", dpi=110)
    plt.close(fig)


# --- sample data reused across charts -------------------------------------
two_series = {"2023": [42, 58, 31, 47], "2024": [55, 49, 38, 62]}
quarters = ["Q1", "Q2", "Q3", "Q4"]

corr_df = pd.DataFrame({
    "revenue":  np.arange(200) + (np.arange(200) * 37 % 20),
    "ad_spend": np.arange(200) * 0.8 + (np.arange(200) * 17 % 25),
    "visitors": np.arange(200) * 1.2 + (np.arange(200) * 53 % 40),
    "refunds":  200 - np.arange(200) + (np.arange(200) * 29 % 18),
    "churn":    np.arange(200) * 13 % 30,
}).corr()


# --- one PNG per chart type -----------------------------------------------
def line():
    ax = vizlib.line(two_series, x=quarters, title="line", ylabel="Revenue ($k)")
    save(ax.figure, "line.png")


def bar():
    ax = vizlib.bar(two_series, title="bar", ylabel="Revenue ($k)")
    ax.set_xticks(range(len(quarters)))
    ax.set_xticklabels(quarters)
    save(ax.figure, "bar.png")


def scatter():
    rng = np.arange(60)
    x = rng + (rng * 7 % 15)
    y = rng * 0.9 + (rng * 11 % 20)
    ax = vizlib.scatter(x, y, title="scatter", xlabel="x", ylabel="y")
    save(ax.figure, "scatter.png")


def hist():
    values = [(i * 37 % 50) for i in range(300)]
    ax = vizlib.hist({"samples": values}, bins=12, title="hist", xlabel="value")
    save(ax.figure, "hist.png")


def box():
    data = {
        "A": [i * 3 % 20 for i in range(40)],
        "B": [i * 5 % 25 + 5 for i in range(40)],
        "C": [i * 7 % 15 + 2 for i in range(40)],
    }
    ax = vizlib.box(data, title="box", ylabel="value")
    save(ax.figure, "box.png")


def pie():
    ax = vizlib.pie(
        {"Product A": 35, "Product B": 25, "Product C": 20, "Product D": 12, "Product E": 8},
        title="pie",
    )
    save(ax.figure, "pie.png")


def area():
    ax = vizlib.area(
        {"organic": [10, 14, 18, 22, 25], "paid": [5, 8, 7, 11, 14]},
        title="area", ylabel="Visitors (k)",
    )
    save(ax.figure, "area.png")


def heatmap():
    df = pd.DataFrame(
        [[1, 2, 3], [3, 4, 1], [2, 1, 4]],
        columns=["c1", "c2", "c3"], index=["r1", "r2", "r3"],
    )
    ax = vizlib.heatmap(df, title="heatmap", cmap="BuPu")
    save(ax.figure, "heatmap.png")


def correlation():
    ax = vizlib.heatmap(corr_df, title="correlation plot", cmap="RdBu_r")
    ax.images[0].set_clim(-1, 1)
    for i in range(len(corr_df)):
        for j in range(len(corr_df)):
            v = corr_df.values[i, j]
            ax.text(j, i, f"{v:.2f}", ha="center", va="center",
                    color="white" if abs(v) > 0.5 else "#0b0b0b", fontsize=9)
    save(ax.figure, "correlation.png")


def showcase():
    fig, axes = plt.subplots(2, 4, figsize=(20, 8))
    vizlib.line({"a": [1, 3, 2, 5], "b": [2, 2, 3, 3]}, ax=axes[0, 0], title="line")
    vizlib.bar({"a": [1, 3, 2], "b": [2, 1, 4]}, ax=axes[0, 1], title="bar")
    vizlib.scatter([1, 2, 3, 4, 2, 3], [3, 1, 4, 2, 3, 1], ax=axes[0, 2], title="scatter")
    vizlib.hist({"a": [1, 2, 2, 3, 3, 3, 4, 4, 5]}, bins=5, ax=axes[0, 3], title="hist")
    vizlib.box({"a": [1, 2, 3, 4, 5], "b": [2, 3, 3, 5, 6], "c": [1, 1, 2, 3, 3]}, ax=axes[1, 0], title="box")
    vizlib.pie({"x": 10, "y": 20, "z": 15, "w": 8}, ax=axes[1, 1], title="pie")
    vizlib.area({"a": [1, 2, 3, 2], "b": [2, 2, 1, 3]}, ax=axes[1, 2], title="area")
    df = pd.DataFrame([[1, 2, 3], [3, 4, 1], [2, 1, 4]],
                      columns=["c1", "c2", "c3"], index=["r1", "r2", "r3"])
    vizlib.heatmap(df, ax=axes[1, 3], title="heatmap", cmap="BuPu")
    fig.suptitle("vizlib — all 8 chart types", fontsize=15, fontweight="bold", x=0.01, ha="left")
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    fig.savefig(os.path.join(OUT, "showcase.png"), facecolor="white", dpi=110)
    plt.close(fig)


if __name__ == "__main__":
    for chart in (line, bar, scatter, hist, box, pie, area, heatmap, correlation, showcase):
        chart()
        print(f"generated {chart.__name__}.png")
