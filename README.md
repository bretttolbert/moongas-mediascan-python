# moongas-py-mediascan
Python library for working with moongas mediascan database files and metadata files

- A component of the `moongas` ecosystem of media library tools
    - [moongas-collection-demo](https://github.com/bretttolbert/moongas-collection-demo) - Example Moongas media collection (metadata only)
    - [moongas-py-mediaserver](https://github.com/bretttolbert/moongas-py-mediaserver) - Flask Web App to serve Moongas media collections enabling users to browse, search (various streaming services) and (optionally) play local media files
    - [moongas-py-mediascan](https://github.com/bretttolbert/moongas-py-mediascan) - Python lib for loading Moongas database and Yaml
    - [moongas-go-mediascan](https://github.com/bretttolbert/moongas-py-mediascan) - Go lib to scan media collections and Moongas Yaml metatadata, outputs Moongas database
    - [moongas-py-mediatest](https://github.com/bretttolbert/moongas-py-mediatest) - Python tool for enforcing media collection rules (implemented with `pytest`)
    - [Flask-JSGlue](https://github.com/bretttolbert/Flask-JSGlue) - Dependency of `moongas-py-mediaserver`

## Installation 

### (User) Install from GitHub repo

```bash
pip install "git+https://github.com/bretttolbert/moongas-py-mediascan.git[stats]"
```

### (Developer) Clone GitHub repo and install (editable)

```bash
git clone git@github.com:bretttolbert/moongas-py-mediascan.git && cd mediascan
python -m pip install -e ".[dev,stats]"
```

### Optional dependency groups

- `[dev]` - development dependencies (includes `pytest` and `ruff`)
- `[stats]` - statistics script dependencies (includes `matplotlib` and `numpy`)

