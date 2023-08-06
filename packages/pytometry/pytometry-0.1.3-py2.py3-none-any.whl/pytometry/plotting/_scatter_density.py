from typing import List, Optional, Union

import datashader as ds
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scanpy as sc
from anndata import AnnData
from datashader.mpl_ext import dsshow
from matplotlib.axes import Axes
from matplotlib.colors import Colormap


def scatter_density(
    adata: AnnData,
    x: str = "FSC-A",
    y: str = "SSC-A",
    x_label: str = "FSC-A",
    y_label: str = "SSC-A",
    x_scale: str = "linear",
    y_scale: str = "linear",
    x_lim: List[float] = [-2 * 1e4, 3 * 1e5],
    y_lim: List[float] = [-2 * 1e4, 3 * 1e5],
    ax: Optional[Axes] = None,
    cmap: Union[str, List, Colormap] = "jet",
    vmin: Optional[float] = None,
    vmax: Optional[float] = None,
):
    """Plots the cell density across two adata.obs.

    Args:
        adata (AnnData): AnnData object containing data.
        x (str): adata.obs to plot on x axis.
            Defaults to 'FSC-A'
        y (str): adata.obs to plot on x axis.
            Defaults to 'SSC-A'.
        x_label (str): x axis label.
        y_label (str): y axis label.
        x_scale (str{"linear", "log", "symlog", "logit", ...}):
            x axis scale type to apply.
            Defaults to 'linear'.
        y_scale (str{"linear", "log", "symlog", "logit", ...}):
            y axis scale type to apply.
            Defaults to 'linear'.
        x_lim (list): upper and lower limit of the x axis.
        y_lim (list): upper and lower limit of the y axis.
        ax (`matplotlib.Axes`), optional:
            Axes to draw into. If *None*, create a new figure or use ``fignum`` to
            draw into an existing figure.
        cmap (str or list or :class:`matplotlib.cm.Colormap`), optional:
            For scalar aggregates, a matplotlib colormap name or instance.
            Alternatively, an iterable of colors can be passed and will be converted
            to a colormap. For a single-color, transparency-based colormap, see
            :func:`alpha_colormap`.
            Defaults to 'jet'.
        vmin, vmax (float), optional:
            For scalar aggregates, the data range that the colormap covers.
            If vmin or vmax is None (default), the colormap autoscales to the
            range of data in the area displayed, unless the corresponding value is
            already set in the norm.

    Returns:
        Scatter plot that displays cell density
    """
    fig, ax = plt.subplots()
    # Create df from anndata object
    markers = [x, y]
    joined = sc.get.obs_df(adata, keys=[*markers])

    # Convert variables to np.array
    x = np.array(joined[x])
    y = np.array(joined[y])

    # Plot density with datashader
    df = pd.DataFrame(dict(x=x, y=y))
    dsartist = dsshow(
        df,
        ds.Point("x", "y"),
        ds.count(),
        vmin=vmin,
        vmax=vmax,
        norm=None,
        # aspect="auto",
        ax=ax,
        cmap=cmap,
    )

    plt.colorbar(dsartist)

    plt.xlim(x_lim)
    plt.ylim(y_lim)
    plt.yscale(x_scale)
    plt.xscale(y_scale)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.show()
    return
