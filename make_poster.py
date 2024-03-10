"""Make a poster of a city area with OSM data"""

import traceback
import warnings

import click
from srai.loaders import OSMPbfLoader
from srai.regionalizers import geocode_to_region_gdf

import utils
from config import config

warnings.simplefilter("ignore")


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
    help="Output file path. By default, the file is saved as "
    + "'<config_name>_<paper_size>.pdf>' in the current directory.",
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
    paper_dimensions = get_paper_dimensions(paper_size)

    # Get area
    area = get_area(properties)

    # Parse feature properties
    feature_props = get_feature_properties(properties)

    # Get OSM features
    features = get_osm_features(area, feature_props)

    # Get lat/lon range of the features
    lon_lat_lims = get_feature_bounds(features)

    # Get pin center
    pin_center = get_pin_center(properties, lon_lat_lims)

    # Transform coordinates according to zoom level
    lon_lat_lims = transform_coordinates(lon_lat_lims, pin_center, properties)

    # Set figure size in inches
    figsize = get_figure_size(paper_dimensions)

    # Plot the poster
    background_color = properties.get(
        "background_color", utils.get_default_background_color()
    )
    fig, ax = utils.plot_poster(
        gdf_and_features=(features, feature_props),
        background_color=background_color,
        lon_lat_lims=lon_lat_lims,
        figsize=figsize,
    )

    # Parse output name
    output = parse_output_name(output, config_name, paper_size)

    # Save the poster
    save_poster(fig, output, dpi)

    print(f"Done. Poster saved as {output}.")


def get_paper_dimensions(paper_size: str):
    try:
        paper_size = paper_size.upper()
        return utils.PAPER_SIZES[paper_size]
    except KeyError:
        raise ValueError(
            f"Paper size {paper_size} not found. Options are: {list(utils.PAPER_SIZES.keys())}"
        )


def get_area(properties):
    query = properties["query"]
    by_osmid = properties.get("by_osmid", False)
    print(f"Getting area {query}, by OSM ID = {by_osmid}...")
    return geocode_to_region_gdf(query, by_osmid=by_osmid)


def get_feature_properties(properties):
    return properties.get("feature_props", utils.get_default_feature_props())


def get_osm_features(area, feature_props):
    features_to_load = {key: True for key in feature_props.keys()}
    features = OSMPbfLoader().load(area, features_to_load).clip(area)
    if features.empty:
        possible_features = utils.get_possible_feature_names()
        raise ValueError(
            "No features with given names found in the area. Possible features are: {}".format(
                possible_features
            )
        )
    return features


def get_feature_bounds(features):
    return features.total_bounds


def get_pin_center(properties, lon_lat_lims):
    pin_center = properties.get("pin_center", [None, None])
    return utils.parse_pin_center(pin_center, lon_lat_lims)


def transform_coordinates(lon_lat_lims, pin_center, properties):
    zoom_level = properties.get("zoom_level", 1.0)
    return utils.zoom(lon_lat_lims, pin_center, zoom_level)


def get_figure_size(paper_dimensions):
    page_length, page_width = paper_dimensions
    return page_length / 25.4, page_width / 25.4


def parse_output_name(output: str, config_name: str, paper_size: str) -> str:
    if output is None:
        output = f"{config_name}_{paper_size}.pdf"
    return output


def save_poster(fig, output, dpi):
    fig.savefig(output, bbox_inches="tight", pad_inches=0, dpi=dpi)
    fig.clf()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(traceback.format_exc())
        raise e
