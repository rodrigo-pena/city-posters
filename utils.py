"""Utilities module"""

import geopandas as gpd
import matplotlib.pyplot as plt

from typing import Tuple


def dd2dms(deg):
    d = int(deg)
    md = abs(deg - d) * 60
    m = int(md)
    sd = (md - m) * 60
    return [d, m, sd]


def plot_rectangle_with_text(
    ax: plt.Axes,
    coords: Tuple[float, float],
    title: str,
    subtitle: str = "",
):
    width = 1.0
    height = 0.085
    fontsize_title = 45
    fontsize_subtitle = 15

    rectangle = plt.Rectangle(
        coords,
        width,
        height,
        facecolor="#ecedea",
        alpha=0.8,
        transform=ax.transAxes,
        zorder=2,
    )

    ax.add_patch(rectangle)
    rx, ry = rectangle.get_xy()
    cx = rx + rectangle.get_width() / 2.0
    cy = ry + rectangle.get_height() / 2.0

    ax.text(
        cx,
        cy,
        title,
        fontsize=fontsize_title,
        transform=ax.transAxes,
        horizontalalignment="center",
        verticalalignment="center",
        color="#2b2b2b",
    )

    ax.text(
        cx,
        cy - 0.032,
        subtitle,
        fontsize=fontsize_subtitle,
        transform=ax.transAxes,
        horizontalalignment="center",
        verticalalignment="center",
        color="#2b2b2b",
    )


def plot_poster(gdf: gpd.GeoDataFrame,
                feature_props=None,
                background_color="#ecedea",
                xlim=None,
                ylim=None,
                figsize=(8.27, 11.69)) -> plt.axes:
    """Plot a poster of the given GeoDataFrame.

    Parameters
    ----------
    gdf : gpd.GeoDataFrame
        The GeoDataFrame to plot.
    feature_props : dict, optional
        The properties of the features to plot, by default None. If None, the following properties are used:
        {
            "water": {"color": "#a8e1e6"},
            "waterway": {"color": "#a8e1e6"},
            "highway": {"color": "#181818"},
        }
        Each key is a feature name and each value is a dictionary with key-value argument pairs to pass to the gpd.GeoDataFrame.plot method.
    background_color : str, optional
        The background color, by default "#ecedea"
    xlim : Tuple[float, float], optional
        The x-axis limits, by default None
    ylim : Tuple[float, float], optional
        The y-axis limits, by default None
    figsize : Tuple[float, float], optional
        The figure size, by default (8.27, 11.69)

    Returns
    -------
    plt.axes
        The axes of the plot.
    """
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot()
    ax.set_position([0, 0, 1, 1])

    if feature_props is None:
        feature_props = {
            "water": {"color": "#a8e1e6"},
            "waterway": {"color": "#a8e1e6"},
            "highway": {"color": "#181818"},
        }

    for feature, props in feature_props.items():
        gdf.dropna(subset=[feature], how="all").plot(
            ax=ax,
            **props
        )

    # Set axes limits
    xmin, ymin, xmax, ymax = gdf.total_bounds
    if xlim is not None:
        ax.set_xlim(*xlim)
    else:
        ax.set_xlim(xmin, xmax)
    if ylim is not None:
        ax.set_ylim(*ylim)
    else:
        ax.set_ylim(ymin, ymax)

    ax.set_axis_off()

    # Draw background rectangle
    ax.add_patch(
        plt.Rectangle(
            (0, 0),
            1,
            1,
            facecolor=background_color,
            transform=ax.transAxes,
            zorder=-1
        )
    )

    ax.margins(0, 0)

    return ax
