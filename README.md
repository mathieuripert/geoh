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
![alt text](https://i.imgur.com/qAxtaNh.png)

#### Geohash coverage with precision 6
`geohashes = geoh.geohashes(geojson=geojson, precision=5)`
![alt text](https://i.imgur.com/LonsbLD.jpg)



