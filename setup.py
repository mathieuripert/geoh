from distutils.core import setup
from setuptools import find_packages

required = [
    "pandas>=0.15.2",
    "geopandas>=0.2",
    "shapely>=1.5.13",
    "python-geohash>=0.8.5"
]

setup(
    name="geoh",
    version="0.3",
    author="Mathieu Ripert",
    author_email="mathieu@instacart.com",
    url="https://github.com/mathieuripert/geoh",
    license="MIT",
    packages=find_packages(),
    package_dir={"geoh": "geoh"},
    description="Transform a geoJSON into a list of geohashes that intersect with it",
    install_requires=required,
    classifiers=[],

)
