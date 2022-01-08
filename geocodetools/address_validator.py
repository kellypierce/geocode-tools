from usps import USPSApi, Address
import os
import pdb
from dotenv import load_dotenv
load_dotenv()
import logging
logging.basicConfig(filename='../logfiles/geocode.log')

def load_credentials():

    errors = False
    try:
        uid = os.environ['USPS_API_UID']
    except KeyError:
        logging.error('USPS_API_UID environment variable not set.')
        errors = True

    try:
        pwd = os.environ['USPS_API_PWD']
    except KeyError:
        logging.error('USPS_API_PWD environment variable not set.')
        errors = True

    if errors:
        raise Exception('USPS API credentials not found in environment.')

    return {"username": uid, "password": pwd}

def validate(addr_dict, credentials):

    addr_dict['name'] = None
    addr_dict['state'] = None
    addr_dict['address_1'] = addr_dict['address']  # expect column header "address" from dfps data
    addr_dict.pop('address', None)

    usps = USPSApi(credentials['username'], test=True)

    #pdb.set_trace()
    fmt_addr = Address(**addr_dict)
    validated_addr_response = usps.validate_address(fmt_addr).result
    try:
        validated_addr_dict = validated_addr_response['AddressValidateResponse']['Address']
    except KeyError:
        logging.error('Did not receive valid response for address {}'.format(addr_dict))
        raise Exception

    validated_addr = {
        'address': validated_addr_dict['Address2'],
        'city': validated_addr_dict['City'],
        'zip_code': '{}-{}'.format(validated_addr_dict['Zip5'], validated_addr_dict['Zip4'])
    }

    return validated_addr
