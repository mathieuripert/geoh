import json
import os

from geoh import geoh


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
geojson = json.loads(open(os.path.join(__location__, './tests/geojson-sf.json')).read())


geohashes = geoh.geohashes(geojson=geojson, precision=5)

print geohashes
