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

@pytest.fixture
def geojson_small():
    return {
      "type": "Feature",
      "geometry": {"coordinates": [[[-80.20607, 40.248738],
                                    [-80.205726, 40.248738],
                                    [-80.205726, 40.248484],
                                    [-80.20607, 40.248484],
                                    [-80.20607, 40.248738]]],
                   "type": "Polygon"},
      "properties": {}
    }

@pytest.mark.parametrize("precision", [1, 2 ,3, 4, 5, 6])
def test_sf(geojson_sf, precision):
  geohashes = geoh.geohashes(geojson=geojson_sf, precision=precision)
  geohashes_5 = geoh.geohashes(geojson=geojson_sf, precision=5)
  assert(len(geohashes) > 0)
  assert(set(geohashes_5) == set(["9q8yh", "9q8yj", "9q8yk", "9q8ym", "9q8yq",
                             "9q8ys", "9q8yt", "9q8yu", "9q8yv", "9q8yw",
                             "9q8yx", "9q8yy", "9q8yz", "9q8zh", "9q8zj",
                             "9q8zn", "9q8zp"]))

@pytest.mark.parametrize("precision", [1, 2, 3, 4, 5, 6])
def test_with_none_geojson(geojson_none, precision):
  geohashes = geoh.geohashes(geojson=geojson_none, precision=precision)
  assert(geohashes == [])


@pytest.mark.parametrize("precision", [1, 2, 3, 4, 5, 6])
def test_with_malformed_geojson(malformed_geojson, precision):
  geohashes = geoh.geohashes(geojson=malformed_geojson, precision=precision)
  assert(geohashes == [])


def test_geojson_small_geohash_9(geojson_small, precision=9):
  geohashes = geoh.geohashes(geojson=geojson_small, precision=precision)
  assert (set(geohashes) == set(['dpnuyz58r', 'dpnuyz58x', 'dpnuyz58z', 'dpnuyz59p', 'dpnuyz59r',
                                 'dpnuyz59x', 'dpnuyz59z', 'dpnuyz5b2', 'dpnuyz5b3', 'dpnuyz5b6',
                                 'dpnuyz5b7', 'dpnuyz5b8', 'dpnuyz5b9', 'dpnuyz5bb', 'dpnuyz5bc',
                                 'dpnuyz5bd', 'dpnuyz5be', 'dpnuyz5bf', 'dpnuyz5bg', 'dpnuyz5bk',
                                 'dpnuyz5bm', 'dpnuyz5bq', 'dpnuyz5br', 'dpnuyz5bs', 'dpnuyz5bt',
                                 'dpnuyz5bu', 'dpnuyz5bv', 'dpnuyz5bw', 'dpnuyz5bx', 'dpnuyz5by',
                                 'dpnuyz5bz', 'dpnuyz5c0', 'dpnuyz5c1', 'dpnuyz5c2', 'dpnuyz5c3',
                                 'dpnuyz5c4', 'dpnuyz5c5', 'dpnuyz5c6', 'dpnuyz5c7', 'dpnuyz5c8',
                                 'dpnuyz5c9', 'dpnuyz5cb', 'dpnuyz5cc', 'dpnuyz5cd', 'dpnuyz5ce',
                                 'dpnuyz5cf', 'dpnuyz5cg', 'dpnuyz5ch', 'dpnuyz5cj', 'dpnuyz5ck',
                                 'dpnuyz5cm', 'dpnuyz5cn', 'dpnuyz5cp', 'dpnuyz5cq', 'dpnuyz5cr',
                                 'dpnuyz5cs', 'dpnuyz5ct', 'dpnuyz5cu', 'dpnuyz5cv', 'dpnuyz5cw',
                                 'dpnuyz5cx', 'dpnuyz5cy', 'dpnuyz5cz']))