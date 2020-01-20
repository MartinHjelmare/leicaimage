"""Handle Leica experiment."""
import re
from collections import namedtuple
from itertools import chain
from pathlib import Path
from typing import List, NamedTuple, Optional

_SLIDE = "slide"
_CHAMBER = "chamber"
_FIELD = "field"
_IMAGE = "image"
_ADDITIONAL_DATA = "AdditionalData"
_SCANNING_TEMPLATE = r"{ScanningTemplate}"


class Experiment:
    """Leica Matrix Screener experiment."""

    def __init__(self, path: str) -> None:
        """Set up instance."""
        self.path = path
        self._path = Path(path)
        self._slide_pattern = _pattern(_SLIDE)
        self._well_pattern = _pattern(self._slide_pattern, _CHAMBER)
        self._field_pattern = _pattern(self._well_pattern, _FIELD)
        self._image_pattern = _pattern(self._field_pattern, _IMAGE)

    def __repr__(self) -> str:
        """Return the representation."""
        return f"{type(self).__name__}(path={self.path})"

    @property
    def slides(self) -> List[str]:
        """Return a list of paths to slides."""
        return sorted(str(path) for path in self._path.glob(self._slide_pattern))

    @property
    def wells(self) -> List[str]:
        """Return a list of paths to wells."""
        return sorted(str(path) for path in self._path.glob(self._well_pattern))

    @property
    def fields(self) -> List[str]:
        """Return a list of paths to fields."""
        return sorted(str(path) for path in self._path.glob(self._field_pattern))

    @property
    def images(self) -> List[str]:
        """Return a list of paths to images."""
        tif_pattern = _pattern(self._image_pattern, extension="tif")
        png_pattern = _pattern(self._image_pattern, extension="png")
        tifs = self._path.glob(tif_pattern)
        pngs = self._path.glob(png_pattern)
        return sorted(str(path) for path in chain(tifs, pngs))

    @property
    def scanning_template(self) -> str:
        """Path to {ScanningTemplate}name.xml of experiment."""
        tmpl = list(
            self._path.glob(
                _pattern(_ADDITIONAL_DATA, _SCANNING_TEMPLATE, extension="*.xml")
            )
        )
        if tmpl:
            return str(tmpl[0])
        else:
            return ""

    @property
    def well_columns(self) -> List[int]:
        """Return all well columns in experiment.

        Equivalent to --V in files.

        Returns
        -------
        list of ints
        """
        return [
            col
            for col in set(attribute(img, "v") for img in self.images)
            if col is not None
        ]

    @property
    def well_rows(self) -> List[int]:
        """Return all well rows in experiment.

        Equivalent to --U in files.

        Returns
        -------
        list of ints
        """
        return [
            row
            for row in set(attribute(img, "u") for img in self.images)
            if row is not None
        ]

    def image(
        self, well_row: int, well_column: int, field_row: int, field_column: int
    ) -> str:
        """Get path of specified image.

        Parameters
        ----------
        well_row : int
            Starts at 0. Same as --U in files.
        well_column : int
            Starts at 0. Same as --V in files.
        field_row : int
            Starts at 0. Same as --Y in files.
        field_column : int
            Starts at 0. Same as --X in files.

        Returns
        -------
        string
            Path to image or empty string if image is not found.
        """
        return next(
            (
                i
                for i in self.images
                if attribute(i, "u") == well_column
                and attribute(i, "v") == well_row
                and attribute(i, "x") == field_column
                and attribute(i, "y") == field_row
            ),
            "",
        )

    def well_images(self, well_row: int, well_column: int) -> List[str]:
        """Get list of paths to images in specified well.

        Parameters
        ----------
        well_row : int
            Starts at 0. Same as --V in files.
        well_column : int
            Starts at 0. Save as --U in files.

        Returns
        -------
        list of strings
            Paths to images or empty list if no images are found.
        """
        return list(
            i
            for i in self.images
            if attribute(i, "u") == well_column and attribute(i, "v") == well_row
        )

    def field_columns(self, well_row: int, well_column: int) -> List[int]:
        """Return field columns for given well.

        Equivalent to --X in files.

        Parameters
        ----------
        well_row : int
            Starts at 0. Same as --V in files.
        well_column : int
            Starts at 0. Same as --U in files.

        Returns
        -------
        list of ints
            Columns found for specified well.
        """
        imgs = self.well_images(well_row, well_column)
        return [
            col for col in set(attribute(img, "x") for img in imgs) if col is not None
        ]

    def field_rows(self, well_row: int, well_column: int) -> List[int]:
        """Return field rows for given well.

        Equivalent to --Y in files.

        Parameters
        ----------
        well_column : int
            Starts at 0. Same as --U in files.
        well_row : int
            Starts at 0. Same as --V in files.

        Returns
        -------
        list of ints
            Rows found for specified well.
        """
        imgs = self.well_images(well_row, well_column)
        return [
            row for row in set(attribute(img, "y") for img in imgs) if row is not None
        ]


def attribute(path: str, name: str) -> Optional[int]:
    """Return the two numbers found behind --[A-Z] in path.

    If several matches are found, the last one is returned.

    Parameters
    ----------
    path : string
        String with path of file/folder to get attribute from.
    name : string
        Name of attribute to get. Should be A-Z or a-z (implicit converted to
        uppercase).

    Returns
    -------
    integer
        Returns number found in path behind --name as an integer.
    """
    matches = re.findall("--" + name.upper() + "([0-9]{2})", path)
    if matches:
        return int(matches[-1])
    else:
        return None


def attribute_as_str(path: str, name: str) -> Optional[str]:
    """Return the two numbers found behind --[A-Z] in path.

    If several matches are found, the last one is returned.

    Parameters
    ----------
    path : string
        String with path of file/folder to get attribute from.
    name : string
        Name of attribute to get. Should be A-Z or a-z (implicit converted to
        uppercase).

    Returns
    -------
    string
        Returns two digit number found in path behind --name.
    """
    matches = re.findall("--" + name.upper() + "([0-9]{2})", path)
    if matches:
        return matches[-1]
    else:
        return None


def attributes(path) -> NamedTuple:
    """Get attributes from path based on format --[A-Z].

    Returns a namedtuple with upper case attributes equal to what is found
    in path (string) and lower case as int.
    If path holds several occurrences of same character, only the last one is kept.

        >>> attrs = attributes('/folder/file--X00-X01.tif')
        >>> print(attrs)
        namedtuple('attributes', 'X x')('01', 1)
        >>> print(attrs.x)
        1

    Parameters
    ----------
    path : string

    Returns
    -------
    collections.namedtuple
    """
    # number of characters set to numbers have changed in LAS AF X !!
    matches = re.findall("--([A-Z]{1})([0-9]{2,4})", path)

    keys: List[str] = []
    values: List[str] = []
    for k, v in matches:
        if k in keys:
            # keep only last key
            i = keys.index(k)
            del keys[i]
            del values[i]
        keys.append(k)
        values.append(v)

    lower_keys = [k.lower() for k in keys]
    int_values = [int(v) for v in values]

    attrs = namedtuple("attributes", keys + lower_keys)

    return attrs(*values + int_values)


def _pattern(*names: str, extension: Optional[str] = None) -> str:
    """Return globbing pattern built from names with extension.

    Parameters
    ----------
    names : tuple
        Which path to join. Example: _pattern('path', 'to', 'experiment') will
        return `path/to/experiment--*`.
    extension : string
        If other extension then --* is wanted.
        Example: _pattern('path', 'to', 'image', extension='*.png') will return
        `path/to/image*.png`.

    Returns
    -------
    string
        Joined glob pattern string.
    """
    if extension is None:
        extension = "--*"
    path = Path("").joinpath(*names)
    return f"{path}{extension}"
