from shapely.geometry import shape, MultiPolygon, mapping
import pandas as pd
import geopandas as gpd
import geohash as gh

BASE32 = "0123456789bcdefghjkmnpqrstuvwxyz"

def geohashes(geojson={}, precision=6):
  """
    Return the list of geohashes that interects the geojson.
  """
  polygon = _polygon_from_geojson(geojson)
  if not polygon:
    return []

  p = min(2, precision)
  center_geohash = get_center_geohash(polygon, precision=p)
  _geohashes = [center_geohash] + gh.neighbors(center_geohash)
  _geohashes = geohashes_polygon_intersection(polygon, _geohashes)

  while p < precision:
    _geohashes = _generate_inner_geohashes_for_geohashes(_geohashes)
    _geohashes = geohashes_polygon_intersection(polygon, _geohashes)
    p += 1

  return _geohashes

def get_center_geohash(polygon, precision=2):
  centroid = mapping(polygon.centroid)["coordinates"]
  return gh.encode(centroid[1], centroid[0], precision=precision)

def geohashes_polygon_intersection(polygon, geohashes=[]):
  df = gpd.GeoDataFrame(geohashes, columns=["geohash"])
  df["geometry"] = df.apply(lambda x: _geohash_to_shape(x["geohash"]), axis=1)
  return list(df[df.intersects(polygon)].geohash)

def _generate_inner_geohashes_for_geohashes(geohashes=[]):
  return _flatten(map(_generate_inner_geohashes_for_geohash, geohashes))

def _generate_inner_geohashes_for_geohash(geohash=""):
  return ["%s%s" % (geohash, l) for l in list(BASE32)]

def _flatten(lyst):
  return [item for sublist in lyst for item in sublist]

def _multi_polygon_to_polygons(geom):
  if geom.geom_type == 'MultiPolygon':
    return list(geom)
  return [geom]

def _polygon_from_geojson(geojson={}):
  if geojson.get("type", None) == "FeatureCollection":
    df = pd.DataFrame(geojson.get("features", []))
    df["polygon"] = df.geometry.map(lambda x: shape(x))
    return MultiPolygon(_flatten(map(_multi_polygon_to_polygons, df["polygon"].values)))
  elif geojson.get("type", None) == "Feature":
    return shape(geojson.get("geometry", None))
  return None

def _geohash_to_shape(geohash):
    box = gh.bbox(geohash)
    coords = [
        [box["w"], box["s"]],
        [box["w"], box["n"]],
        [box["e"], box["n"]],
        [box["e"], box["s"]],
        [box["w"], box["s"]],
    ]
    return shape({"type": "Polygon", "coordinates": [coords]})
