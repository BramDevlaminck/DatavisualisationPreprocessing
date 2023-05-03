# Datavisualisation Crime data

This repository contains some python files to extract the number of official registered bike sheds in Ghent per quarter.

Furthermore, we also created a JSON with all the University and graduate campuses that we found in Ghent.
We also include a script to add the geo point data and quarter data to these addresses.

## Results
The results of the 2 scripts can be found back in the `/out` directory.

## How to run?
### Required data
We expect 2 datasets to be present in the `/Datasets` folder.  
These can be downloaded from [here](https://data.stad.gent/explore/?disjunctive.keyword&disjunctive.theme&sort=modified&q=politie) (Choose 1 of the listed datasets as json) and [here](https://data.stad.gent/explore/dataset/fietsenstallingen-gent/export/) (once again as a json).  
Once you downloaded these datasets, you can change the appropriate path to the datasets in `addressToGeoPoint.py`and `bikeShedToQuarter.py`

### Setting up the environment
This project was set up using [poetry](https://python-poetry.org/)
To install all the required dependencies and create a venv, simply run
```bash
poetry install
```
in the root directory of this project.

After that you can just run the script you need and everything should be good to go.