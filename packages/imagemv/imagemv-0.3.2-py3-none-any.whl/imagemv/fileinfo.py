# -*- coding: utf-8 -*-

"""
imagemv.fileinfo

This module contains logic to find information about a file such as metadata,
its MIME type or whether the file exists.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import imagemv.datefunctions as datefunctions
import imagemv.metadata as metadata
import os


@dataclass
class FileInfo:
    """Class for keeping track of the properties of an analyzed file."""

    is_image: bool = False
    metadata_date: Optional[datetime] = None
    filename_date: Optional[datetime] = None
    mtime_date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    skip_reason: Optional[str] = None
    path: Optional[str] = None
    target_path: Optional[str] = None


def analyze_file(path):
    stats = FileInfo()
    stats.path = path
    md = metadata.parse(path)

    stats.metadata_date = md.creation_date
    stats.filename_date = datefunctions.guess_date(os.path.split(path)[1])
    stats.mtime_date = datetime.fromtimestamp(os.stat(path).st_mtime)
    
    stats.is_image = is_image(md.mime_type)

    stats.created_at = stats.metadata_date or stats.filename_date or stats.mtime_date
    return stats


def find_skip_reason(is_image, target_path):
    if not is_image:
        return "not an image"
    if os.path.isfile(target_path):
        return "file already exists at destination"
    # TODO skip if filename_date and metadata_date are out of sync
    return None


def is_image(mime_type):
    return is_photo(mime_type) or is_video(mime_type)


def is_photo(mime_type):
    return mime_type is not None and mime_type.startswith("image")


def is_video(mime_type):
    return mime_type is not None and mime_type.startswith("video")


def is_quicktime_video(mime_type, description):
    if not description:
        return False
    return is_image(mime_type) and "quicktime" in description.lower()
