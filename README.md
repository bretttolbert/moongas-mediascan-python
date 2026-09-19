<img src="https://raw.githubusercontent.com/bretttolbert/moongas-mediatunes-web/refs/heads/main/client/public/moongas.svg" width="128" height="128">

# moongas-py-mediascan

> 🚧 **Status: Work in Progress (WIP)**  
> This project is currently under active development. Features, APIs, and documentation are subject to change.

---

## Overview

**Python library for working with moongas mediascan database files and metadata files.**

### A component of the `moongas` ecosystem of media library tools

- [moongas-mediatunes-web](https://github.com/bretttolbert/moongas-mediatunes-web) [![CI](https://github.com/bretttolbert/moongas-py-mediaserver/actions/workflows/ci.yml/badge.svg)](https://github.com/bretttolbert/moongas-mediatunes-web/actions/workflows/ci.yml) - A Deno-tooled TypeScript/Vue SPA for Moongas hybrid media collections, pairing with the separate moongas-py-mediatunes-svc backend to seemlessly blend offline and streaming playback
- [moongas-py-mediatunes-svc](https://github.com/bretttolbert/moongas-py-mediatunes-svc) [![CI](https://github.com/bretttolbert/moongas-py-mediaserver/actions/workflows/ci.yml/badge.svg)](https://github.com/bretttolbert/moongas-py-mediatunes-svc/actions/workflows/ci.yml) - Python+BlackSheep API service for Moongas hybrid media collections—backend for moongas-mediatunes-web application
- [moongas-collection-demo](https://github.com/bretttolbert/moongas-collection-demo) [![CI](https://github.com/bretttolbert/moongas-collection-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/bretttolbert/moongas-collection-demo/actions/workflows/ci.yml) - Example Moongas media collection (metadata only)
- [moongas-py-mediascan](https://github.com/bretttolbert/moongas-py-mediascan) [![CI](https://github.com/bretttolbert/moongas-py-mediascan/actions/workflows/ci.yml/badge.svg)](https://github.com/bretttolbert/moongas-py-mediascan/actions/workflows/ci.yml) - Python package for loading Moongas database and Yaml
- [moongas-go-mediascan](https://github.com/bretttolbert/moongas-go-mediascan) [![CI](https://github.com/bretttolbert/moongas-go-mediascan/actions/workflows/ci.yml/badge.svg)](https://github.com/bretttolbert/moongas-go-mediascan/actions/workflows/ci.yml) - Golang module to scan media collections and Moongas Yaml metatadata, outputs Moongas database
- [moongas-py-mediatest](https://github.com/bretttolbert/moongas-py-mediatest) [![CI](https://github.com/bretttolbert/moongas-py-mediatest/actions/workflows/ci.yml/badge.svg)](https://github.com/bretttolbert/moongas-py-mediatest/actions/workflows/ci.yml) - Python tool for enforcing media collection rules (implemented with `pytest`)

## Live Demos
- [Live Demo (hosted on bretttolbert.com)](https://bretttolbert.com/mediaserver)
- [Live Demo (hosted on moongas.org)](https://moongas.org/mediaserver)

# Quick Start

```bash
pip install "git+https://github.com/bretttolbert/moongas-py-mediascan.git[stats]"
```

### (Developer) Clone GitHub repo and install (editable)

```bash
git clone git@github.com:bretttolbert/moongas-py-mediascan.git && cd mediascan
python -m pip install -e ".[dev,llm,stats]"
```

### Optional dependency groups

- `[dev]` - development dependencies (includes `pytest` and `ruff`)
- `[stats]` - statistics script dependencies (includes `matplotlib` and `numpy`)

## Media Scripts

This Python package includes various console scripts for working with Moongas media collections. The included script `mediascripts` can be used to list them. All scripts accept the `-h` (_help_) command-line argument to display usage information.


```bash
$ mediascripts
artist:
  artist-countries-to-mapgraph-json
  artist-csv-to-artist-yaml
  artist-yaml-auto-populate
  artist-yaml-reformat-with-files-yaml
  artist-yaml-test-with-files-yaml
  list-missing-region-names
convert:
  convert-covers
  convert-videos
  make-covers-video
copy:
  copy-medialib
dev:
  generate-dataclasses
media_files_yaml:
  list-artists-from-files-yaml
  play-rand-file-from-files-yaml
rename:
  rename-album-files
stats:
  mediastats
```
