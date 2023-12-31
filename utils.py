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
                city: str,
                country: str,
                with_text=True) -> plt.axes:
    centroid = gdf.dissolve().centroid.item()
    lat = dd2dms(centroid.y)
    lng = dd2dms(centroid.x)

    fig = plt.figure(figsize=(8.27, 11.69))
    ax = fig.add_subplot()
    ax.set_position([0, 0, 1, 1])

    gdf.dropna(subset=["water", "waterway"], how="all").plot(
        ax=ax,
        color="#a8e1e6"
    )

    gdf.dropna(subset=["highway"], how="all").plot(
        ax=ax,
        color="#181818",
        markersize=0.1
    )

    # Format coordinates string
    ns = "N" if centroid.y >= 0 else "S"
    ew = "E" if centroid.x >= 0 else "W"
    coord_str = f"{abs(lat[0])}°{lat[1]}' {ns}, {abs(lng[0])}°{lng[1]}' {ew}"

    if with_text:
        # Draw city coordinates
        plot_rectangle_with_text(
            ax,
            (0, 0.90),
            coord_str,
        )

        # Draw city name
        plot_rectangle_with_text(ax, (0, 0.15), city, country)

    # Set axes limits
    xmin, ymin, xmax, ymax = gdf.total_bounds
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    ax.set_axis_off()

    # Draw background rectangle
    ax.add_patch(
        plt.Rectangle(
            (0, 0),
            1,
            1,
            facecolor="#ecedea",
            transform=ax.transAxes,
            zorder=-1
        )
    )

    ax.margins(0, 0)

    return ax
