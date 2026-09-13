from enum import Enum
from pathlib import Path
import argparse
import os
import shutil
from typing import NamedTuple

from mediascan.utils.log import log_arguments


class DirCopyMode(Enum):
    SingleDirectory = 1  #  All images copies to single destination directory, replacing filenames with 00001.jpg etc.
    PreserveStructure = 2  #  Preserve directory structure and filenames in destination


class CopyResults(NamedTuple):
    would_be_copied: int
    actually_copied: int
    skipped: int
    errors: int


@log_arguments
def copy_medialib(
    src_path: Path,
    dst_path: Path,
    include_filenames: list[str] = ["artist.yml", "cover.jpg"],
    exclude_keywords: list[str] = [],
    dry_run: bool = False,
    ignore_existing: bool = True,
    dir_copy_mode: DirCopyMode = DirCopyMode.PreserveStructure,
) -> CopyResults:
    """
    Recursively copy files (e.g. album cover images) from src medialib directory
    to specified destination directory, preserving directory structure (default)

    src_path : path e.g. '/data/Music'
    dst_path : path e.g. '/data/Covers/Music'

    Dir Copy Modes:
        1. SingleDirectory
            All images copies to single destination directory, replacing filenames with 00001.jpg etc.
        2. PreserveStructure
            Preserve directory structure and filenames in destination

    Returns number it copied (or would have copied if not dry_run)
    """
    ret = CopyResults(
        would_be_copied=0,
        actually_copied=0,
        skipped=0,
        errors=0,
    )
    if not dry_run:
        Path(dst_path).mkdir(parents=True, exist_ok=True)

    # first make the directories
    if dir_copy_mode == DirCopyMode.PreserveStructure:
        for root, dirs, files in os.walk(src_path, topdown=False):
            for sd in dirs:
                src_dir_abs_path = Path(root).joinpath(sd)
                src_dir_rel_path = src_dir_abs_path.relative_to(src_path)
                dst_abs_path = Path(dst_path).joinpath(src_dir_rel_path)
                if not dry_run:
                    dst_abs_path.mkdir(parents=True, exist_ok=True)

    for root, dirs, files in os.walk(src_path, topdown=False):
        for src_fname in files:
            # skip any files not specifically included
            if src_fname not in include_filenames:
                ret = ret._replace(skipped=ret.skipped + 1)
                continue
            # skip files with any exclude keywords anywhere in the file path
            src_file_abs_path = Path(root).joinpath(src_fname)
            skip = False
            for keyword in exclude_keywords:
                if str(src_file_abs_path).find(keyword) != -1:
                    print(
                        f"Skipping file '{src_file_abs_path}' based on exclude keyword '{keyword}'"
                    )
                    skip = True
            if skip:
                ret = ret._replace(skipped=ret.skipped + 1)
                continue
            _, src_ext = os.path.splitext(src_fname)

            src_file_rel_path = src_file_abs_path.relative_to(src_path)
            dst_abs_path = Path(dst_path)
            if dir_copy_mode == DirCopyMode.SingleDirectory:
                # This mode is for creating flat dir full of images, etc.
                # so we need to make the filenames unique
                dst_fname: str = str(ret.would_be_copied + 1).rjust(5, "0") + src_ext
                dst_abs_path = dst_abs_path.joinpath(dst_fname)
            elif dir_copy_mode == DirCopyMode.PreserveStructure:
                # This mode retains the original filename exactly
                dst_abs_path = dst_abs_path.joinpath(src_file_rel_path)

            # Never replace a destination file that is newer than the source.
            if (
                dst_abs_path.exists()
                and dst_abs_path.stat().st_mtime > src_file_abs_path.stat().st_mtime
            ):
                ret = ret._replace(skipped=ret.skipped + 1)
                continue

            # Don't copy if it exists unless ignore_existing==False
            if not ignore_existing or not dst_abs_path.exists():
                # Special case:
                # If copying a .jpg file and .webp file already exists in destination,
                # skip the copy unless ignore_existing==False
                # (I copy jpegs first and then convert them to webp in place,
                # consequently I want to skip copying jpegs that have already been
                # converted)
                if src_ext == ".jpg":
                    dst_fbase, _ = os.path.splitext(dst_abs_path)
                    dst_abs_path_converted = Path(dst_fbase + ".webp")
                    if dst_abs_path_converted.exists() and ignore_existing:
                        ret = ret._replace(skipped=ret.skipped + 1)
                        continue

                if not dry_run:
                    shutil.copy(src_file_abs_path, dst_abs_path)
                    ret = ret._replace(actually_copied=ret.actually_copied + 1)
                ret = ret._replace(would_be_copied=ret.would_be_copied + 1)
            else:
                ret = ret._replace(skipped=ret.skipped + 1)
    return ret


@log_arguments
def copy_medialibs(
    src_paths: list[Path],
    dst_root_path: Path,
    include_filenames: list[str] = ["artist.yml", "cover.jpg"],
    exclude_keywords: list[str] = [],
    dry_run: bool = False,
    ignore_existing: bool = True,
    dir_copy_mode: DirCopyMode = DirCopyMode.PreserveStructure,
) -> CopyResults:
    """
    Copies files* from one or more medialib directories from src directory to
    medialib directories inside the specified root destination directory

    *Which files are copied is determined by the arguments. The idea is to only copy
    specified files and ignore everything else.

    src_paths : paths to one or more media library directories to be copied from
    E.g. /data/Music and /data/OtherMusic

    dst_root_path : path to root destination directory medialibs will be copied into
    E.g. /data/Covers

    Complete example:
    Given the following arguments:
        - src_paths = ['/data/Music', '/data/OtherMusic']
        - dst_root_path = '/data/Covers'
    Then the following destination subdirectories would be created inside /data/Covers:
        - /data/Covers/Music
        - /data/Covers/OtherMusic
    """
    ret = CopyResults(
        would_be_copied=0,
        actually_copied=0,
        skipped=0,
        errors=0,
    )
    for src_path in src_paths:
        ret_tmp: CopyResults = copy_medialib(
            src_path=src_path,
            dst_path=dst_root_path.joinpath(src_path.name),
            include_filenames=include_filenames,
            dir_copy_mode=dir_copy_mode,
            exclude_keywords=exclude_keywords,
            dry_run=dry_run,
            ignore_existing=ignore_existing,
        )
        print(
            f"Total copied for medialib dir {src_path}: would be copied: {ret_tmp.would_be_copied}; actually copied: {ret_tmp.actually_copied}; skipped: {ret_tmp.skipped}; errors: {ret_tmp.errors};"
        )
        ret = ret._replace(
            would_be_copied=ret.would_be_copied + ret_tmp.would_be_copied,
            actually_copied=ret.actually_copied + ret_tmp.actually_copied,
            skipped=ret.skipped + ret_tmp.skipped,
            errors=ret.errors + ret_tmp.errors,
        )
    print(
        f"Grand total copied for all medialib dirs: would be copied: {ret.would_be_copied}; actually copied: {ret.actually_copied}; skipped: {ret.skipped}; errors: {ret.errors}"
    )
    return ret


def copy_covers():
    copy_medialibs(
        src_paths=[Path("/data/Music"), Path("/data/MusicOther")],
        dst_root_path=Path("/data/Covers"),
        include_filenames=["cover.jpg"],
        exclude_keywords=[],
        dry_run=False,
        ignore_existing=True,
        dir_copy_mode=DirCopyMode.PreserveStructure,
    )


def copy_artist_yaml():
    copy_medialibs(
        src_paths=[Path("/data/Music"), Path("/data/MusicOther")],
        dst_root_path=Path("/home/brett/Git/bretttolbert/moongas/moongas-library"),
        include_filenames=["cover.jpg"],
        exclude_keywords=[],
        dry_run=False,
        ignore_existing=True,
        dir_copy_mode=DirCopyMode.PreserveStructure,
    )


def parse_args():
    parser = argparse.ArgumentParser(
        description="Copy media library files maintaining structure or target criteria."
    )

    parser.add_argument(
        "-s",
        "--src-paths",
        type=Path,
        nargs="+",
        default=[Path("/data/Music"), Path("/data/MusicOther")],
        help="One or more source directory paths.",
    )
    parser.add_argument(
        "-d", "--dst-path", type=Path, required=True, help="Destination directory path."
    )
    parser.add_argument(
        "-i",
        "--include-filenames",
        nargs="+",
        default=["cover.jpg"],
        help="Filename patterns to include (e.g., cover.jpg artist.yml).",
    )
    parser.add_argument(
        "-e",
        "--exclude-keywords",
        nargs="*",
        default=[],
        help="Keywords to exclude from file paths.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a trial run without making actual file changes.",
    )
    parser.add_argument(
        "--overwrite-existing",
        dest="ignore_existing",
        action="store_false",
        default=True,
        help="Overwrite existing destination files (if newer in source) (default: skip existing).",
    )
    parser.add_argument(
        "--dir-copy-mode",
        type=lambda mode: DirCopyMode[mode],
        choices=list(DirCopyMode),
        default=DirCopyMode.PreserveStructure,
        help="Directory structure copy mode.",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    copy_medialibs(
        src_paths=args.src_paths,
        dst_root_path=args.dst_path,
        include_filenames=args.include_filenames,
        exclude_keywords=args.exclude_keywords,
        dry_run=args.dry_run,
        ignore_existing=args.ignore_existing,
        dir_copy_mode=args.dir_copy_mode,
    )


if __name__ == "__main__":
    main()
