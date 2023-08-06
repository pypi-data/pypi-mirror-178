# -*- coding: utf-8 -*-

"""
imagemv.metadata

This module contains the parsing logic imagemv uses to find a file's creation
date and other metadata.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from hachoir.core import config as hachoirconfig
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from typing import Optional
import imagemv.fileinfo as fileinfo
import logging
import os

hachoirconfig.quiet = True


@dataclass
class FileMetadata:
    """Metadata of a file."""

    creation_date: Optional[datetime] = None
    mime_type: Optional[str] = None


def parse(file_path):
    result = FileMetadata()
    parser = createParser(file_path)
    if not parser:
        logging.error(f'Unable to parse file: "{file_path}"')
        return result
    with parser:
        try:
            metadata = extractMetadata(parser)
        except Exception as err:
            logging.error(f"Metadata extraction error: {err}")
            metadata = None
        if metadata:
            creation_dates = metadata.getValues("creation_date")
            if len(creation_dates) > 0:
                creation_date = creation_dates[0]
                # Dates of Quicktime videos are UTC, but do not use UTC format,
                # see https://github.com/vstinner/hachoir/issues/79
                if fileinfo.is_quicktime_video(parser.mime_type, parser.description):
                    creation_date = (
                        creation_date.replace(tzinfo=timezone.utc)
                        .astimezone()
                        .replace(tzinfo=None)
                    )
                    logging.debug(
                        f'Metadata date values appear to be UTC. Interpreting "{creation_dates[0]}" as "{creation_date}"'
                    )
                result.creation_date = creation_date
        result.mime_type = parser.mime_type
    return result
