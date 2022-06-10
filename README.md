# A delta of days

![https://xkcd.com/1883/](https://imgs.xkcd.com/comics/supervillain_plan.png)

## Description

We'd like to compute the number of days between two dates _from scratch_.
I.e. without importing or otherwise building on existing packages for date processing.

Despite the ominous XKCD comic above we don't need to worry about times or time zones for this problem.
Just the regular [calendar](https://en.wikipedia.org/wiki/Gregorian_calendar) and dates represented by strings of the form:
`YYYY-MM-DD`

For example, between `2012-01-01` and `2012-01-5` there are `3` days.

Note that start and end day should not be counted and we only care about the _absolute_ difference in dates.
If the order of two dates being compared is flipped the difference remains the same.

### Valid examples

`"2012-01-10"` <-> `"2012-01-11"` = `0` days

`"2012-01-01"` <-> `"2012-01-10"` = `8` days

`"1801-06-13"` <-> `"1801-11-11"` = `150` days

`"2021-12-01"` <-> `"2017-12-14"` = `1447` days

### Invalid examples

You should consider the possibility that malformed comparisons will be requested.
To simplify the problem we've constrained the definition of a calendar date to those which may be represented as: `YYYY-MM-DD`.

We leave it up-to you how these are handled or not by your application.

Examples of invalid dates:

- `"01-01-2020"`: not in the expected format..
- `"20000-01-01"`: invalid under our definition of allowed years (`YYYY`)..
- `"2022-02-29"`: format is not the only consideration for validity! 🤦‍♂️

## Solution shape

Construct an application that lets you answer a few arbitrary date comparison requests during the peer-review session.

For example, a command line application which takes two dates via stdin and returns the difference via stdout before exiting.

You're welcome to show off your skills by getting a little more fancy. Especially if you can demonstrate applicable technology and design choices relevant to your role.

A distributed machine learning solution running on the blockchain with virtual reality interface would be impressive; but overkill!



## Solution

## 🛠️ Requirements

- [Python ^3.8.0](https://www.python.org/downloads/release/python-380/)


## 🛠️ Getting Started

Installation

```zsh
❯ make install
```

To run the script

Input dates must be

- Gregorian date of format `(YYYY-MM-DD)`
- years must be of [astronomical year number](https://en.wikipedia.org/wiki/Astronomical_year_numbering) format which follows AD/CE format for years after year 1 BC/BCE where 1 BC==0. eg. 2 BC==−1. eg. 4713 BC (-4712) `-4712-01-01`
- no earlier than Mar 1st 4713 BC - `(-4712-03-01)`

```zsh
- after Mar 1st -

```zsh
❯ python datetime_delta.py -v DEBUG -d1 2020-02-28 -d2 2024-02-29

Calculating days between 2020-02-28 and 2024-02-29 CE/AD.
debug: 2020 is a leap year
debug: 2024 is a leap year
1461 days
```

To run tests


```zsh
❯ make test

or if you would like to customize test params
❯ python -m pytest tests/unit -vv -x -rs

```
