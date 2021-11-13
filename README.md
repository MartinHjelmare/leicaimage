# leicaimage

[![build-badge]][build]

Handle Leica Matrix Screener experiment images

The leicaimage library is a modified version of the
[leicaexperiment](https://github.com/arve0/leicaexperiment) library,
and was built as a drop in replacement for that library but without any xml
or image processing. This also makes leicaimage work without heavy dependencies.

## Overview

This is a python module for interfacing with *Leica LAS AF/X Matrix Screener*
experiments.

The module can be used to:

- Programmatically select slides/wells/fields/images given by attributes like:
  - slide (S)
  - well position (U, V)
  - field position (X, Y)
  - z-stack position (Z)
  - channel (C)

## Features

- Access experiment as a python object

## Installation

Python 3.7+ is required. Install using `pip`:

```bash
pip install leicaimage
```

## Examples

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

## Development

Install dependencies and link development version of leicaimage to pip:

```bash
git clone https://github.com/MartinHjelmare/leicaimage.git
cd leicaimage
pip install -r requirements_dev.txt
```

### Run tests

```bash
tox
```

[build-badge]: https://github.com/MartinHjelmare/leicaimage/workflows/Test/badge.svg
[build]: https://github.com/MartinHjelmare/leicaimage/actions
