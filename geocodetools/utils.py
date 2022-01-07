import datetime
import logging
import pandas as pd
import pdb
logging.basicConfig(filename='../logfiles/geocode.log')


def type_sanitizer(series, target_type):
    """Attempt to coerce all elements in a pandas Series object ot the target_type"""
    assert target_type in set(['int32', 'int64', 'float32', 'float64', 'str', 'date', 'int'])

    if target_type == 'date':
        series = pd.to_datetime(series)

    else:
        try:
            series = series.astype(target_type)

        except (ValueError, TypeError):
            logging.info('Unable to convert pd.Series to type {}'.format(target_type))

    return series