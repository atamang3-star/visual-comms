"""vizlib: a tiny matplotlib wrapper with a pandas-style plotting API.

Each chart function takes a dict, pandas Series/DataFrame, or plain
sequence and returns the Axes it drew on, e.g.:

    vizlib.line({"a": [1, 2, 3], "b": [3, 2, 1]}, title="Trend")
    vizlib.bar({"x": [1, 2, 3]})
"""

import numpy as np
import matplotlib.pyplot as plt

COLORS = ["#7fbce8", "#ffab91", "#80cbc4", "#ffcc80",
          "#ce93d8", "#f48fb1", "#c5e1a5", "#9fa8da"]
INK = "#0b0b0b"
MUTED = "#898781"
GRID = "#e1e0d9"
SURFACE = "#fcfcfb"


def _ax(ax):
    if ax is None:
        fig, ax = plt.subplots(figsize=(7, 4))
        return ax
    return ax


def _style(ax, title=None, xlabel=None, ylabel=None, legend=False):
    ax.set_facecolor(SURFACE)
    ax.grid(True, color=GRID, linewidth=0.8, axis="y")
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(MUTED)
    ax.spines["bottom"].set_color(MUTED)
    ax.tick_params(colors=MUTED, labelcolor=INK)
    if title:
        ax.set_title(title, color=INK, fontsize=12, fontweight="bold", loc="left")
    if xlabel:
        ax.set_xlabel(xlabel, color=MUTED)
    if ylabel:
        ax.set_ylabel(ylabel, color=MUTED)
    if legend:
        ax.legend(frameon=False, labelcolor=INK)
    return ax


def _series(data):
    """Normalize dict / DataFrame / Series / list input to (x, {label: values})."""
    if hasattr(data, "columns"):  # DataFrame
        x = np.asarray(data.index)
        return x, {col: np.asarray(data[col]) for col in data.columns}
    if hasattr(data, "items"):  # dict or Series
        series = {label: np.asarray(values) for label, values in data.items()}
        length = len(next(iter(series.values())))
        return np.arange(length), series
    values = np.asarray(data)
    return np.arange(len(values)), {"": values}


def line(data, x=None, ax=None, title=None, xlabel=None, ylabel=None):
    ax = _ax(ax)
    xi, series = _series(data)
    xi = np.asarray(x) if x is not None else xi
    for i, (label, y) in enumerate(series.items()):
        ax.plot(xi, y, color=COLORS[i % len(COLORS)], linewidth=2,
                 solid_capstyle="round", label=label or None)
    return _style(ax, title, xlabel, ylabel, legend=len(series) > 1)


def bar(data, ax=None, title=None, xlabel=None, ylabel=None, horizontal=False):
    ax = _ax(ax)
    xi, series = _series(data)
    n = len(series)
    width = 0.8 / n
    for i, (label, y) in enumerate(series.items()):
        pos = xi + (i - (n - 1) / 2) * width
        if horizontal:
            ax.barh(pos, y, height=width * 0.9, color=COLORS[i % len(COLORS)], label=label or None)
        else:
            ax.bar(pos, y, width=width * 0.9, color=COLORS[i % len(COLORS)], label=label or None)
    return _style(ax, title, xlabel, ylabel, legend=n > 1)


def scatter(x, y, ax=None, title=None, xlabel=None, ylabel=None, size=40):
    ax = _ax(ax)
    ax.scatter(x, y, s=size, color=COLORS[0], edgecolor=SURFACE, linewidth=0.5, alpha=0.9)
    return _style(ax, title, xlabel, ylabel)


def hist(data, bins=10, ax=None, title=None, xlabel=None, ylabel=None):
    ax = _ax(ax)
    _, series = _series(data)
    alpha = 0.85 if len(series) > 1 else 1
    for i, (label, y) in enumerate(series.items()):
        ax.hist(y, bins=bins, color=COLORS[i % len(COLORS)], alpha=alpha, label=label or None)
    return _style(ax, title, xlabel, ylabel or "Count", legend=len(series) > 1)


def box(data, ax=None, title=None, ylabel=None):
    ax = _ax(ax)
    _, series = _series(data)
    labels = [label or str(i) for i, label in enumerate(series.keys())]
    bp = ax.boxplot(list(series.values()), tick_labels=labels, patch_artist=True,
                     medianprops={"color": INK})
    for patch, color in zip(bp["boxes"], COLORS):
        patch.set_facecolor(color)
        patch.set_alpha(0.85)
    return _style(ax, title, None, ylabel)


def pie(data, ax=None, title=None):
    ax = _ax(ax)
    if hasattr(data, "items"):
        labels, values = list(data.keys()), list(data.values())
    else:
        labels, values = None, list(data)
    colors = [COLORS[i % len(COLORS)] for i in range(len(values))]
    ax.pie(values, labels=labels, colors=colors,
           wedgeprops={"linewidth": 2, "edgecolor": SURFACE},
           textprops={"color": INK})
    ax.set_aspect("equal")
    if title:
        ax.set_title(title, color=INK, fontsize=12, fontweight="bold", loc="left")
    return ax


def area(data, x=None, ax=None, title=None, xlabel=None, ylabel=None, stacked=True):
    ax = _ax(ax)
    xi, series = _series(data)
    xi = np.asarray(x) if x is not None else xi
    labels, values = list(series.keys()), list(series.values())
    colors = [COLORS[i % len(COLORS)] for i in range(len(values))]
    if stacked and len(values) > 1:
        ax.stackplot(xi, *values, labels=labels, colors=colors, alpha=0.85)
    else:
        for i, (label, y) in enumerate(series.items()):
            ax.fill_between(xi, y, color=COLORS[i % len(COLORS)], alpha=0.35)
            ax.plot(xi, y, color=COLORS[i % len(COLORS)], linewidth=2, label=label or None)
    return _style(ax, title, xlabel, ylabel, legend=len(values) > 1)


def heatmap(data, ax=None, title=None, cmap="Blues"):
    ax = _ax(ax)
    if hasattr(data, "values"):  # DataFrame
        matrix, rows, cols = data.values, list(data.index), list(data.columns)
    else:
        matrix, rows, cols = np.asarray(data), None, None
    im = ax.imshow(matrix, cmap=cmap, aspect="auto")
    if cols is not None:
        ax.set_xticks(range(len(cols)))
        ax.set_xticklabels(cols, color=INK, rotation=45, ha="right")
    if rows is not None:
        ax.set_yticks(range(len(rows)))
        ax.set_yticklabels(rows, color=INK)
    ax.figure.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    for spine in ax.spines.values():
        spine.set_visible(False)
    if title:
        ax.set_title(title, color=INK, fontsize=12, fontweight="bold", loc="left")
    return ax
