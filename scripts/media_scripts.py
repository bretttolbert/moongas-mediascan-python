#!/bin/bash

import argparse
import importlib.metadata


def list_media_scripts():
    parser = argparse.ArgumentParser(
        description="Lists all media* console script entry points, grouped by scripts subdirectory."
    )
    parser.parse_args()

    # Fetch all entry points belonging to the 'console_scripts' group
    eps = importlib.metadata.entry_points(group='console_scripts')

    # Group command names by the scripts subdirectory of the target module,
    # e.g. "scripts.convert.convert_covers:main" belongs to the "convert" group
    groups: dict[str, list[str]] = {}
    for ep in eps:
        # ep.value holds the 'module:function' path
        # ep.dist holds metadata about the package providing it (if available)
        package_name = ep.dist.name if ep.dist else "Unknown"
        if not package_name.startswith("media"):
            continue
        parts = ep.value.split(":")[0].split(".")
        group = parts[1] if len(parts) > 2 else "(root)"
        if ep.name != 'media-scripts':
            groups.setdefault(group, []).append(ep.name)

    for group in sorted(groups):
        print(f"{group}:")
        for name in sorted(groups[group]):
            print(f"  {name}")

if __name__ == "__main__":
    list_media_scripts()

