import logging
import os
from pathlib import Path

import pytest
import yaml

if not os.environ.get("OPENAI_API_KEY"):
    pytest.skip(
        "LLM auto-populate tests require OPENAI_API_KEY",
        allow_module_level=True,
    )

import scripts.artist.artist_yaml.artist_yaml_auto_populate as auto_populate


@pytest.mark.parametrize(("value", "expected"), [("true", True), ("false", False)])
def test_parse_boolean(value: str, expected: bool) -> None:
    assert auto_populate.parse_boolean(value) is expected


def test_parse_boolean_rejects_invalid_value() -> None:
    with pytest.raises(Exception, match="expected true or false"):
        auto_populate.parse_boolean("yes")


def test_process_artist_yaml_file_skips_model_request_when_llm_disabled(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    artist_yaml_path = tmp_path / "artist.yml"
    original_content = "artistData:\n  members: []\n"
    artist_yaml_path.write_text(original_content, encoding="utf-8")
    monkeypatch.setattr(auto_populate, "client", object())

    result = auto_populate.process_artist_yaml_file(
        artist_yaml_path, "reference examples", 1, 1, llm_enabled=False
    )

    assert result is True
    assert artist_yaml_path.read_text(encoding="utf-8") == original_content


def test_remove_duplicate_members_lists_merges_lists() -> None:
    content = """artistData:
    artistNames:
        - The Example Band
    members:
        - artistNames:
                - First Member
    members:
        - artistNames:
                - Duplicate Member
    city: Example City
"""

    normalized = auto_populate.remove_duplicate_members_lists(content)

    assert normalized.count("    members:\n") == 1
    assert "First Member" in normalized
    assert "Duplicate Member" in normalized
    assert "    city: Example City\n" in normalized


def test_remove_duplicate_members_lists_removes_empty_inline_list() -> None:
    content = """artistData:
  artistNames:
  - Glass Animals
  city: Oxford
  countryCode: GB
  languageCodes:
  - en
  regionCode: GB-ENG
  members:
    - artistNames:
      - Dave Bayley
      dob:
        y: 1989
        m: 6
        d: 2
  members: []
"""

    normalized = auto_populate.remove_duplicate_members_lists(content)

    assert normalized.count("members:") == 1
    assert "Dave Bayley" in normalized


def test_remove_duplicate_members_lists_from_root_cleans_all_artist_yaml_files(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level(logging.INFO)
    duplicate_content = """artistData:
  members:
    - artistNames:
        - First Member
  members:
    - artistNames:
        - Duplicate Member
"""
    first_path = tmp_path / "A" / "First Artist" / "artist.yml"
    second_path = tmp_path / "Z" / "Second Artist" / "artist.yml"
    first_path.parent.mkdir(parents=True)
    second_path.parent.mkdir(parents=True)
    first_path.write_text(duplicate_content, encoding="utf-8")
    second_path.write_text(duplicate_content, encoding="utf-8")

    cleaned_count = auto_populate.remove_duplicate_members_lists_from_root(tmp_path)

    assert cleaned_count == 2
    assert first_path.read_text(encoding="utf-8").count("  members:\n") == 1
    assert second_path.read_text(encoding="utf-8").count("  members:\n") == 1
    assert "First Member" in first_path.read_text(encoding="utf-8")
    assert "Duplicate Member" in second_path.read_text(encoding="utf-8")
    assert "Scanning 2 artist YAML file(s)" in caplog.text
    assert "Completed duplicate members scan: 2 modified, 0 unchanged" in caplog.text


def test_process_artist_yaml_files_skips_valid_artist_yaml(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level(logging.INFO)
    artist_path = tmp_path / "Example Artist"
    artist_path.mkdir()
    artist_yaml_path = artist_path / "artist.yml"
    artist_yaml_path.write_text(
        yaml.safe_dump(
            {
                "artistData": {
                    "artistNames": ["The Example Band"],
                    "dob": {"y": 1990},
                    "city": "Example City",
                    "countryCode": "US",
                    "regionCode": "US-CA",
                    "languageCodes": ["en"],
                    "members": [],
                }
            }
        ),
        encoding="utf-8",
    )
    processed_files: set[Path] = set()

    def load_input_files(_letters: list[str]) -> list[Path]:
        return [artist_yaml_path]

    def load_reference_examples(_letters: list[str]) -> str:
        raise AssertionError("valid files should not load reference examples")

    monkeypatch.setattr(auto_populate, "load_input_files", load_input_files)
    monkeypatch.setattr(
        auto_populate,
        "load_reference_examples",
        load_reference_examples,
    )

    result = auto_populate.process_artist_yaml_files(tmp_path, ["E"], processed_files)

    assert result is None
    assert processed_files == {artist_yaml_path}
    assert f"Skipping already-valid artist YAML file: {artist_yaml_path}" in caplog.text


def test_process_artist_yaml_files_logs_validation_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    artist_path = tmp_path / "Example Artist"
    artist_path.mkdir()
    artist_yaml_path = artist_path / "artist.yml"
    artist_yaml_path.write_text(
        yaml.safe_dump(
            {
                "artistData": {
                    "artistNames": ["The Example Band"],
                    "dob": {"y": 1990},
                    "city": "Example City",
                    "countryCode": "UK",
                    "regionCode": "GB-LND",
                    "languageCodes": ["en"],
                    "members": [],
                }
            }
        ),
        encoding="utf-8",
    )
    processed_files: set[Path] = set()

    monkeypatch.setattr(
        auto_populate, "load_input_files", lambda _letters: [artist_yaml_path]  # type: ignore
    )
    monkeypatch.setattr(
        auto_populate,
        "load_reference_examples",
        lambda _letters: "reference examples",  # type: ignore
    )
    monkeypatch.setattr(
        auto_populate,
        "process_artist_yaml_file",
        lambda *_args, **_kwargs: True,  # type: ignore
    )

    result = auto_populate.process_artist_yaml_files(tmp_path, ["E"], processed_files)

    assert result is True
    assert processed_files == {artist_yaml_path}
    assert "invalid countryCode 'UK'" in caplog.text
