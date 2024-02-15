"""Utilities module"""

import warnings

import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt

from typing import Tuple
from srai.loaders.osm_loaders.filters import BASE_OSM_GROUPS_FILTER

PAPER_SIZES = {
    "A0": (1189, 841),  # (height, width) in mm
    "A1": (841, 594),   # (height, width) in mm
    "A2": (594, 420),   # (height, width) in mm
    "A3": (420, 297),   # (height, width) in mm
    "A4": (297, 210),   # (height, width) in mm
}


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
                lon_lim=None,
                lat_lim=None,
                figsize=(8.27, 11.69),
                show_axis=False) -> plt.axes:
    """Plot a poster of the given GeoDataFrame.

    Parameters
    ----------
    gdf : gpd.GeoDataFrame
        The GeoDataFrame to plot.
    feature_props : dict, optional
        The properties of the features to plot, by default None. If None, the
        default properties are used. See `get_default_feature_props` for the
        default properties.
    background_color : str, optional
        The background color, by default "#ecedea"
    lat_lim : Tuple[float, float], optional
        Latitude limits (min, max), by default None
    lon_lim : Tuple[float, float], optional
        Longitude limits (min, max), by default None
    figsize : Tuple[float, float], optional
        The figure size, by default (8.27, 11.69)
    show_axis : bool, optional
        Whether to show the axis, by default False

    Returns
    -------
    plt.axes
        The axes of the plot.
    """
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot()
    ax.set_position([0, 0, 1, 1])

    if feature_props is None:
        feature_props = get_default_feature_props()

    for feature, props in feature_props.items():
        gdf.dropna(subset=[feature], how="all").plot(
            ax=ax,
            **props
        )

    # Set axes limits
    lon_min, lat_min, lon_max, lat_max = gdf.total_bounds
    if lat_lim is not None:
        ax.set_xlim(*lon_lim)
    else:
        ax.set_xlim(lon_min, lon_max)
    if lon_lim is not None:
        ax.set_ylim(*lat_lim)
    else:
        ax.set_ylim(lat_min, lat_max)

    if not show_axis:
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

    return fig, ax


def get_default_feature_props():
    return {
        "water": {"color": "#a8e1e6"},
        "waterway": {"color": "#a8e1e6"},
        "highway": {
            "color": "#181818",
            "linewidth": 0.5,
            "markersize": 0.5,
        },
    }


def get_possible_feature_names():
    possible_features = []
    for key in BASE_OSM_GROUPS_FILTER.keys():
        possible_features.append(key)
        for child_key in BASE_OSM_GROUPS_FILTER[key].keys():
            possible_features.append(child_key)
            try:
                for item in BASE_OSM_GROUPS_FILTER[key][child_key]:
                    possible_features.append(item)
            except TypeError:
                pass
    return possible_features


def zoom(lon_min, lat_min, lon_max, lat_max, pin_center, zoom_level=1.0):
    """Zoom in on the given lat/lon range.

    Parameters
    ----------
    lat_min : float
        The minimum latitude.
    lat_max : float
        The maximum latitude.
    lon_min : float
        The minimum longitude.
    lon_max : float
        The maximum longitude.
    pin_center : Tuple[float, float]
        The center of the pin.
    zoom_level : float or Tuple[float, float], optional
        The zoom level, by default 1.0. It can be a float or a tuple with two
        floats, the first for the longitude axis and the second for the
        latitude axis.

    Returns
    -------
    Tuple[float, float, float, float]
        The new lat/lon range: `(lon_min, lat_min, lon_max, lat_max)`
    """
    # If zoom_level is not a tuple or a list, turn it into a tuple
    try:
        zoom_level = (zoom_level[0], zoom_level[1])
    except TypeError or IndexError:
        zoom_level = (zoom_level, zoom_level)

    # Zoom in on longitude axis
    lon_center = pin_center[0]
    lon_diff = np.abs(lon_max - lon_min)
    lon_min = lon_center - (lon_diff / 2) / zoom_level[0]
    lon_max = lon_center + (lon_diff / 2) / zoom_level[0]

    # Zoom in on latitude axis
    lat_center = pin_center[1]
    lat_diff = np.abs(lat_max - lat_min)
    lat_min = lat_center - (lat_diff / 2) / zoom_level[1]
    lat_max = lat_center + (lat_diff / 2) / zoom_level[1]

    return lon_min, lat_min, lon_max, lat_max


def parse_pin_center(pin_center, lon_min, lat_min, lon_max, lat_max):
    if pin_center is None:
        pin_center = [None, None]
    pin_center = list(pin_center)
    if pin_center[0] is None:
        pin_center[0] = (lon_min + lon_max) / 2
    if pin_center[1] is None:
        pin_center[1] = (lat_min + lat_max) / 2
    return pin_center


def fit_to_paper(lon_min,
                 lat_min,
                 lon_max,
                 lat_max,
                 paper_size,
                 orientation="portrait"):
    """Fit the given lat/lon range to the given paper size.

    Parameters
    ----------
    lon_min : float
        The minimum longitude.
    lat_min : float
        The minimum latitude.
    lon_max : float
        The maximum longitude.
    lat_max : float
        The maximum latitude.
    paper_size : str
        The paper size. It has to be one of the keys in `PAPER_SIZES`
    orientation : str, optional
        The paper orientation, by default "portrait". Can also be "landscape".

    Returns
    -------
    Tuple[float, float, float, float]
        The new lat/lon range: `(lon_min, lat_min, lon_max, lat_max)`
    """
    # Get paper dimensions
    paper_size = paper_size.upper()
    paper_dimensions = PAPER_SIZES[paper_size]

    # Get lat/lon range dimensions
    lon_diff = np.abs(lon_max - lon_min)
    lat_diff = np.abs(lat_max - lat_min)

    # Get lat/lon range aspect ratio
    lon_lat_ratio = lon_diff / lat_diff

    # Get paper aspect ratio
    paper_ratio = paper_dimensions[1] / paper_dimensions[0]

    if orientation == "landscape":
        paper_ratio = 1 / paper_ratio
    elif orientation == "portrait":
        pass
    else:
        warnings.warn(f"Orientation {orientation} not recognized. Using " +
                      "portrait orientation.")

    # Adjust lat/lon range to paper aspect ratio
    if lon_lat_ratio > paper_ratio:
        lon_diff = lat_diff * paper_ratio
    else:
        lat_diff = lon_diff / paper_ratio

    # Get new lat/lon range
    lon_center = (lon_min + lon_max) / 2
    lat_center = (lat_min + lat_max) / 2
    lon_min = lon_center - lon_diff / 2
    lon_max = lon_center + lon_diff / 2
    lat_min = lat_center - lat_diff / 2
    lat_max = lat_center + lat_diff / 2

    return lon_min, lat_min, lon_max, lat_max
