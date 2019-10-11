import os
import json
import pytest
import geoh

@pytest.fixture
def geojson_sf():
  __location__ = os.path.realpath(os.path.join(
      os.getcwd(), os.path.dirname(__file__)))
  geojson = json.loads(
    open(os.path.join(__location__, './geojson-sf.json')).read())
  return geojson

@pytest.fixture
def geojson_none():
  return {
    'type': 'FeatureCollection', 
    'features': [None]
  }

@pytest.fixture
def malformed_geojson():
    return {
        'type': 'FeatureCollection',
        'features': [{
          'geometry': None,
          'type': 'Polygon',
        }]
    }

@pytest.mark.parametrize("precision", [1, 2 ,3, 4, 5, 6])
def test_sf(geojson_sf, precision):
  geohashes = geoh.geohashes(geojson=geojson_sf, precision=precision)
  assert(len(geohashes) > 0)

@pytest.mark.parametrize("precision", [1, 2, 3, 4, 5, 6])
def test_with_none_geojson(geojson_none, precision):
  geohashes = geoh.geohashes(geojson=geojson_none, precision=precision)
  assert(geohashes == [])


@pytest.mark.parametrize("precision", [1, 2, 3, 4, 5, 6])
def test_with_malformed_geojson(malformed_geojson, precision):
  geohashes = geoh.geohashes(geojson=malformed_geojson, precision=precision)
  assert(geohashes == [])
