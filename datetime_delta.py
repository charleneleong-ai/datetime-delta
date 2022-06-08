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
        y1, m1, d1 = map(int, date1.split("-"))
        y2, m2, d2 = map(int, date2.split("-"))

        days_diff = abs(gregorian_to_jdn(y1, m1, d1) - gregorian_to_jdn(y2, m2, d2)) - 1
        if date1 == date2:
            days_diff = 0

        logger.info(f"{days_diff} days")
        return days_diff
    return None


# ==================================================
# ============= Helper functions ===================
# ==================================================


def gregorian_to_jdn(year: int, month: int, day: int) -> int:
    """Converting date to Julian day number
    - January 1, 4713 BC in the proleptic Julian calendar at 12:00 PM (noon) in UTC
    - November 24, 4714 BC in the proleptic Gregorian calendar at 00:00 in UTC
    Julian days are counted as integers continuously until the present time.
    This makes it very easy to compare relative times of events and do arithmetic between days.
    Ref: https://quasar.as.utexas.edu/BillInfo/JulianDatesG.html
    """
    A = year // 100
    B = A // 4
    C = 2 - A + B
    E = 365.25 * (year + 4716)
    F = 30.6001 * (month + 1)
    jdn = int(C + day + E + F - 1524.5)

    return jdn


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
    y, m, d = map(int, date_str.split("-"))
    days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if (y % 4 == 0) and (y % 400 == 0 or y % 100 != 0):
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


def is_valid_date_regex(date_str: str):
    date_regex = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$"
    return bool(re.search(date_regex, date_str))


if __name__ == "__main__":
    cli()
