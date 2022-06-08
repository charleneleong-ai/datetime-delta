#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import pytest

from click.testing import CliRunner

runner = CliRunner()

from datetime_delta import main


@pytest.mark.parametrize(
    ["date1", "date2", "expected_days"],
    [
        ("2012-01-10", "2012-01-11", 0),
        ("2012-01-01", "2012-01-10", 8),
        ("1801-06-13", "1801-11-11", 150),
        ("2021-12-01", "2017-12-14", 1447),
    ],
)
def test_main(date1, date2, expected_days):

    assert main(date1=date1, date2=date2) == expected_days
