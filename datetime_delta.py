#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
from typing import Union, Tuple, List

import click
import click_log
from pathlib import Path
import json
import re

BASE_DIR = Path(__file__).resolve().parent.parent

click_log.basic_config()
logger = logging.getLogger(__name__)

# ==================================================
# =============== MAIN =============================
# ==================================================
@click.command()
@click_log.simple_verbosity_option()
@click.option("--date1", "-d1", help="Date of format `YYYY-MM-DD`", type=str)
@click.option("--date2", "-d2", help="Date of format `YYYY-MM-DD`", type=str)
def cli(date1: str, date2: str):
    return main(date1=date1, date2=date2)


def main(date1: str, date2: str):
    logger.info(f"Calculating days between {date1} and {date2} CE/AD.")

    if is_valid_date_format(date1) and is_valid_date_format(date2):
        y1, m1, d1 = map(int, split_date(date1))
        y2, m2, d2 = map(int, split_date(date2))

        if is_within_date_limit(y1, m1, d1):
            print(gregorian_to_jdn(y1, m1, d1))
            print(gregorian_to_jdn(y2, m2, d2))
            days_diff = (
                abs(gregorian_to_jdn(y1, m1, d1) - gregorian_to_jdn(y2, m2, d2)) - 1
            )
            if date1 == date2:
                days_diff = 0

            logging.info(f"{days_diff} days")

            # ## Short test ##
            # from datetime import datetime

            # date1_dt = datetime(y1, m1, d1)
            # date2_dt = datetime(y2, m2, d2)
            # days_diff_dt = abs((date1_dt - date2_dt).days)-1
            # if date1_dt == date2_dt:
            #     days_diff_dt = 0

            # logging.info(days_diff_dt)
            # assert days_diff == days_diff_dt

            return days_diff
    return None


# ==================================================
# ============= Helper functions ===================
# ==================================================


def is_valid_date_format(date_str: str):
    """Validate date is of valid format YYYY-MM-DD"""
    if is_valid_date_regex(date_str):
        if is_valid_date(date_str):
            return date_str
        else:
            err = f"{date_str} is an invalid date."
            logger.error(f"{err}")
            raise ValueError(f"{err}")
    else:
        err = (
            f"{date_str} is an invalid date format. Please enter in format YYYY-MM-DD."
        )
        logger.error(f"{err}")
        raise ValueError(f"{err}")


def is_valid_date(date_str: str):
    """Check for date interval and leap years"""
    y, m, d = map(int, split_date(date_str))
    days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if is_leap_year(y):
        logger.debug(f"{y} is a leap year")
        days_in_month[2] = 29

    if not (1 <= m <= 12):
        logger.error(f"{m} is not in the correct range of 1-12.")
        return False
    if not (1 <= d <= days_in_month[m]):
        logger.error(
            f"{d} is not in the correct range of 1-{days_in_month[m]} for month {m} in year {y}."
        )
        return False
    return True


def is_leap_year(year: int):
    return (year % 4 == 0) and (year % 100 != 0 or year % 400 == 0)


def is_valid_date_regex(date_str: str):
    date_regex = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$"
    return bool(re.search(date_regex, date_str))


def split_date(date_str: str, delimiter: str = "-"):
    """To handle negative dates in astronomical year format"""
    date_list = date_str.split(delimiter)
    if date_list[0] == "":
        date_list[1] = f"-{date_list[1]}"
        date_list = date_list[1:]
        assert len(date_list) == 3
    return date_list


def is_within_date_limit(year: int, month: int, day: int):
    """Gregorian to JDN formula date limit is after Mar 1st -4712 AD (-4712-03-01)"""
    ## If date > Mar 1st -4712 Gregorian, Julian day num 98
    date_limit_str = "-4712-03-01"
    y, m, d = map(int, split_date(date_limit_str))

    date_limit = gregorian_to_jdn(y, m, d)
    if gregorian_to_jdn(year, month, day) < date_limit:
        err = (
            f"Gregorian date {year}-{month}-{day} is before formula limit {date_limit}"
        )
        logger.error(err)
        raise ValueError(err)
    return True


def gregorian_to_jdn(year: int, month: int, day: int) -> int:
    """Converting Gregorian date to Julian day number
    - January 1, 4713 BC in the proleptic Julian calendar at 12:00 PM (noon) in UTC
    - November 24, 4714 BC in the proleptic Gregorian calendar at 00:00 in UTC
    Julian days are counted as integers continuously until the present time.
    To compute calendar date -> jdn:
    1. Find # days in whole years of the current Julian period
    2. Find # days in completed months
    3. Add numbers together, and add day of month

    Ref: https://articles.adsabs.harvard.edu//full/1984QJRAS..25...53H/0000053.000.html
        Title: Simple Formulae for Julian Day Numbers and Calendar Dates
        Authors: Hatcher, D. A.
        Journal: Quarterly Journal of the Royal Astronomical Society, Vol. 25, NO.1, P. 53, 1984
    """
    A = year
    M = month
    D = day
    A_ = A - (12 - M) // 10
    M_ = (M - 3) % 12

    y = int(365.25 * (A_ + 4712))
    d = int(30.6 * M_ + 0.5)
    N = y + d + D + 59

    ## If date > Mar 1st -4712 Julian, jdn 60,
    ## If date > Mar 1st -4712 Gregorian, jdn 98
    g = int((int(A_ / 100) + 49) * 0.75) - 38
    jdn = N - g

    return jdn


if __name__ == "__main__":
    cli()
