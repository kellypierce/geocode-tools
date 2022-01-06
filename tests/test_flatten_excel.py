import pandas as pd
import pytest
import os
from geocodetools.flatten_excel import collect_sheets


@pytest.fixture(params=[1, 2])
def test_sheets(request):

    base_dir = 'data'
    idx = request.param

    return {
        'flat': os.path.join(base_dir, f'flat_excel_{idx}.xlsx'),
        'multisheet': os.path.join(base_dir, f'multisheet_excel_{idx}.xlsx')
    }


class TestFlattenExcel:

    def test_collect_sheets(self, test_sheets):

        test = collect_sheets(test_sheets['multisheet'])
        target = pd.read_excel(test_sheets['flat'])
        print(test)
        print(target)

        pd.testing.assert_frame_equal(test.reset_index(drop=True), target.reset_index(drop=True))
