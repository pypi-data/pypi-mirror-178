from typing import Callable, Optional, Tuple, Union

from PIL.ImageFont import FreeTypeFont

Bounds = Tuple[float, float, float, float]
"""
X0, Y0, X1, Y1
"""

Color = Union[
    Tuple[int, int, int],
    Tuple[int, int, int, int],
]

GetTextLength = Callable[[str, Optional[FreeTypeFont]], float]
