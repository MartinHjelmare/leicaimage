"""Handle Leica images."""
from pathlib import Path

from .experiment import Experiment, attribute, attribute_as_str, attributes

__all__ = ["Experiment", "attribute", "attribute_as_str", "attributes"]
__version__ = (Path(__file__).parent / "VERSION").read_text().strip()
