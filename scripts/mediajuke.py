import random
import subprocess
import sys

from mediascan.media_files_yaml_file_loader import load_media_files_yaml_file

"""
mediajuke.py
Reads yaml file output by mediascan and plays a random file
"""


def main():
    if len(sys.argv) != 3:
        print("Usage: {0} <player cmd> <files yaml file>".format(sys.argv[0]))
    else:
        player_cmd = sys.argv[1]
        file_yaml_path = sys.argv[2]
        files = load_media_files_yaml_file(file_yaml_path)
        file = random.choice(files.files)
        subprocess.run([player_cmd, file.path], check=False)


if __name__ == "__main__":
    main()
