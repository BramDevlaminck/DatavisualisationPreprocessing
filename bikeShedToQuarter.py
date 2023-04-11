import json
from typing import TextIO
from turfpy.measurement import boolean_point_in_polygon
from geojson import Point, Polygon, Feature


def open_json(filename: str) -> TextIO:
    data: TextIO
    with open(filename) as fp:
        data = json.load(fp)
    return data


def extract_quarters(filename: str) -> dict[str, list[list[tuple[float, float]]]]:
    """Return a dict with as key the quarter and as value the polygon coordinate shape of that quarter"""
    data = open_json(filename)

    quarter_to_geo_list: dict[str, list[list[tuple[float, float]]]] = dict()
    for item in data:
        quarter = item["quarter"]
        if quarter not in quarter_to_geo_list.keys():
            if quarter != "Onbekend":
                geom = item["geometry"]["geometry"]["coordinates"][0]
                quarter_to_geo_list[quarter] = [[(float(loc[0]), float(loc[1])) for loc in geom]]

    return quarter_to_geo_list


def extract_bike_sheds(filename: str) -> dict[tuple[float, float], int]:
    """Return a dicht with as key a coordinate point of a bike shed and as value the size of that bike shed"""
    data = open_json(filename)

    bike_shed_with_size: dict[tuple[float, float], int] = dict()
    for item in data:
        geo_point = item["geo_point_2d"]
        point: tuple[float, float] = float(geo_point["lon"]), float(geo_point["lat"])
        size: int = item["capaciteit"]
        bike_shed_with_size[point] = size

    return bike_shed_with_size


def calculate_places_per_quarter(quarter_data: dict[str, list[list[tuple[float, float]]]], bike_shed_data: dict[tuple[float, float], int]):
    """Return a dict with as key the quarter and as value the numer of bike places in that quarter"""
    polygon_per_quarter: dict[str, Polygon] = dict()

    for quarter, coordinates in quarter_data.items():
        # the type hint in polygon itself is wrong, the right type is list[list[tuple[float, float]]]
        polygon_per_quarter[quarter] = Polygon(coordinates)

    bike_places_per_quarter: dict[str, int] = {quarter: 0 for quarter in polygon_per_quarter.keys()}
    for coord, size in bike_shed_data.items():
        point = Feature(geometry=Point(coord))
        for quarter, polygon in polygon_per_quarter.items():
            if boolean_point_in_polygon(point, polygon):
                bike_places_per_quarter[quarter] += size

    return bike_places_per_quarter


if __name__ == "__main__":
    # download datasets as JSON from here: https://data.stad.gent/explore/?disjunctive.keyword&disjunctive.theme&sort=modified&q=politie
    quarter_data = extract_quarters("Dataset/criminaliteitscijfers-per-wijk-per-maand-gent-2022.json")
    # download dataset as JSON from here: https://data.stad.gent/explore/dataset/fietsenstallingen-gent/export/
    bike_data = extract_bike_sheds("Dataset/fietsenstallingen-gent.json")
    print(calculate_places_per_quarter(quarter_data, bike_data))
