# leicaimage

<p align="center">
  <a href="https://github.com/MartinHjelmare/leicaimage/actions/workflows/ci.yml?query=branch%3Amain">
    <img src="https://img.shields.io/github/actions/workflow/status/MartinHjelmare/leicaimage/ci.yml?branch=main&label=CI&logo=github&style=flat-square" alt="CI Status" >
  </a>
  <a href="https://codecov.io/gh/MartinHjelmare/leicaimage">
    <img src="https://img.shields.io/codecov/c/github/MartinHjelmare/leicaimage.svg?logo=codecov&logoColor=fff&style=flat-square" alt="Test coverage percentage">
  </a>
</p>
<p align="center">
  <a href="https://github.com/astral-sh/uv">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json" alt="uv">
  </a>
  <a href="https://github.com/astral-sh/ruff">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff">
  </a>
  <a href="https://github.com/pre-commit/pre-commit">
    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat-square" alt="pre-commit">
  </a>
</p>
<p align="center">
  <a href="https://pypi.org/project/leicaimage/">
    <img src="https://img.shields.io/pypi/v/leicaimage.svg?logo=python&logoColor=fff&style=flat-square" alt="PyPI Version">
  </a>
  <img src="https://img.shields.io/pypi/pyversions/leicaimage.svg?style=flat-square&logo=python&amp;logoColor=fff" alt="Supported Python versions">
  <img src="https://img.shields.io/pypi/l/leicaimage.svg?style=flat-square" alt="License">
</p>

---

**Source Code**: <a href="https://github.com/MartinHjelmare/leicaimage" target="_blank">https://github.com/MartinHjelmare/leicaimage </a>

---

Handle Leica Matrix Screener experiment images.

The leicaimage library is a modified version of the
[leicaexperiment](https://github.com/arve0/leicaexperiment) library,
and was built as a drop in replacement for that library but without any xml
or image processing. This also makes leicaimage work without heavy dependencies.

## Overview

This is a python module for interfacing with _Leica LAS AF/X Matrix Screener_
experiments.

The module can be used to:

- Programmatically select slides/wells/fields/images given by attributes like:
  - slide (S)
  - well position (U, V)
  - field position (X, Y)
  - z-stack position (Z)
  - channel (C)

## Installation

Install this via pip (or your favourite package manager):

`pip install leicaimage`

## Usage

### Access all images

```python
from leicaimage import Experiment

experiment = Experiment('path/to/experiment--')

for image in experiment.images:
    ...
```

### Access specific wells/fields

```python
from leicaimage import Experiment

experiment = Experiment('path/to/experiment--')

# on images in well --U00--V00
for well in experiment.well_images(0, 0):
    ...
```

### Extract attributes from file names

```python
from leicaimage import attribute

# get all channels
channels = [attribute(image, 'C') for image in experiment.images]
min_ch, max_ch = min(channels), max(channels)
```

## Credits

[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-orange.json)](https://github.com/copier-org/copier)

This package was created with
[Copier](https://copier.readthedocs.io/) and the
[browniebroke/pypackage-template](https://github.com/browniebroke/pypackage-template)
project template.
