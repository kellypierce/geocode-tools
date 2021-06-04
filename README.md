# Geocoding Tools

## Environment

This environment relies on some locally built packages. The file `esri-geocode.yml` lists the packages in the environment, but it might be more convenient to set up the environment (including local package builds) by hand.

    conda create --name esri-geocode python=3.7
    conda activate esri-geocode

## Packages from channel `esri`

This package includes the ESRI geocoding functions.

    conda install -c esri arcgis

## Packages from channel `r`:

    conda install -c r r-tidyverse

## Packages from channel `conda-forge`:

The version of rpy2 in the `r` channel is outdated and incompatible with more recent versions of pandas.

    conda install -c conda-forge r-tidygeocoder rpy2

## Packages from PyPI:

This package includes a function for address validation using the USPS API. It can be installed directly using `pip`, but I've elected to rebuild as a conda package so all packages are managed by conda. The downside is that the conda environment is less portable, but the upside is that the `esri-geocode.yml` file lists all of the dependencies (whereas `pip`-installed packages aren't captured in this file).

    conda install conda-build
    conda skeleton pypi usps-api
    conda-build usps-api
    conda install /path/to/build.tar.bz2

The path for the local build is included in the standard out returned by `conda-build usps-api`.