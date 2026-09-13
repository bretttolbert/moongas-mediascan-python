from pathlib import Path

from .artists_yaml_file import ArtistsYamlFile


def load_artists_yaml_file(path: Path) -> ArtistsYamlFile:
    """
    DEPRECATED (only used by deprecated artists.yml)
    raises: yaml.YAMLError
    """
    files = None
    with open(path, "r") as stream:
        files = ArtistsYamlFile.from_yaml(stream)  # type: ignore
    return files  # type: ignore
