"""Utilities module"""

from typing import Tuple

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from srai.loaders.osm_loaders.filters import BASE_OSM_GROUPS_FILTER

PAPER_SIZES = {
    "A0": (1189, 841),  # (height, width) in mm
    "A1": (841, 594),  # (height, width) in mm
    "A2": (594, 420),  # (height, width) in mm
    "A3": (420, 297),  # (height, width) in mm
    "A4": (297, 210),  # (height, width) in mm
}


def plot_poster(
    gdf_and_features: Tuple[gpd.GeoDataFrame, dict],
    background_color="#ecedea",
    lon_lat_lims=None,
    figsize=(8.27, 11.69),
) -> Tuple[plt.Figure, plt.Axes]:
    """Plot a poster of the given GeoDataFrame.

    Parameters
    ----------
    gdf_and_features : Tuple[gpd.GeoDataFrame, dict]
        A tuple with the GeoDataFrame and a dictionary with the feature
        properties.
    background_color : str, optional
        The background color, by default "#ecedea". If None, no background is
        drawn.
    lon_lat_lims : Tuple[float, float, float, float], optional
        The lon/lat limits of the plot, by default None. If None, the total
        bounds of the GeoDataFrame are used.
    figsize : Tuple[float, float], optional
        The figure size, by default (8.27, 11.69)

    Returns
    -------
    Tuple[plt.Figure, plt.Axes]
        The figure and the axes of the plot.
    """
    gdf, feature_props = gdf_and_features

    fig, ax = create_figure(figsize)

    set_plot_position(ax)
    set_feature_props(gdf, feature_props, ax)

    if lon_lat_lims is None:
        lon_lat_lims = gdf.total_bounds
    set_axes_limits(lon_lat_lims, ax)
    set_axis_visibility(ax, False)
    draw_background(background_color, ax)

    return fig, ax


def create_figure(figsize):
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot()
    return fig, ax


def set_plot_position(ax):
    ax.set_position([0, 0, 1, 1])


def set_feature_props(gdf, feature_props, ax):
    if feature_props is None:
        feature_props = get_default_feature_props()

    for feature, props in feature_props.items():
        gdf.dropna(subset=[feature], how="all").plot(ax=ax, **props)


def set_axes_limits(lon_lat_lims, ax):
    lon_min, lat_min, lon_max, lat_max = lon_lat_lims
    ax.set_xlim(lon_min, lon_max)
    ax.set_ylim(lat_min, lat_max)


def set_axis_visibility(ax, show_axis):
    if not show_axis:
        ax.set_axis_off()


def draw_background(background_color, ax):
    if background_color is not None:
        ax.add_patch(
            plt.Rectangle(
                (0, 0),
                1,
                1,
                facecolor=background_color,
                transform=ax.transAxes,
                zorder=-1,
            )
        )


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


def get_default_background_color():
    return "#ecedea"


def zoom(lon_lat_lims, pin_center, zoom_level=1.0):
    """Zoom in on the given lat/lon range.

    Parameters
    ----------
    lon_lat_lims : Tuple[float, float, float, float]
        The lat/lon range: `(lon_min, lat_min, lon_max, lat_max)`
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

    # Unpack the lat/lon limits
    lon_min, lat_min, lon_max, lat_max = lon_lat_lims

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


def parse_pin_center(pin_center, lon_lat_lims):
    lon_min, lat_min, lon_max, lat_max = lon_lat_lims
    if pin_center is None:
        pin_center = [None, None]
    pin_center = list(pin_center)
    if pin_center[0] is None:
        pin_center[0] = (lon_min + lon_max) / 2
    if pin_center[1] is None:
        pin_center[1] = (lat_min + lat_max) / 2
    return pin_center
