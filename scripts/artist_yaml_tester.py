import os
from pathlib import Path

from mediascan.artist_yaml_file_loader import load_artist_yaml_file
from mediascan.media_files_yaml_file_loader import load_media_files_yaml_file

"""
Tests whether media library artist dirs have valid artists.yml file
(TODO: Integrate this into mediatest)

Note: Some of these tests should be moved to mediatest, once it has been refactored 
to test mediascan database instead of mediascan files.yml file

The scope of this script should be reduced to only test that the artist.yml files are
present and syntactically valid.

artist.yml file example:

artist_data:
  artist_names:
  - Parcels
  city: Byron Bay
  country_code: AU
  region_code: AU-NSW
  language_codes:
  - en


"""


EXCLUDE_DIRS = ["Various Artists"]


def excluded(path: Path) -> bool:
    for d in EXCLUDE_DIRS:
        if d in str(path):
            return True
    return False


def main():

    files_yaml_path = "../../out/files.yml"

    # TODO: Read source paths from config
    artist_yaml_paths: list[str] = []
    SOURCE_PATHS = ["/data/Music", "/data/MusicOther"]
    for source_path in SOURCE_PATHS:
        for root, _, files in os.walk(source_path):
            for f in files:
                if f == "artist.yml":
                    full_path = os.path.join(root, f)
                    absolute_path = os.path.abspath(full_path)
                    artist_yaml_paths.append(str(absolute_path))
                    print(f"found artist.yml: absolute_path={absolute_path}")
    artist_yaml_paths = list(set(artist_yaml_paths))

    files = load_media_files_yaml_file(files_yaml_path)
    artist_paths: dict[str, Path] = {}
    for file in files.files:
        if file.artist not in artist_paths:
            artist_paths[file.artist] = Path(file.path).parent.parent
    print(f"loaded {len(artist_paths)} artist paths from mediafiles yaml")
    artists_missing: list[str] = []
    exceptions: list[tuple[Path, Exception]] = []
    for artist, artist_path in artist_paths.items():
        if excluded(artist_path):
            continue

        artist_yaml_path = Path(artist_path).joinpath("artist.yml")
        if not artist_yaml_path.exists():
            print(f"{artist_path} missing artist.yml")
            artists_missing.append(artist)
        else:
            try:
                artist_yaml_paths.remove(str(artist_yaml_path))
            except Exception as ex:
                # (was hitting this due to symlink path difference and then str vs. Path type difference)
                print(f"path exists but isn't in the list, how?? '{artist_yaml_path}'")
                exceptions.append((artist_yaml_path, ex))
                # sys.exit(1)
            # validate yaml
            # according to official ISO standards (not European Commission standards)
            # Explanation:

            # The European Commission generally uses ISO 3166-1 alpha-2 codes with two exceptions:
            # 1) EL (not GR) is used to represent Greece
            # 2) UK (not GB) is used to represent the United Kingdom.

            # However I have decided to stick with the official ISO code (GB) based on this:

            # The official ISO 3166-1 alpha-2 code for the United Kingdom is GB (Great Britain), not "UK".
            # While "UK" is used colloquially and for the .uk internet domain,
            # ISO prefers "GB" because it stands for the sovereign state, i.e.
            # "The United Kingdom of Great Britain and Northern Ireland", while ignoring fillers like
            # "United" and "Kingdom". "UK" is officially reserved in ISO standards.

            # Northern Ireland uses GB (ISO 3166-1 alpha-2) as part of the United Kingdom.
            # Within ISO 3166-2 (subdivisions), it is designated as GB-NIR.
            # So for our validation purposes,
            # Northern Ireland should have country code "GB" and region code "GB-NIR"
            # Scotland should have country code "GB" and region code "GB-SCT"

            # The Euro convention would be inconsistent, having "UK" as the country_code
            # and "GB-NIR" as the region code, for example,
            # even though Northern Ireland is not geographically in Great Britain,
            # "GB" refers to "(The United Kingdom of) Great Britain and Northern Ireland",
            # and not to the geographic entity "Great Britain".

            try:
                adf = load_artist_yaml_file(str(artist_yaml_path))
                if adf.artist_data.country_code.upper() == "UK":
                    raise Exception(
                        "invalid countryCode 'UK' (United Kingdom country code should be 'GB', per ISO standard)"
                    )
                if adf.artist_data.country_code.upper() == "EL":
                    raise Exception(
                        "invalid countryCode 'EL' (Greece country code should be 'GR', per ISO standard)"
                    )
                if (
                    len(adf.artist_data.region_code)
                    and "-" not in adf.artist_data.region_code
                ):
                    # require format 'GB-NIR' rather than just 'NIR'
                    raise Exception(
                        f"invalid regionCode '{adf.artist_data.region_code}' (missing hyphen)"
                    )
                # require country and region codes to be uppercase
                if adf.artist_data.country_code != adf.artist_data.country_code.upper():
                    raise Exception(
                        "invalid countryCode (lowercase letters are not allowed"
                    )
                if adf.artist_data.region_code != adf.artist_data.region_code.upper():
                    raise Exception(
                        "invalid regionCode (lowercase letters are not allowed"
                    )
                # require language codes to be lowercase
                for l in adf.artist_data.language_codes:
                    if l != l.lower():
                        raise Exception(
                            "invalid languageCode (uppercase letters are not allowed"
                        )
                # require countryCode to be non-empty
                if adf.artist_data.country_code == "":
                    raise Exception("invalid countryCode (must not be empty)")

                # The region codes should be broader than the city,
                # but not too broad.

                # No: Birmingham (Birmingham, United Kingdom)
                # No: Birmingham (England, United Kingdom)
                # Yes: Birmingham (West Midlands, United Kingdom)
                if (
                    adf.artist_data.city == "Birmingham"
                    and adf.artist_data.country_code == "GB"
                    and adf.artist_data.region_code != "GB-WMD"
                ):
                    raise Exception(
                        "The correct region code for Birmingham, UK is GB-WMD (West Midlands)"
                    )

                # No: Manchester (Manchester, United Kingdom)
                # No: Manchester (England, United Kingdom)
                # Yes: Manchester (North West England, United Kingdom)
                if (
                    adf.artist_data.city == "Manchester"
                    and adf.artist_data.country_code == "GB"
                    and adf.artist_data.region_code != "GB-NWK"
                ):
                    raise Exception(
                        "The correct region code for Manchester, UK is GB-NWK (North West England)"
                    )

                # Don't allow region code to be so specific that it simply duplicates the city
                # Region code should be state, province, or equivalent
                if adf.artist_data.region_code == "GB-HER":
                    raise Exception(
                        "The correct region code for Herefordshire, UK is GB-WMD (West Midlands)"
                    )

            except Exception as ex:
                artists_missing.append(artist)
                exceptions.append((artist_yaml_path, ex))
    exist_count = len(artist_paths) - len(artists_missing)
    print(
        f"Found artist.yml for {exist_count} out of {len(artist_paths)} artist folders"
    )
    print(f"Missing/Invalid count: {len(artists_missing)}")
    if len(artists_missing) > 0:
        print("Writing artists missing artist.yml list to artists_missing.txt")
        with open("artists_missing.txt", "w") as f:
            for artist in sorted(artists_missing):
                f.write(artist + os.linesep)
    if len(exceptions) > 0:
        print("Exceptions:")
        for artist_yaml_path, ex in exceptions:
            print(artist_yaml_path, ex)

    # artist_yaml_paths should now be empty
    # if it's not empty, that means there is an artist.yml file on the filesystem that is not
    # in the artist path of any artist, so it's probably in the wrong directory
    if len(artist_yaml_paths) > 0:
        print("Warnings:")
        print(
            "Validation skipped for the following artist.yml files which are not in any artist path:"
        )
        for p in artist_yaml_paths:
            print(p)


if __name__ == "__main__":
    main()
