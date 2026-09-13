from pathlib import Path
import os

from scripts.copy_medialib import (
    copy_medialib,
    copy_medialibs,
    DirCopyMode,
)
from scripts.convert_covers import convert_medialibs_cover_images_inplace


def test_copy_covers(tmp_path: Path) -> None:
    src_path = tmp_path / "src"
    dst_path = tmp_path / "dst"
    copy_medialib(
        src_path,
        dst_path,
        include_filenames=["cover.jpg"],
        exclude_keywords=["Sepulga"],
        dry_run=True,
        ignore_existing=False,
        dir_copy_mode=DirCopyMode.PreserveStructure,
    )


def test_copy_all(tmp_path: Path):
    src_path1 = tmp_path / "src" / "lib1"
    src_path2 = tmp_path / "src" / "lib2"
    dst_path = tmp_path / "dst"
    copy_medialibs([src_path1, src_path2], dst_path)


def test_copy_medialib_does_not_overwrite_newer_destination(tmp_path: Path) -> None:
    src_path = tmp_path / "src"
    dst_path = tmp_path / "dst"
    src_path.mkdir()
    dst_path.mkdir()
    src_file = src_path / "cover.jpg"
    dst_file = dst_path / "cover.jpg"
    src_file.write_text("source")
    dst_file.write_text("newer destination")
    os.utime(src_file, (100, 100))
    os.utime(dst_file, (200, 200))

    count = copy_medialib(
        src_path,
        dst_path,
        include_filenames=["cover.jpg"],
        ignore_existing=False,
    )

    assert count == 0
    assert dst_file.read_text() == "newer destination"


def test_copy_medialib_overwrites_older_destination(tmp_path: Path) -> None:
    src_path = tmp_path / "src"
    dst_path = tmp_path / "dst"
    src_path.mkdir()
    dst_path.mkdir()
    src_file = src_path / "cover.jpg"
    dst_file = dst_path / "cover.jpg"
    src_file.write_text("source")
    dst_file.write_text("older destination")
    os.utime(src_file, (200, 200))
    os.utime(dst_file, (100, 100))

    count = copy_medialib(
        src_path,
        dst_path,
        include_filenames=["cover.jpg"],
        ignore_existing=False,
    )

    assert count == 1
    assert dst_file.read_text() == "source"


def test_convert_all(tmp_path: Path):
    src_path1 = tmp_path / "src" / "lib1"
    src_path2 = tmp_path / "src" / "lib2"
    convert_medialibs_cover_images_inplace([src_path1, src_path2])
