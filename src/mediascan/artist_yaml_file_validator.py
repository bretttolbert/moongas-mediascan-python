from pathlib import Path

import yaml

from mediascan.artist_yaml_file_loader import load_artist_yaml_file


def validate_artist_yaml_content(content: str) -> None:
    """Validate that generated artist YAML content is valid YAML."""
    yaml.safe_load(content)


def validate_artist_yaml_file(
    artist: str,
    artist_path: Path,
    artist_yaml_paths: list[str],
    artists_missing: list[str],
    exceptions: list[tuple[Path, Exception]],
) -> None:
    """Check an artist YAML file and record missing or invalid files."""
    artist_yaml_path = artist_path / "artist.yml"
    if not artist_yaml_path.exists():
        print(f"{artist_path} missing artist.yml")
        artists_missing.append(artist)
        return

    try:
        artist_yaml_paths.remove(str(artist_yaml_path))
    except Exception as ex:
        print(f"path exists but isn't in the list, how?? '{artist_yaml_path}'")
        exceptions.append((artist_yaml_path, ex))

    try:
        adf = load_artist_yaml_file(artist_yaml_path)
        if adf.artist_data.country_code.upper() == "UK":
            raise Exception(
                "invalid countryCode 'UK' (United Kingdom country code should be 'GB', per ISO standard)"
            )
        if adf.artist_data.country_code.upper() == "EL":
            raise Exception(
                "invalid countryCode 'EL' (Greece country code should be 'GR', per ISO standard)"
            )
        if len(adf.artist_data.region_code) and "-" not in adf.artist_data.region_code:
            raise Exception(
                f"invalid regionCode '{adf.artist_data.region_code}' (missing hyphen)"
            )
        if adf.artist_data.country_code != adf.artist_data.country_code.upper():
            raise Exception("invalid countryCode (lowercase letters are not allowed")
        if adf.artist_data.region_code != adf.artist_data.region_code.upper():
            raise Exception("invalid regionCode (lowercase letters are not allowed")
        for language_code in adf.artist_data.language_codes:
            if language_code != language_code.lower():
                raise Exception(
                    "invalid languageCode (uppercase letters are not allowed)"
                )
        if adf.artist_data.country_code == "":
            raise Exception("invalid countryCode (must not be empty)")
        if (
            adf.artist_data.city == "Birmingham"
            and adf.artist_data.country_code == "GB"
            and adf.artist_data.region_code != "GB-WMD"
        ):
            raise Exception(
                "The correct region code for Birmingham, UK is GB-WMD (West Midlands)"
            )
        if (
            adf.artist_data.city == "Manchester"
            and adf.artist_data.country_code == "GB"
            and adf.artist_data.region_code != "GB-NWK"
        ):
            raise Exception(
                "The correct region code for Manchester, UK is GB-NWK (North West England)"
            )
        if adf.artist_data.region_code == "GB-HER":
            raise Exception(
                "The correct region code for Herefordshire, UK is GB-WMD (West Midlands)"
            )
    except Exception as ex:
        artists_missing.append(artist)
        exceptions.append((artist_yaml_path, ex))
