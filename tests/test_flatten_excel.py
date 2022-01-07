import pandas as pd
import pytest
import os
import json
import datetime
from geocodetools.flatten_excel import collect_sheets, clean_sheets
from geocodetools.utils import type_sanitizer


@pytest.fixture(params=[1, 2])
def test_sheets(request):

    base_dir = 'data'
    idx = request.param

    return {
        'flat': os.path.join(base_dir, f'flat_excel_{idx}.xlsx'),
        'multisheet': os.path.join(base_dir, f'multisheet_excel_{idx}.xlsx'),
        'flat_metadata': os.path.join(base_dir, f'flat_excel_{idx}.json'),
        'multisheet_metadata': os.path.join(base_dir, f'multisheet_excel_{idx}.json')
    }


@pytest.fixture(params=[1, 2])
def test_clean(request):
    base_dir = 'data'
    idx = request.param

    return {
        'human': os.path.join(base_dir, f'human_readable_{idx}.xlsx'),
        'machine': os.path.join(base_dir, f'machine_readable_{idx}.xlsx'),
        'human_metadata': os.path.join(base_dir, f'human_readable_{idx}.json'),
        'machine_metadata': os.path.join(base_dir, f'machine_readable_{idx}.json')
    }


class TestFlattenExcel:

    def test_collect_sheets(self, test_sheets):

        test = collect_sheets(sheet_path=test_sheets['multisheet'], metadata_path=test_sheets['multisheet_metadata'])
        target = pd.read_excel(test_sheets['flat'])

        assert test.shape == target.shape
        assert len(set(test.columns).difference(set(target.columns))) == 0

    def test_clean_sheets(self, test_clean):

        sheet_name = 'Sheet1'
        data = pd.read_excel(test_clean['human'], sheet_name=sheet_name)

        with open(test_clean['human_metadata'], 'r') as m:
            test_metadata = json.load(m)
        with open(test_clean['machine_metadata'], 'r') as m:
            target_metadata = json.load(m)

        test = clean_sheets(sheet_name=sheet_name, sheet=data, metadata=test_metadata)

        # apply same type sanitization to the target file (rather than using dtypes arg to read_excel)
        target = pd.read_excel(test_clean['machine'])
        for col in target:
            try:
                target_type = target_metadata[col]
            except KeyError:
                target_type = 'str'

            target[col] = type_sanitizer(target[col], target_type=target_type)

        pd.testing.assert_frame_equal(test.reset_index(drop=True), target.reset_index(drop=True), check_column_type=False)
