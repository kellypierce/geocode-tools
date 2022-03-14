# Geocoding Tools

## Geocoding in R

The R package [`tidygeocoder`](https://cran.r-project.org/web/packages/tidygeocoder/vignettes/tidygeocoder.html) provides a friendly interface to the US Census Bureau [Public Geocoder API](https://www2.census.gov/geo/pdfs/maps-data/data/FAQ_for_Census_Bureau_Public_Geocoder.pdf).

This repository contains helper scripts ([`rscripts/geocode.r`](https://github.com/kellypierce/geocode-tools/blob/main/rscripts/geocode.r)) that help with batch processing of large datasets using functions from the `tidygeocoder` package.

## Address validation in Python

The Python package `usps-api` provides a friendly interface to the US Postal Service [Web Tools API](https://www.usps.com/business/web-tools-apis/). This API includes an address validation service that can be used to clean *small* numbers of addresses.

This repository contains helper scripts ([`geocodetoools/address_validator.py`](https://github.com/kellypierce/geocode-tools/blob/main/geocodetools/address_validator.py)) that help with processing of addresses requiring validation.

## Geocoding in Python

This repository also contains Python wrappers to `tidygeocoder` scripts using the [`rpy2`](https://rpy2.github.io/) library for running R embedded in a Python process.

These wrappers allow the address validation and geocoding workflows to be unified in Python; for example, through the creation of a single Jupyer notebook or Python script that performs both the R-native and Python-native tasks.

## Quickstart

### Clone the repository

	git clone https://github.com/kellypierce/geocode-tools.git

### Environment setup

#### R requirements

- packages listed in [`renv.lock`](https://github.com/kellypierce/geocode-tools/blob/main/renv.lock)

#### Python requirements

- packages listed in [`requirements.txt`](https://github.com/kellypierce/geocode-tools/blob/main/requirements.txt)
- install locally using the provided `setup.py` script (e.g. `pip3 install .` from within the repository directory)

#### USPS Web Tools API key

The Python scrips in this repository are designed to use the `python-dotenv` library to store and retrieve credentials saved as environment variables in a `.env` file.

- Register for API credentials at https://www.usps.com/business/web-tools-apis/
- Create a `.env` file in the repository directory and assign the variables `USPS_API_UID` and `USPS_API_PWD` the values of your user ID and password, respectively.

