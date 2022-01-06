import pandas as pd
import logging
logging.basicConfig(filename='../logfiles/geocode.log')


def collect_sheets(path):
    """Read in an excel sheet, check for multiple tabs, and flatten to dataframe if necessary"""

    logging.info('Loading excel sheet from path {}.'.format(path))
    xls = pd.read_excel(path, sheet_name=None)

    logging.info('\tIdentified {} sheets in file {}.'.format(len(xls.keys()), path))
    logging.info('\tSheet names are {}'.format(list(xls.keys())))

    xls_sheets = []
    for key, val in xls.items():
        val['sheet_name'] = key
        xls_sheets.append(val)
    flat_xls = pd.concat(xls_sheets)

    return flat_xls
