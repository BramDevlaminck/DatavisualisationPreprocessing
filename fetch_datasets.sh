#!/bin/bash

path="Datasets"
wget -O "${path}/quarter_shapes.geojson" "https://data.stad.gent/api/explore/v2.1/catalog/datasets/stadswijken-gent/exports/geojson"
wget -O "${path}/bike_parkings_data.json" "https://data.stad.gent/api/explore/v2.1/catalog/datasets/fietsenstallingen-gent/exports/json"