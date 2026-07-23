# vizlib

A tiny matplotlib wrapper with a **pandas-style plotting API**. Short function
names, sensible defaults, and one consistent light pastel palette across every
chart type — so you can go from data to a good-looking chart in a single call.

```python
import vizlib
vizlib.line({"a": [1, 3, 2, 5], "b": [2, 2, 3, 3]}, title="Trend")
```

## Install

```bash
pip install -e .
```

Requires Python ≥ 3.9, `matplotlib` ≥ 3.9, and `numpy`.

## Chart types

Eight short-named functions. Each accepts a `dict`, a plain `list`/array, or a
pandas `Series`/`DataFrame`, and returns the matplotlib `Axes` it drew on (so
you can keep customizing after the call).

| Function | Draws | Example |
|----------|-------|---------|
| `line`    | Line chart (one line per series)        | `vizlib.line({"a": [1, 2, 3]})` |
| `bar`     | Grouped bar chart (`horizontal=True` for bars) | `vizlib.bar({"a": [1, 3, 2], "b": [2, 1, 4]})` |
| `scatter` | Scatter plot                            | `vizlib.scatter([1, 2, 3], [3, 1, 4])` |
| `hist`    | Histogram                               | `vizlib.hist({"a": [1, 2, 2, 3, 3, 4]}, bins=5)` |
| `box`     | Box plot (one box per series)           | `vizlib.box({"a": [...], "b": [...]})` |
| `pie`     | Pie chart                               | `vizlib.pie({"x": 10, "y": 20, "z": 15})` |
| `area`    | Area chart (`stacked=True` by default)  | `vizlib.area({"a": [1, 2, 3], "b": [2, 2, 1]})` |
| `heatmap` | Matrix heatmap (great for correlations) | `vizlib.heatmap(df.corr(), cmap="RdBu_r")` |

## Accepted input

All functions normalize their input the same way:

- **dict** — `{"label": [values], ...}`; keys become series names / legend labels.
- **pandas DataFrame** — each column is a series; the index becomes the x-axis.
- **pandas Series** — a single labeled series.
- **list / numpy array** — a single unlabeled series (x is `0..n-1`).

## Common keywords

Most functions take `ax`, `title`, `xlabel`, and `ylabel`:

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
vizlib.bar({"2023": [42, 58, 31], "2024": [55, 49, 38]},
           ax=ax, title="Revenue", ylabel="$k")
plt.show()
```

Extras: `bar(..., horizontal=True)`, `hist(..., bins=N)`,
`scatter(..., size=N)`, `area(..., stacked=False)`, `heatmap(..., cmap=...)`.

## Correlation plot

Because `heatmap` accepts a DataFrame, a correlation plot is one line on top of
pandas — use a diverging colormap centered at 0:

```python
ax = vizlib.heatmap(df.corr(), title="correlation plot", cmap="RdBu_r")
ax.images[0].set_clim(-1, 1)
```

## Theming

The palette lives in `vizlib.COLORS` (a list of hex strings). Override it before
plotting to recolor everything:

```python
vizlib.COLORS = ["#2a78d6", "#e87ba4"]   # e.g. blue + pink
vizlib.bar({"a": [1, 3, 2], "b": [2, 1, 4]})
```

The default is a light pastel set — soft blue, coral, teal, amber, lavender,
pink, green, and indigo.

## Examples

Rendered examples live in [`examples/`](examples/) — one PNG per chart type
plus a combined showcase. Regenerate them all with:

```bash
python examples/generate.py
```

| File | Chart |
|------|-------|
| `examples/showcase.png` | All 8 chart types in one grid |
| `examples/line.png` | `line` |
| `examples/bar.png` | `bar` |
| `examples/scatter.png` | `scatter` |
| `examples/hist.png` | `hist` |
| `examples/box.png` | `box` |
| `examples/pie.png` | `pie` |
| `examples/area.png` | `area` |
| `examples/heatmap.png` | `heatmap` |
| `examples/correlation.png` | `heatmap` used as a correlation matrix |
