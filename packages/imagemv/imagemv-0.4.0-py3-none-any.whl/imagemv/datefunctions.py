# -*- coding: utf-8 -*-

"""
imagemv.datefunctions

This module contains the date- and time-related logic imagemv uses to find a
date within a filename (or string in general).
"""

from datetime import datetime
import os
import re

"""
Date and time patterns commonly found in image files

- Date: `YYYYMMDD` unseparated or separated by `-`
- Time: `HHMMSS` unseparated or separated by `:` or `-`

The patterns are usually surrounded by non-numeric characters
"""
DATE_PATTERN = re.compile(
    r"[^\d-](?P<year>[\d]{4})(|-)(?P<month>[01]\d)(|-)(?P<day>[0123]\d)[^d-]"
)
TIME_PATTERN = re.compile(
    r"[^\d:-](?P<hour>[012]\d)(|:|-)(?P<minute>[012345]\d)(|:|-)(?P<second>[012345]\d)[^\d:-]"
)


def find_skip_reason(file_stats):
    if not file_stats.is_image:
        return "not an image"
    if os.path.isfile(file_stats.target_path):
        return "file already exists at destination"
    return None


def guess_date(s):
    date_matches = DATE_PATTERN.search(s)
    if date_matches:
        year = date_matches.group("year")
        month = date_matches.group("month")
        day = date_matches.group("day")
        time_matches = TIME_PATTERN.search(s)
        if time_matches:
            hour = time_matches.group("hour")
            minute = time_matches.group("minute")
            second = time_matches.group("second")
            return datetime(
                int(year), int(month), int(day), int(hour), int(minute), int(second)
            )
        return datetime(int(year), int(month), int(day))
    return None


def get_dir_for_date(dt):
    return os.path.join(f"{dt:%Y}", f"{dt:%m}", f"{dt:%d}")
