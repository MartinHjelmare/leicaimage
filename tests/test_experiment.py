"""Test experiment."""
from pathlib import Path

import pytest

from leicaimage import Experiment
from leicaimage.experiment import _ADDITIONAL_DATA, _SCANNING_TEMPLATE


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
