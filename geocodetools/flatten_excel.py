import pandas as pd
import logging
import json
import datetime
import pdb
from .utils import type_sanitizer
logging.basicConfig(filename='../logfiles/geocode.log')


def collect_sheets(sheet_path, metadata_path):
    """Read in an excel sheet, check for multiple tabs, and flatten to dataframe if necessary"""

    # load metadata for type setting by column
    with open(metadata_path, 'r') as m:
        metadata = json.load(m)

    # load data file
    logging.info('Loading excel sheet from path {}.'.format(sheet_path))
    xls = pd.read_excel(sheet_path, sheet_name=None, header=None)

    logging.info('\tIdentified {} sheets in file {}.'.format(len(xls.keys()), sheet_path))
    logging.info('\tSheet names are {}'.format(list(xls.keys())))

    # collect and concatenate all sheets
    xls_sheets = []
    for key, val in xls.items():
        sheet = clean_sheets(key, val, metadata)
        sheet['sheet_name'] = key
        xls_sheets.append(sheet)
    flat_xls = pd.concat(xls_sheets)

    return flat_xls


def clean_sheets(sheet_name, sheet, metadata):
    """Remove empty rows and incomplete rows above the header
        Steps:
            1. drop all rows and columns that are completely NA
            2. drop rows where only the first column has data (this indicates notes above the actual data)
            3. find the row that contains the column names in the metadata
            4. fix column types -- reading in w/no header will make numeric columns object type
    """

    # drop all columns that are completely null, and all rows that have one or fewer entries
    column_clean = sheet.dropna(axis=1, how='all')
    row_column_clean = column_clean.dropna(axis=0, how='all', thresh=2)

    # start discarding rows until one contains expected column names is found
    header_found = False
    header_index = None
    valid_idx = [i for i in row_column_clean.index]
    columns = set(metadata.keys())

    if not header_found:
        check_idx = valid_idx.pop(0)
        # does this row have the headers? not all headers must be specified in metadata, so we just need to check
        # that the expected columns are in the row vals
        row_vals = set(row_column_clean.loc[check_idx])
        if len(columns.difference(row_vals)) == 0:
            header_found = True
            header_index = check_idx

    if not header_found:
        logging.error('Unable to find expected header row in {}'.format(sheet_name))
        raise AssertionError

    row_column_clean.columns = row_column_clean.loc[header_index]
    row_column_clean.columns.name = None
    row_column_clean = row_column_clean.drop(labels=header_index)

    # sanitize the column types. if type not specified, treat as a string
    for col in row_column_clean:
        try:
            target_type = metadata[col]
        except KeyError:
            target_type = 'str'

        row_column_clean[col] = type_sanitizer(row_column_clean[col], target_type=target_type)

    return row_column_clean
