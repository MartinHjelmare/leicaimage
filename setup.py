"""Set up file for leicaimage package."""
from pathlib import Path

from setuptools import find_packages, setup

PROJECT_DIR = Path(__file__).parent.resolve()
README_FILE = PROJECT_DIR / "README.md"
LONG_DESCR = README_FILE.read_text(encoding="utf-8")
VERSION = (PROJECT_DIR / "leicaimage" / "VERSION").read_text().strip()
GITHUB_URL = "https://github.com/MartinHjelmare/leicaimage"
DOWNLOAD_URL = f"{GITHUB_URL}/archive/master.zip"


setup(
    name="leicaimage",
    version=VERSION,
    description="Handle Leica Matrix Screener experiment images",
    long_description=LONG_DESCR,
    author="Martin Hjelmare",
    author_email="marhje52@gmail.com",
    url=GITHUB_URL,
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    include_package_data=True,
    license="MIT",
    zip_safe=False,
    keywords="leicaimage",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
