import shapefile
import json
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def map():
    return render_template('map.html')

@app.route('/trees')
def trees():
    return json.dumps(get_trees(), indent=4, sort_keys=True, default=str)

trees = []

def get_trees():
    print "Getting trees"

    # they are already loaded. this will change in the future for filtering them.
    # effectively a naive cache.
    if len(trees) > 0:
        print "We have cached trees. Returning them"
        return trees

    # open the shapefile containing the trees
    sf = shapefile.Reader('resources/StatePlane/Trees.shp')

    # split into shape records: so that the point is associated with a tree
    shapes = sf.shapeRecords()
    print "Checking " + str(len(shapes)) + " trees for fruitfulness"

    ## TODO: convert the array index of the shape record into a key/value map
    for shape in shapes:
        # common name: index 34
        # address: index 5
        # latitude: index 44
        # longitude: index 43
        # tree state: index 9: one of [INSVC, REMOVED]
        commonName = shape.record[34]
        address = shape.record[5]
        latitude = shape.record[44]
        longitude = shape.record[43]
        treeState = shape.record[9]

        ## TODO: make this configurable and modifiable with request args
        if ('Apple' in commonName \
            or 'apple' in commonName) \
            and not is_crabby(commonName) \
            and not is_service_berry(commonName) \
            and 'INSVC' in treeState:
            trees.append({
                'commonName': commonName,
                'address': address,
                'latitude': latitude,
                'longitude': longitude,
                'state': treeState,
                'verboseDetails': shape.record
            })
    print "Found " + str(len(trees)) + " fruitful trees"
    
    return trees

def is_crabby(commonName):
    return 'Crab' in commonName \
        or 'crab' in commonName

def is_service_berry(commonName):
    return 'Serviceberry' in commonName \
        or 'serviceberry' in commonName
