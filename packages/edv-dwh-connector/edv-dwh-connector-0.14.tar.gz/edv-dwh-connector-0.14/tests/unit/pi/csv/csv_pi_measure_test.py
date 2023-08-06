"""
Test case for PI measures based on CSV files.
.. since: 0.13
"""

# -*- coding: utf-8 -*-
# Copyright (c) 2022 Endeavour Mining
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to read
# the Software only. Permissions is hereby NOT GRANTED to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import os
import shutil
from datetime import datetime
from tempfile import TemporaryDirectory

from hamcrest import assert_that, equal_to

from edv_dwh_connector.pi.cached.cached_pi_tag import CachedPITag
from edv_dwh_connector.pi.csv.csv_pi_measure import CsvWithLatestPIMeasuresDf
from edv_dwh_connector.pi.pi_measure import PIMeasuresDf
from tests.fake_pi_measure import FakePIMeasures, FakePIMeasuresDf


def test_updates_csv_file(resource_path_root) -> None:
    """
    Test that updates CSV files.
    :param resource_path_root: Resource path
    """
    tag = CachedPITag(
        uid=1, code="AI162003_SCLD",
        name="AI162003 CIL Free Cyanide Analyser "
             "pH Indicator Tank 1 Scaled Value",
        uom="pH",
        web_id="F1DPmN2MpX8PREOtdbEZ56sypAQw"
               "IAAASVRZLVNSVi1QSS1ISTAxXEFJMTYwMDE0QV9TQ0xE"
    )
    with TemporaryDirectory() as tmp:
        csv_file = resource_path_root / f'{tag.code()}.csv'
        tmp_file = os.path.join(tmp, f'{tag.code()}.csv')
        shutil.copy(csv_file, tmp_file)
        size = PIMeasuresDf.load(tmp_file, tag.code()).shape[0]
        measures = FakePIMeasures(tag)
        dte = datetime(2022, 6, 21, 15, 0, 0)
        measures.add(dte, 10.1)
        dtf = CsvWithLatestPIMeasuresDf(
            tmp_file, tag, FakePIMeasuresDf(measures)
        ).frame(
            datetime(2022, 6, 19), datetime(2022, 6, 22)
        )
        assert_that(
            dtf.to_dict(), equal_to(
                PIMeasuresDf.load(tmp_file, tag.code()).to_dict()
            ),
            "Should be updated"
        )
        assert_that(
            dtf.shape[0], equal_to(size + 1),
            "Should only add one measure"
        )


def test_no_need_to_update_csv_file(resource_path_root) -> None:
    """
    Test that no need to update CSV file.
    :param resource_path_root: Resource path
    """
    tag = CachedPITag(
        uid=1, code="AI162003_SCLD",
        name="AI162003 CIL Free Cyanide Analyser "
             "pH Indicator Tank 1 Scaled Value",
        uom="pH",
        web_id="F1DPmN2MpX8PREOtdbEZ56sypAQw"
               "IAAASVRZLVNSVi1QSS1ISTAxXEFJMTYwMDE0QV9TQ0xE"
    )
    with TemporaryDirectory() as tmp:
        csv_file = resource_path_root / f'{tag.code()}.csv'
        tmp_file = os.path.join(tmp, f'{tag.code()}.csv')
        shutil.copy(csv_file, tmp_file)
        size = PIMeasuresDf.load(tmp_file, tag.code()).shape[0]
        measures = FakePIMeasures(tag)
        measures.add(datetime(2022, 6, 21, 15, 0, 0), 10.1)
        dtf = CsvWithLatestPIMeasuresDf(
            tmp_file, tag, FakePIMeasuresDf(measures)
        ).frame(
            datetime(2022, 6, 19), datetime(2022, 6, 20)
        )
        assert_that(
            dtf.to_dict(), equal_to(
                PIMeasuresDf.load(csv_file, tag.code()).to_dict()
            ),
            "Should not be updated"
        )
        assert_that(
            dtf.shape[0], equal_to(size),
            "Should only add one measure"
        )
