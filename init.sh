#!/bin/bash

# check for pip
echo "Checking for pip existence"
which pip
if [[ $? != 0 ]]; then
  echo "Do you have pip installed? You can install it by running `sudo easy_install pip`"
  exit 1
fi

# check software dependencies
echo "Installing or checking for dependencies"
sudo pip install flask
sudo pip install pyshp

# check data dependencies
echo "Checking for shape files"
if [ ! -d "resources/StatePlane" ]; then
  echo "No shapefiles found, fetching from data.seattle.gov"
  curl -L https://data.seattle.gov/download/xg4t-j322/application%2Fzip > resources/shapefile.zip
  cd resources
  unzip shapefile.zip
  cd ..
fi

# run the application
echo "Starting the application"
FLASK_APP=tree-map.py flask run
sleep 2
open http://localhost:5000
