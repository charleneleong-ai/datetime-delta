#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import pytest


from datetime_delta import (
    main,
    is_valid_date_format,
    is_valid_date,
    is_leap_year,
    is_valid_date_regex,
    is_within_date_limit,
    gregorian_to_jdn,
)


@pytest.mark.parametrize(
    ["date1", "date2", "expected_days"],
    [
        ("2012-01-10", "2012-01-10", 0),  ## Same date should return 0
        ("2012-01-10", "2012-01-11", 0),  ## One day difference should return 0
        ("2012-01-01", "2012-01-10", 8),
        ("2020-01-01", "2020-02-29", 58),  ## Leap year
        ("1801-06-13", "1801-11-11", 150),
    ],
    ids=[
        "same_date",
        "1_day_diff",
        "10_day_diff",
        "leap_year_date",
        "1801_date",
    ],
)
def test_main_success(date1, date2, expected_days):

    assert main(date1=date1, date2=date2, format1="CE", format2="CE") == expected_days


@pytest.mark.parametrize(
    ["date1", "date2", "expected"],
    [
        ("2012-1-01", "2012-01-05", ValueError),
        ("2012-01-01", "2012-01-5", ValueError),
        ("2020-01-01", "2019-02-29", ValueError),
        ("2020-01-01", "2019-02-30", ValueError),
        ("1500-01-01", "2019-02-30", ValueError),
    ],
    ids=[
        "invalid_date_format YYYY-M-DD",
        "invalid_date_format YYYY-MM-D",
        "non_leap_year_29",
        "feb_30_date",
        "pre_gregorian_1582-10-15_date",
    ],
)
def test_main_fail(date1, date2, expected):
    with pytest.raises(expected) as e_info:
        print(e_info)
        main(date1=date1, date2=date2, format1="CE", format2="CE")


@pytest.mark.parametrize(
    ["date_str", "expected"],
    [
        ("2000-01-01", "2000-01-01"),
        ("1585-01-01", "1585-01-01"),
    ],
    ids=["valid_date_format 2000-01-01", "valid_date_format 1585-01-01"],
)
def test_is_valid_date_format_success(date_str, expected):
    assert is_valid_date_format(date_str) == expected


@pytest.mark.parametrize(
    ["date_str", "expected"],
    [
        ("2000-02-30", ValueError),
        ("20000-02-30", ValueError),
    ],
    ids=["invalid_date_format 2000-02-30", "invalid_date_format 20000-02-30"],
)
def test_is_valid_date_format_fail(date_str, expected):
    with pytest.raises(expected) as e_info:
        print(e_info)
        is_valid_date_format(date_str)


@pytest.mark.parametrize(
    ["date_str", "expected"],
    [
        ("2000-01-01", True),
        ("1585-01-01", True),
        ("1585-13-01", False),
        ("2017-02-29", False),
        ("2017-04-31", False),
    ],
    ids=[
        "valid_date 2000-01-01",
        "valid_date 1585-01-01",
        "invalid_date 1585-13-01",
        "invalid_date 2017-02-29",
        "invalid_date 2017-04-31",
    ],
)
def test_is_valid_date(date_str, expected):
    assert is_valid_date(date_str) == expected


@pytest.mark.parametrize(
    ["year", "expected"],
    [
        (2024, True),
        (2000, True),
        (2200, False),
        (1900, False),
        (2019, False),
    ],
    ids=[
        "valid_leap_year 2024",
        "valid_leap_year 2000",
        "invalid_leap_year 2200",
        "invalid_leap_year 1900",
        "invalid_leap_year 2019",
    ],
)
def test_is_leap_year(year, expected):
    assert is_leap_year(year) == expected


@pytest.mark.parametrize(
    ["date_str", "expected"],
    [
        ("2000-01-01", True),
        ("20000-01-01", False),
        ("1985-06-100", False),
        ("1985-6-10", False),
    ],
    ids=[
        "valid_date_regex 2000-01-01",
        "invalid_date_regex 20000-1-01",
        "invalid_date_regex 1985-06-100",
        "invalid_date_regex 1985-6-10",
    ],
)
def test_is_valid_date_regex(date_str, expected):
    assert is_valid_date_regex(date_str) == expected


@pytest.mark.parametrize(
    ["year", "month", "day", "expected"],
    [(2000, 1, 1, True)],
    ids=["valid_date_limit 2000-01-01"],
)
def test_is_within_date_limit_success(year, month, day, expected):
    assert is_within_date_limit(year, month, day) == expected


@pytest.mark.parametrize(
    ["year", "month", "day", "expected"],
    [
        (-4713, 1, 1, ValueError),
        (-4720, 10, 14, ValueError),
    ],
    ids=["invalid_date_limit 1500-01-01", "invalid_date_limit 1582-10-14"],
)
def test_is_within_date_limit_fail(year, month, day, expected):
    with pytest.raises(expected) as e_info:
        print(e_info)
        is_within_date_limit(year, month, day)


@pytest.mark.parametrize(
    ["year", "month", "day", "expected"],
    [
        (2020, 2, 28, 2458908),
        (2024, 2, 29, 2460370),
    ],
    ids=["valid_gregorian_to_jdn 2020-02-28", "valid_gregorian_to_jdn 2024-02-29"],
)
def test_gregorian_to_jdn(year, month, day, expected):
    assert gregorian_to_jdn(year, month, day) == expected
