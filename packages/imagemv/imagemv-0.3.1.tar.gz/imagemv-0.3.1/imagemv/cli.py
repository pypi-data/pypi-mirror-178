# -*- coding: utf-8 -*-

"""imagemv

Usage:
  imagemv.py SOURCE DEST [--keep=<days>] [--dry-run]
  imagemv.py SOURCE DEST [--keep-all] [--dry-run]
  imagemv.py (-h | --help)
  imagemv.py (-v | --version)

Options:
  -h --help          Show this screen.
  -v --version       Show version.
  --verbose          Print more information about progress.
  --keep=<days>      Keep original files which are younger than the specified number of <days> old [default: 0].
  --keep-all         Keep all original files.
  --dry-run          Simulation mode (no changes will be written to the filesystem).
"""

from datetime import datetime, timedelta
from docopt import docopt
from imagemv.processstats import ProcessStats
import imagemv.datefunctions as datefunctions
import imagemv.fileinfo as fileinfo
import logging
import os
import shutil


logger = logging.getLogger("imagemv")

NOW = datetime.now()


def parse_arguments(arguments):
    source = arguments.get("SOURCE")
    destination = arguments.get("DEST")
    keep = -1 if arguments.get("--keep-all") else abs(int(arguments.get("--keep")))
    keep_td = None if keep < 0 else timedelta(days=keep)
    keep_all = keep == -1
    dry_run = arguments.get("--dry-run")
    return source, destination, keep_td, keep_all, dry_run


def process_dir(src_dir, dest_dir, keep_td, keep_all, dry_run):
    stats = ProcessStats(started_at=NOW)

    for root, dirs, files in os.walk(src_dir):
        for filename in files:
            path = os.path.join(root, filename)

            file_stats = process_file(path, dest_dir, keep_td, keep_all, dry_run)
            stats.files_processed += 1

            if file_stats.skip_reason:
                stats.skipped_files.append(file_stats)

            print(
                f"{file_stats.path} -> {f'skipped: {file_stats.skip_reason}' if file_stats.skip_reason else file_stats.target_path}"
            )

        # cleanup: remove all empty directories except source
        if not dry_run and root != src_dir:
            remove_empty_dirs(root)

    stats.finished_at = datetime.now()
    return stats


def process_file(src, dst_dir, keep_td, keep_all, dry_run):
    stats = fileinfo.analyze_file(src)
    filename = os.path.split(src)[-1]

    target_dir = os.path.join(dst_dir, datefunctions.get_dir_for_date(stats.created_at))
    stats.target_path = os.path.join(target_dir, filename)

    stats.skip_reason = fileinfo.find_skip_reason(stats.is_image, stats.target_path)
    if not stats.skip_reason and not dry_run:
        os.makedirs(target_dir, exist_ok=True)
        if keep_all or (keep_td is not None and keep_td >= NOW - stats.created_at):
            shutil.copy2(src, stats.target_path)
        else:
            shutil.move(src, stats.target_path)
    return stats


def remove_empty_dirs(root_dir):
    logger.debug(f'Removing empty directories in "{root_dir}" ...')
    try:
        os.removedirs(root_dir)
    except OSError:
        logger.debug(f'"{root_dir}" was not empty')


def print_stats(stats):
    out = (
        f"Number of files processed: {stats.files_processed}{os.linesep}"
        f"Files skipped: {len(stats.skipped_files)}{os.linesep}"
        f"Started at: {stats.started_at}{os.linesep}"
        f"Finished at: {stats.finished_at}{os.linesep}"
        f"Time elapsed: {(stats.finished_at - stats.started_at).total_seconds()} seconds{os.linesep}"
    )
    print()
    print(out)


def main(arguments=None):
    if not arguments:
        arguments = docopt(__doc__, version="imagemv 0.3.1")

    logging.basicConfig(
        level=logging.DEBUG if arguments.get("--verbose") else logging.INFO
    )
    logging.debug(f"arguments:{dict(arguments)}")

    source, destination, keep_td, keep_all, dry_run = parse_arguments(arguments)
    stats = process_dir(source, destination, keep_td, keep_all, dry_run)
    print_stats(stats)
