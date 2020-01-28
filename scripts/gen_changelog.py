#!/usr/bin/env python
"""Generate changelog."""
import os
from pathlib import Path
from typing import Optional

from pygcgen.main import ChangelogGenerator

GITHUB_PROJECT = "leicaimage"
GITHUB_USER = "MartinHjelmare"


def validate_version() -> Optional[str]:
    """Validate version before release."""
    import leicaimage  # pylint: disable=import-outside-toplevel

    version_string = leicaimage.__version__
    versions = version_string.split(".", 3)
    try:
        for ver in versions:
            int(ver)
    except ValueError:
        print(
            "Only integers are allowed in release version, "
            f"please adjust current version {version_string}"
        )
        return None
    return version_string


def generate() -> None:
    """Generate changelog."""
    old_dir = Path.cwd()
    proj_dir = Path(__file__).parent.parent
    os.chdir(proj_dir)
    version = validate_version()
    if not version:
        os.chdir(old_dir)
        return
    print(f"Generating changelog for version {version}")
    options = [
        "--user",
        GITHUB_USER,
        "--project",
        GITHUB_PROJECT,
        "-v",
        "--with-unreleased",
        "--future-release",
        version,
    ]
    generator = ChangelogGenerator(options)
    generator.run()
    os.chdir(old_dir)


if __name__ == "__main__":
    generate()
