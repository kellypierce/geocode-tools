from arcgis.gis import GIS
from arcgis.geocoding import Geocoder, get_geocoders, geocode, batch_geocode
from usps import USPSApi, Address
import pandas as pd
import json
import rpy2.robjects as ro
from rpy2.robjects import r, pandas2ri
from rpy2.robjects.packages import importr
pandas2ri.activate()


def load_geocode():
    """
    Load the R package `tidygeocoder` and return the `geocode()` function as an rpy2 object.
    :return:
    """
    gcr = importr('tidygeocoder')

    return gcr.geocode


def load_as_tibble():
    """
    Load the R package `tibble` and return the `as_tibble()` function as an rpy2 object.
    :return:
    """
    tb = importr('tibble')

    return tb.as_tibble

def load_as_dataframe():
    """
    Load the R method as.data.frame as an rpy2 object.
    :return:
    """

    asdf = ro.r('as.data.frame')

    return asdf


def sample_df():

    tacc = {
        'full_address': ['10100 Burnet Rd Austin TX 78757', 'Patterson Labs UT Austin'],
        'street': ['10100 Burnet Rd', '2401 Speedway'],
        'city': ['Austin', 'Austin'],
        'county': ['Travis', 'Travis'],
        'state': ['Texas', 'Texas'],
        'postalcode': ['78757', '78712']
    }
    df = pd.DataFrame.from_dict(tacc)
    return df


def main():

    r_as_tibble = load_as_tibble()
    r_geocode = load_geocode()
    df = sample_df()

    rdf = pandas2ri.py2rpy(df)
    rtib = r_as_tibble(rdf)
    gc = r_geocode(
        rtib,
        address='full_address',
        method='census',
        full_results=True,
        return_type='geographies'
    )

    return gc

if __name__ == '__main__':

    # load USPS API credentials
    with open('/Users/kpierce/CooksProTX/usps_api_credentials.json', 'r') as f:
        credentials = json.load(f)

    result = main()
