import sys

from mediascan.media_file_data import MediaFileData
from mediascan.media_files_yaml_file_loader import load_media_files_yaml_file


def list_artists(files: list[MediaFileData]):
    artists: set[str] = set()
    for f in files:
        artists.add(f.artist)
    for a in artists:
        print(a)


def main():
    if len(sys.argv) != 2:
        print("Usage: {0} <files yaml file>".format(sys.argv[0]))
    else:
        files_yaml_file = load_media_files_yaml_file(sys.argv[1])
        files = files_yaml_file.files
        list_artists(files)


if __name__ == "__main__":
    main()
