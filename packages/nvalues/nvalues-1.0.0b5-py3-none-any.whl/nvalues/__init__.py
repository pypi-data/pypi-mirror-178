"""
nvalues is a Python package for working with n-dimensional volumes of data.

&copy; 2022 Cariad Eccleston and released under the MIT License.

For usage and support, see https://nvalues.dev.
"""

from importlib.resources import files

from nvalues.cube import Cube
from nvalues.grid import Grid
from nvalues.line import Line
from nvalues.penteract import Penteract
from nvalues.tesseract import Tesseract
from nvalues.value import Value
from nvalues.volume import Volume

with files(__package__).joinpath("VERSION").open("r") as t:
    version = t.readline().strip()

__all__ = [
    "Cube",
    "Grid",
    "Line",
    "Penteract",
    "Tesseract",
    "Value",
    "Volume",
]
