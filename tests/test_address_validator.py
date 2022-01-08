from usps import USPSApi, Address
import json
import os
import pytest
from dotenv import load_dotenv
load_dotenv()
from geocodetools.address_validator import load_credentials, validate
import logging
logging.basicConfig(filename='../logfiles/geocode.log')

@pytest.fixture(params=[1])
def addresses(request):

    base_dir = 'data'
    idx = request.param

    with open(os.path.join(base_dir, f'test_address_{idx}.json')) as j:
        test_address = json.load(j)

    with open(os.path.join(base_dir, f'target_address_{idx}.json')) as j:
        target_address = json.load(j)

    return {'test': test_address, 'target': target_address}


class TestValidateAddress:

    def test_load_credentials(self):

        creds = load_credentials()

        assert type(creds) == dict

    def test_validate(self, addresses):

        creds = load_credentials()

        validated = validate(addresses['test'], creds)

        for key, val in addresses['target'].items():
            assert key in validated.keys()
            assert val == validated[key]



