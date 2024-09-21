"""Test experiment."""

from pathlib import Path

import pytest

from leicaimage import Experiment
from leicaimage.experiment import (
    _ADDITIONAL_DATA,
    _SCANNING_TEMPLATE,
    PathAttributes,
    attribute,
    attribute_as_str,
    attributes,
)

REL_IMAGE_PATH = (
    Path("slide--S00")
    / "chamber--U00--V00"
    / "field--X00--Y01"
    / ("image--L00--S00--U00--V00--J20--E00--O00--X00--Y01--T00--Z00--C00.ome.tif")
)


@pytest.fixture(name="experiment")
def experiment_fixture():
    """'experiment--test' in tmpdir. Returns Experiment object."""
    exp_path = Path(__file__).parent / "fixtures" / "experiment--test"
    return Experiment(str(exp_path))


def test_experiment_dirs(experiment):
    """Test experiment dirs."""
    slides = experiment.slides
    assert slides == [str(Path(experiment.path) / "slide--S00")]

    wells = experiment.wells
    assert wells == [str(Path(experiment.path) / "slide--S00" / "chamber--U00--V00")]

    # chambers is an alias for wells
    chambers = experiment.chambers
    assert chambers == [str(Path(experiment.path) / "slide--S00" / "chamber--U00--V00")]

    fields = [
        str(
            Path(experiment.path)
            / "slide--S00"
            / "chamber--U00--V00"
            / f"field--X00--Y{field_y:02}"
        )
        for field_y in range(2)
    ]
    assert experiment.fields == fields


def test_images(experiment):
    """Test experiment images."""
    images = [
        str(
            Path(experiment.path)
            / "slide--S00"
            / "chamber--U00--V00"
            / f"field--X00--Y{field_y:02}"
            / (
                "image--L00--S00--U00--V00--J20--E00--O00"
                f"--X00--Y{field_y:02}--T00--Z00--C{channel_id:02}.ome.tif"
            )
        )
        for field_y in range(2)
        for channel_id in range(2)
    ]

    assert experiment.images == images


def test_scanning_template(experiment):
    """Test experiment scanning template."""
    template = str(
        Path(experiment.path) / _ADDITIONAL_DATA / f"{_SCANNING_TEMPLATE}test.xml"
    )

    assert experiment.scanning_template == template


def test_empty_scanning_template(tmp_path):
    """Test empty experiment scanning template."""
    empty_exp_path = tmp_path / "experiment--test"
    empty_exp_path.mkdir()
    empty_exp = Experiment(str(empty_exp_path))

    assert not empty_exp.scanning_template


def test_well_columns(experiment):
    """Test experiment well columns."""
    cols = [0]

    assert experiment.well_columns == cols


def test_well_rows(experiment):
    """Test experiment well rows."""
    rows = [0]

    assert experiment.well_rows == rows


def test_image(experiment):
    """Test experiment image."""
    image = str(Path(experiment.path) / REL_IMAGE_PATH)

    assert experiment.image(0, 0, 1, 0) == image


def test_well_images(experiment):
    """Test experiment well images."""
    images = [
        str(
            Path(experiment.path)
            / "slide--S00"
            / "chamber--U00--V00"
            / f"field--X00--Y{field_y:02}"
            / (
                "image--L00--S00--U00--V00--J20--E00--O00"
                f"--X00--Y{field_y:02}--T00--Z00--C{channel_id:02}.ome.tif"
            )
        )
        for field_y in range(2)
        for channel_id in range(2)
    ]

    assert experiment.well_images(0, 0) == images


def test_field_columns(experiment):
    """Test experiment field columns."""
    assert experiment.field_columns(0, 0) == [0]


def test_field_rows(experiment):
    """Test experiment field rows."""
    assert experiment.field_rows(0, 0) == [0, 1]


def test_attribute(experiment):
    """Test experiment attribute as str."""
    assert attribute(str(Path(experiment.path) / REL_IMAGE_PATH), "U") == 0
    assert attribute(str(Path(experiment.path) / REL_IMAGE_PATH), "u") == 0
    assert attribute(str(Path(experiment.path) / REL_IMAGE_PATH), "Y") == 1
    assert attribute(str(Path(experiment.path) / REL_IMAGE_PATH), "y") == 1


def test_missing_attribute(experiment):
    """Test experiment missing attribute."""
    attr = attribute(str(Path(experiment.path) / REL_IMAGE_PATH), "missing")

    assert attr is None


def test_attribute_str(experiment):
    """Test experiment attribute as str."""
    assert attribute_as_str(str(Path(experiment.path) / REL_IMAGE_PATH), "U") == "00"
    assert attribute_as_str(str(Path(experiment.path) / REL_IMAGE_PATH), "u") == "00"
    assert attribute_as_str(str(Path(experiment.path) / REL_IMAGE_PATH), "Y") == "01"
    assert attribute_as_str(str(Path(experiment.path) / REL_IMAGE_PATH), "y") == "01"


def test_missing_attribute_str(experiment):
    """Test experiment missing attribute str."""
    attr = attribute_as_str(str(Path(experiment.path) / REL_IMAGE_PATH), "missing")

    assert attr is None


def test_attributes(experiment):
    """Test experiment attributes."""
    path = str(Path(experiment.path) / REL_IMAGE_PATH)
    # pylint: disable-next=use-dict-literal
    params = dict(
        L="00",
        S="00",
        U="00",
        V="00",
        J="20",
        E="00",
        O="00",  # noqa: E741
        X="00",
        Y="01",
        T="00",
        Z="00",
        C="00",
        l=0,  # noqa: E741
        s=0,
        u=0,
        v=0,
        j=20,
        e=0,
        o=0,
        x=0,
        y=1,
        t=0,
        z=0,
        c=0,
    )
    attrs = PathAttributes(**params)

    assert attributes(path) == attrs
