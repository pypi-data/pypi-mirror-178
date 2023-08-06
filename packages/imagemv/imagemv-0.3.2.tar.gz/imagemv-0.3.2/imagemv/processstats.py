# -*- coding: utf-8 -*-

"""
imagemv.processstats

This module contains the ProcessStats data structure.
"""

from dataclasses import dataclass, field
from imagemv.fileinfo import FileInfo
from enum import Enum
from typing import Optional, List
from datetime import datetime, timedelta


@dataclass
class ProcessStats:
    """A process run's statistics."""

    started_at: datetime
    skipped_files: List[FileInfo] = field(default_factory=lambda: [])
    finished_at: Optional[datetime] = None
    files_processed: int = 0
