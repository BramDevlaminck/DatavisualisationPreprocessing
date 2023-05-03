import json
import sys
from dataclasses import dataclass
import requests
from geojson import Polygon, Point, Feature
from turfpy.measurement import boolean_point_in_polygon

from bikeShedToQuarter import open_json, extract_quarters, get_quarter_polygons


@dataclass
class Campus:
    house_number: int
    street: str
    city: str = "Ghent"
    postalCode: int = 9000
    country: str = "Belgium"
    name: str = ""
    institute: str = ""

    def to_request_params(self) -> dict[str: str]:
        return {
            "street": f"{self.house_number} {self.street}",
            "city": self.city,
            "country": self.country,
            "postalCode": self.postalCode
        }

    def __str__(self):
        return f"{self.street} {self.house_number}, {self.postalCode} {self.city}, {self.country} ({self.institute}: {self.name})"


@dataclass
class CampusPoint:
    lat: str
    lon: str
    name: str = ""
    institute: str = ""
    quarter: str = ""

    def to_dict(self) -> dict[str, str]:
        return {
            "lat": self.lat,
            "lon": self.lon,
            "name": self.name,
            "institute": self.institute,
            "quarter": self.quarter
        }


def address_to_location(address: Campus, quarters: dict[str, Polygon]) -> CampusPoint | None:
    response = requests.get("https://geocode.maps.co/search", params=address.to_request_params())
    if response.ok:
        res = response.json()[0]
        lat, lon = res["lat"], res["lon"]
        point = Feature(geometry=Point((float(lat), float(lon))))

        campus_point = CampusPoint(
            lat=lat,
            lon=lon,
            name=address.name,
            institute=address.institute,
        )
        # search the matching quarter and set it if we find one
        for quarter, polygon in quarters.items():
            if boolean_point_in_polygon(point, polygon):
                campus_point.quarter = quarter
                return campus_point
        return campus_point

    else:
        print("Could not find geo point associated with following campus: " + str(address), file=sys.stderr)


def campussen_json_to_objects(filename: str) -> list[Campus]:
    data = open_json(filename)

    campussen: list[Campus] = []
    # data is actually a big dictionary, so .items() does work on it
    for institute, campus_data in data.items():
        for entry in campus_data:
            campussen.append(
                Campus(
                    house_number=entry["number"],
                    street=entry["street"],
                    city=entry["city"],
                    postalCode=entry["postalCode"],
                    country=entry["country"],
                    name=entry["name"],
                    institute=institute
                )
            )

    return campussen


if __name__ == "__main__":
    campussen_as_json = campussen_json_to_objects("Datasets/campuses.json")

    geo_points: list[CampusPoint] = []
    quarters = get_quarter_polygons(extract_quarters("Datasets/criminaliteitscijfers-per-wijk-per-maand-gent-2022.json"))
    for campus in campussen_as_json:
        res = address_to_location(campus, quarters)
        if res is not None:
            geo_points.append(res)

    out_file = open("out/geo_point_per_campus.json", "w")
    json.dump([campus_point.to_dict() for campus_point in geo_points], out_file, indent=4)


