import shapefile
import json
from flask import Flask, render_template
from tree import Tree

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
        tree = Tree(shape.record)
        ## TODO: make this configurable and modifiable with request args
        treeType = tree.commonName
        if ('Apple' in treeType \
            or 'apple' in treeType) \
            and not is_crabby(treeType) \
            and not is_service_berry(treeType) \
            and 'INSVC' == tree.currentStatus:
            trees.append(tree.__dict__)
    print "Found " + str(len(trees)) + " fruitful trees"

    return trees

def is_crabby(commonName):
    return 'Crab' in commonName \
        or 'crab' in commonName

def is_service_berry(commonName):
    return 'Serviceberry' in commonName \
        or 'serviceberry' in commonName
