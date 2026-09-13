from pathlib import Path
from typing import cast

from .artist_yaml_file import ArtistYamlFile, ArtistYamlFileOldFmt


def load_artist_yaml_file(yaml_fname: str) -> ArtistYamlFile:
    """
    raises: FileNotFoundError, yaml.YAMLError
    """
    ret = None
    path = Path(yaml_fname)
    if not path.exists():
        raise FileNotFoundError(
            f"Moongas artist yaml file '{yaml_fname}' not found in current directory: {Path.cwd()}"
        )

    with open(path, "r") as stream:
        ret = cast(ArtistYamlFile, getattr(ArtistYamlFile, "from_yaml")(stream))
    return ret


def load_artist_yaml_file_old_fmt(yaml_fname: str) -> ArtistYamlFileOldFmt:
    """
    raises: yaml.YAMLError
    """
    """
    raises: FileNotFoundError, yaml.YAMLError
    """
    ret = None
    path = Path(yaml_fname)
    if not path.exists():
        raise FileNotFoundError(
            f"Moongas artist yaml file '{yaml_fname}' not found in current directory: {Path.cwd()}"
        )

    with open(path, "r") as stream:
        ret = cast(
            ArtistYamlFileOldFmt, getattr(ArtistYamlFileOldFmt, "from_yaml")(stream)
        )
    return ret
