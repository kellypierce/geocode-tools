import datetime
import logging
import pandas as pd
import pdb


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


def deduplicate_colnames(df):
    '''https://stackoverflow.com/questions/24685012/pandas-dataframe-renaming-multiple-identically-named-columns'''

    cols = pd.Series(df.columns)
    for dup in df.columns[df.columns.duplicated(keep=False)]:
        cols[df.columns.get_loc(dup)] = ([dup + '_' + str(d_idx)
                                          if d_idx != 0
                                          else dup
                                          for d_idx in range(df.columns.get_loc(dup).sum())]
        )
    df.columns = cols
    return df