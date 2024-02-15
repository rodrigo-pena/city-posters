"""Make a poster of a city area with OSM data"""

import click
import traceback
import utils
import warnings

from config import config
from srai.regionalizers import geocode_to_region_gdf
from srai.loaders import OSMPbfLoader

warnings.simplefilter("ignore")

# Paper sizes
paper_sizes = {
    "A0": (1189, 841),  # (height, width) in mm
    "A1": (841, 594),   # (height, width) in mm
    "A2": (594, 420),   # (height, width) in mm
    "A3": (420, 297),   # (height, width) in mm
    "A4": (297, 210),   # (height, width) in mm
}


@click.command()
@click.option(
    "--config_name",
    "-cn",
    required=True,
    help="Name of configuration to use from the config.py file",
)
@click.option(
    "--output",
    "-o",
    default=None,
    help="Output file path. By default, the file is saved as " +
    "'<config_name>_<paper_size>.pdf>' in the current directory.",
)
@click.option(
    "--paper-size",
    "-ps",
    default="A2",
    help="Paper size",
)
@click.option(
    "--dpi",
    "-d",
    default=300,
    help="DPI",
)
def main(config_name: str, output: str, paper_size: str, dpi: int):
    # Get configuration properties from config.py
    properties = config[config_name]

    # Get paper size
    try:
        paper_size = paper_size.upper()
        paper_dimensions = paper_sizes[paper_size]
    except KeyError:
        raise ValueError(f"Paper size {paper_size} not found." +
                         f" Options are: {list(paper_sizes.keys())}")

    # Get area
    print(f"Getting area for {properties['city']}, {properties['country']}...")
    area_name = f"{properties['city']}, {properties['country']}"
    area = geocode_to_region_gdf(area_name)

    # Parse feature properties
    try:
        feature_props = properties["feature_props"]
    except KeyError:
        feature_props = utils.get_default_feature_props()

    # Get OSM features
    features_to_load = {}
    for key in feature_props.keys():
        features_to_load[key] = True
    features = (
        OSMPbfLoader().load(area, features_to_load).clip(area)
    )
    if features.empty:
        possible_features = utils.get_possible_feature_names()
        raise ValueError("No features with given names found in the area. " +
                         "Possible features are: {}".format(possible_features))

    # Get lat/lon range of the features
    lon_min, lat_min, lon_max, lat_max = features.total_bounds

    # Get pin center
    try:
        pin_center = properties["pin_center"]
    except KeyError:
        pin_center = [None, None]
    pin_center = utils.parse_pin_center(pin_center,
                                        lon_min,
                                        lat_min,
                                        lon_max,
                                        lat_max)

    # Transform coordinates according to zoom level
    try:
        zoom_level = properties["zoom_level"]
    except KeyError:
        zoom_level = 1.
    lon_min, lat_min, lon_max, lat_max = utils.zoom(
        lon_min,
        lat_min,
        lon_max,
        lat_max,
        pin_center,
        zoom_level
    )

    # Fit the map to an A2 paper size
    try:
        orientation = properties["orientation"]
    except KeyError:
        orientation = "portrait"
    lon_min, lat_min, lon_max, lat_max = utils.fit_to_paper(
        lon_min,
        lat_min,
        lon_max,
        lat_max,
        paper_size=paper_size,
        orientation=orientation
    )

    # Set figure size in inches
    page_length, page_width = paper_dimensions
    figsize = (page_length / 25.4, page_width / 25.4)

    # Plot the poster
    print(
        f"Plotting poster for {properties['city']}, {properties['country']}..."
    )
    fig, _ = utils.plot_poster(
        features,
        feature_props=feature_props,
        lon_lim=(lon_min, lon_max),
        lat_lim=(lat_min, lat_max),
        figsize=figsize,
    )

    # Save the poster
    if output is None:
        output = f"{config_name}_{paper_size}.pdf"
    fig.savefig(output, bbox_inches="tight", pad_inches=0, dpi=dpi)

    # Close the figure
    fig.clf()

    print(f"Done. Poster saved as {output}.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(traceback.format_exc())
        raise e
