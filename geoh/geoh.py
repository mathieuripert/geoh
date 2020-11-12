from shapely.geometry import shape, MultiPolygon, mapping
import pandas as pd
import geohash as gh


BASE32 = "0123456789bcdefghjkmnpqrstuvwxyz"

def geohashes(geojson={}, precision=6, start_precision=2):
    """
        Return the list of geohashes that interects the geojson.
    """
    polygon = _polygon_from_geojson(geojson)
    if not polygon:
        return []

    precision_init = precision
    if precision_init >= 9:
        precision = precision - 1

    p = min(start_precision, precision)

    center_geohash = get_center_geohash(polygon, precision=p)
    _geohashes = [center_geohash] + gh.neighbors(center_geohash)
    _geohashes = geohashes_polygon_intersection(polygon, _geohashes)

    while p < precision:
        _geohashes = _generate_inner_geohashes_for_geohashes(_geohashes)
        _geohashes = geohashes_polygon_intersection(polygon, _geohashes)
        p += 1

    if precision_init >= 9:
        inside_geohashes_coarse =  geohashes_polygon_within(polygon, _geohashes)
        inside_geohashes = _generate_inner_geohashes_for_geohashes(inside_geohashes_coarse)

        intersect_geohashes_coarse = list(set(_geohashes) - set(inside_geohashes_coarse))
        intersect_geohashes = _generate_inner_geohashes_for_geohashes(intersect_geohashes_coarse)
        intersect_geohashes = geohashes_polygon_intersection(polygon, intersect_geohashes)

        return inside_geohashes + intersect_geohashes

    else:
        return _geohashes

def get_center_geohash(polygon, precision=2):
    centroid = mapping(polygon.centroid)["coordinates"]
    return gh.encode(centroid[1], centroid[0], precision=precision)

def geohashes_polygon_intersection(polygon, geohashes=[]):
    """Return geohashes that intersect `polygon`"""
    from itertools import compress
    geoms = map(_geohash_to_shape, geohashes)
    intersections = map(lambda g_h: g_h.intersects(polygon), geoms)
    return list(compress(geohashes, intersections))

def geohashes_polygon_within(polygon, geohashes=[]):
    from itertools import compress
    geoms = map(_geohash_to_shape, geohashes)
    withins = map(lambda g_h: g_h.within(polygon), geoms)
    return list(compress(geohashes, withins))

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
        features = [f for f in geojson.get("features", []) if f is not None]
        df = pd.DataFrame(features, columns=["geometry"])
        df["polygon"] = df[pd.notnull(df.geometry)].geometry.map(lambda x: shape(x))
        df = df[pd.notnull(df.polygon)]
        if len(df.index):
            return MultiPolygon(_flatten(map(_multi_polygon_to_polygons, df["polygon"].values)))
        else:
            return None
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
