# geoh
Transform a geoJSON into a list of geohashes that intersect with it.


## Install

`pip install geoh`


## How to use it

```
import geoh

geohashes = geoh.geohashes(geojson=geojson, precision=6)

```

## Example

Let's take the geojson of San Francisco boundaries. (available here https://github.com/mathieuripert/geoh/blob/master/examples/geojson-sf.json)

![alt text](https://i.imgur.com/e5uN0oK.png)

#### Geohash coverage with precision 5
`geohashes = geoh.geohashes(geojson=geojson, precision=5)`
```
['9q8yh', '9q8yj', '9q8yk', '9q8ym', '9q8yn', '9q8yp', '9q8yq', '9q8yr', '9q8ys', '9q8yt', '9q8yu', '9q8yv', '9q8yw', '9q8yx', '9q8yy', '9q8yz', '9q8zh', '9q8zj', '9q8zn', '9q8zp']
```

![alt text](https://i.imgur.com/qAxtaNh.png)

#### Geohash coverage with precision 6
`geohashes = geoh.geohashes(geojson=geojson, precision=6)`

![alt text](https://i.imgur.com/LonsbLD.jpg)



