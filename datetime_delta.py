#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#####

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
def main(date1: str, date2: str):
    logger.info(f"Calculating days between - {date1} and {date2} CE/AD.")

    if is_valid_date_format(date1) and is_valid_date_format(date2):
        y1, m1, d1 = map(int, date1.split("-"))
        y2, m2, d2 = map(int, date2.split("-"))

        days_diff = abs(gregorian_to_jdn(y1, m1, d1) - gregorian_to_jdn(y2, m2, d2)) - 1
        if date1 == date2:
            days_diff = 0

        logger.info(f"{days_diff} days")


# ==================================================
# ============= Helper functions ===================
# ==================================================


def gregorian_to_jdn(year: int, month: int, day: int) -> int:
    """Converting date to Julian day number
    - January 1, 4713 BC in the proleptic Julian calendar at 12:00 PM (noon) in UTC
    - November 24, 4714 BC in the proleptic Gregorian calendar at 00:00 in UTC
    Julian days are counted as integers continuously until the present time.
    This makes it very easy to compare relative times of events and do arithmetic between days.
    Ref: https://orbital-mechanics.space/reference/julian-date.html
    """
    A = (month - 14) // 12
    B = 1461 * (year + 4800 + A)
    C = 367 * (month - 2 - (12 * A))
    E = (year + 4900 + A) // 100

    jdn = B // 4 + C // 12 - (3 * E) // 4 + day - 32075
    return jdn


def is_valid_date_format(date_str: str):
    """Validate date is of valid format YYYY-MM-DD"""
    ## Basic regex check
    date_regex = "^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$"
    if bool(re.search(date_regex, date_str)):
        if is_valid_date(date_str):
            return date_str
        else:
            err = f"{date_str} is an invalid date."
            logger.error(f"{err}")
            raise ValueError(f"{err}")
    else:
        err = f"{date_str} is an invalid date format. Please enter in format YYYY-MM-DD"
        logger.error(f"{err}")
        raise ValueError(f"{err}")


def is_valid_date(date_str: str):
    """Check for date interval and leap years"""
    y, m, d = map(int, date_str.split("-"))
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if (y % 4 == 0) and (y % 400 == 0 or y % 100 != 0):
        logger.debug(f"{y} is a leap year")
        days_in_month[1] = 29
    return 0 <= y and 0 <= m - 1 <= 11 and 0 <= d <= days_in_month[m - 1]


if __name__ == "__main__":
    main()
