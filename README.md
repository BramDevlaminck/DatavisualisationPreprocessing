# Datavisualisation Crime data

This repository contains some python files to extract the number of official registered bike sheds in Ghent per quarter.

Furthermore, we also created a JSON with all the University and graduate campuses that we found in Ghent.  
We also include a script to add the geo point data and quarter data to these addresses.

## Results
The results of the 2 scripts can be found back in the `/out` directory.

## How to run?
### Required data
We expect 2 datasets to be present in the `/Datasets` folder.  
These can be downloaded by running 
```bash
./fetch_datasets.sh
```
in the root of this project.

### Setting up the environment
This project was set up using [poetry](https://python-poetry.org/).  
To install all the required dependencies and create a venv, simply run
```bash
poetry install
```
in the root directory of this project.  
After that you can just run the script you need and everything should work out-of-the-box.