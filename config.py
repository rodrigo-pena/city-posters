"""Configuration file for make_poster.py

For area queries, see https://osm-boundaries.com/Map. You may query either by
string, e.g. 'Plano Piloto, Brazil', or by OSM ID. In the latter case, make
sure to also set the property 'by_osmid' to True. See
`osmnx.geocoder.geocode_to_gdf` for more information on formatting the area
query.
"""

config = {
    "df": {
        "query": ["R421151"],
        "by_osmid": True,
        "pin_center": (-47.88251815347833, -15.793941721687496),
        "zoom_level": (2.8, 2.8),
        "background_color": "#ecedea",
    },
    "df-no-bg": {
        "query": ["R421151"],
        "by_osmid": True,
        "pin_center": (-47.88251815347833, -15.793941721687496),
        "zoom_level": (2.8, 2.8),
        "background_color": None,
    },
    "brasilia-centro": {
        "query": [
            "R2758138",
            "R3359473",
            "R3359467",
            "R3359471",
            "R3359488",
            "R3359474",
        ],
        "by_osmid": True,
        "pin_center": (-47.88251815347833, -15.793941721687496),
        "zoom_level": (1.4, 2.1),
        "background_color": "#ecedea",
    },
    "brasilia-centro-no-bg": {
        "query": [
            "R2758138",
            "R3359473",
            "R3359467",
            "R3359471",
            "R3359488",
            "R3359474",
        ],
        "by_osmid": True,
        "pin_center": (-47.88251815347833, -15.793941721687496),
        "zoom_level": (1.4, 2.1),
        "background_color": None,
    },
    "plano-piloto": {
        "query": ["R3359467", "R3359488", "R2758138"],
        "by_osmid": True,
        "pin_center": (-47.88251815347833, -15.793941721687496),
        "zoom_level": (1.2, 1.8),
        "background_color": "#ecedea",
    },
    "plano-piloto-no-bg": {
        "query": ["R3359467", "R3359488", "R2758138"],
        "by_osmid": True,
        "pin_center": (-47.88251815347833, -15.793941721687496),
        "zoom_level": (1.2, 1.8),
        "background_color": None,
    },
    "warsaw-no-bg": {
        # "query": "Warsaw, Poland",
        "query": ["R336075", "R336134", "R336132", "R336131", "R336133"],
        "by_osmid": True,
        "zoom_level": 0.9,
        "background_color": None,
    },
    "warsaw": {
        # "query": "Warsaw, Poland",
        "query": ["R336075", "R336134", "R336132", "R336131", "R336133"],
        "by_osmid": True,
        "zoom_level": 0.9,
        "background_color": "#ecedea",
    },
    "basel-no-bg": {
        "query": "Basel-Stadt, Switzerland",
        "by_osmid": False,
        "zoom_level": 0.9,
        "background_color": None,
    },
    "basel": {
        "query": "Basel-Stadt, Switzerland",
        "by_osmid": False,
        "zoom_level": 0.9,
        "background_color": "#ecedea",
    },
    "lausanne-no-bg": {
        "query": ["R365554", "R365551"],
        "by_osmid": True,
        "zoom_level": 0.9,
        "background_color": None,
    },
    "lausanne": {
        "query": ["R365554", "R365551"],
        "by_osmid": True,
        "zoom_level": 0.9,
        "background_color": "#ecedea",
    },
    "bordeaux-no-bg": {
        "query": [
            "R105270",
            "R105271",
            "R105278",
            "R88613",
            "R88808",
            "R105280",
            "R88809",
            "R105268",
            "R88633",
            "R105283",
            "R88807",
            "R105275",
            "R105281",
            "R105267",
            "R105273",
        ],
        "by_osmid": True,
        "zoom_level": 0.9,
        "background_color": None,
    },
    "bordeaux": {
        "query": [
            "R105270",
            "R105271",
            "R105278",
            "R88613",
            "R88808",
            "R105280",
            "R88809",
            "R105268",
            "R88633",
            "R105283",
            "R88807",
            "R105275",
            "R105281",
            "R105267",
            "R105273",
        ],
        "by_osmid": True,
        "zoom_level": 0.9,
        "background_color": "#ecedea",
    },
}
