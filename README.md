<img src="https://raw.githubusercontent.com/bretttolbert/moongas-mediatunes-web-vue/refs/heads/main/client/public/moongas.svg" width="128" height="128">

# moongas-mediascan-python

> 🚧 **Status: Work in Progress (WIP)**  
> This project is currently under active development. Features, APIs, and documentation are subject to change.

---

## Overview

**Python library for working with Moongas mediascan database files and metadata files.**

### A component of the `moongas` ecosystem of media library tools

- [moongas-collection-demo](https://github.com/bretttolbert/moongas-collection-demo) [![CI](https://github.com/bretttolbert/moongas-collection-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/bretttolbert/moongas-collection-demo/actions/workflows/ci.yml) - Example Moongas media collection (metadata only)
- [moongas-mediatunes-web-vue](https://github.com/bretttolbert/moongas-mediatunes-web-vue) [![CI](https://github.com/bretttolbert/moongas-mediatunes-web-vue/actions/workflows/ci.yml/badge.svg)](https://github.com/bretttolbert/moongas-mediatunes-web-vue/actions/workflows/ci.yml) - A Deno-tooled TypeScript/Vue SPA for Moongas hybrid media collections, pairing with the separate moongas-mediatunes-svc-python-blacksheep backend to seemlessly blend offline and streaming playback
- [moongas-mediatunes-svc-python-blacksheep](https://github.com/bretttolbert/moongas-mediatunes-svc-python-blacksheep) [![CI](https://github.com/bretttolbert/moongas-mediatunes-svc-python-blacksheep/actions/workflows/ci.yml/badge.svg)](https://github.com/bretttolbert/moongas-mediatunes-svc-python-blacksheep/actions/workflows/ci.yml) - Python+BlackSheep implementation of API service for Moongas hybrid media collections—backend for Moongas mediatunes web application (moongas-mediatunes-web-vue)
- [moongas-mediatunes-svc-java-javalin](https://github.com/bretttolbert/moongas-mediatunes-svc-java-javalin) [![CI](https://github.com/bretttolbert/moongas-mediatunes-svc-python-blacksheep/actions/workflows/ci.yml/badge.svg)](https://github.com/bretttolbert/moongas-mediatunes-svc-java-javalin/actions/workflows/ci.yml) - Java+Javalin implementation of API service for Moongas hybrid media collections—backend for Moongas mediatunes web application (moongas-mediatunes-web-vue)
- [moongas-mediascan-go](https://github.com/bretttolbert/moongas-mediascan-go) [![CI](https://github.com/bretttolbert/moongas-mediascan-go/actions/workflows/ci.yml/badge.svg)](https://github.com/bretttolbert/moongas-mediascan-go/actions/workflows/ci.yml) - Golang module to scan media collections and Moongas Yaml metatadata, outputs Moongas database
- [moongas-mediascan-python](https://github.com/bretttolbert/moongas-mediascan-python) [![CI](https://github.com/bretttolbert/moongas-mediascan-python/actions/workflows/ci.yml/badge.svg)](https://github.com/bretttolbert/moongas-mediascan-python/actions/workflows/ci.yml) - Python library with data classes for loading Moongas mediascan databases and Yaml metadata files
- [moongas-mediascripts-python](https://github.com/bretttolbert/moongas-mediascripts-python) [![CI](https://github.com/bretttolbert/moongas-mediascripts-python/actions/workflows/ci.yml/badge.svg)](https://github.com/bretttolbert/moongas-mediascripts-python/actions/workflows/ci.yml) - Python scripts for working with Moongas media collections.
- [moongas-mediatest-python-pytest](https://github.com/bretttolbert/moongas-mediatest-python-pytest) [![CI](https://github.com/bretttolbert/moongas-mediatest-python-pytest/actions/workflows/ci.yml/badge.svg)](https://github.com/bretttolbert/moongas-mediatest-python-pytest/actions/workflows/ci.yml) - Python tool for enforcing media collection rules (implemented with `pytest`)

## Live Demos
- [Live Demo (hosted on bretttolbert.com)](https://bretttolbert.com/mediaserver)
- [Live Demo (hosted on moongas.org)](https://moongas.org/mediaserver)

# Quick Start

```bash
pip install "git+https://github.com/bretttolbert/moongas-mediascan-python.git"
```

### (Developer) Clone GitHub repo and install (editable)

```bash
git clone git@github.com:bretttolbert/moongas-mediascan-python.git
cd moongas-mediascan-python
python -m pip install -e ".[dev]"
```

### Optional dependency groups

- `[dev]` - development dependencies (includes `pytest` and `ruff`)
