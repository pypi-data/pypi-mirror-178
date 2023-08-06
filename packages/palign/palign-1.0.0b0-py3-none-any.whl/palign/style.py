from dataclasses import dataclass
from typing import Any, Optional, TypeVar

from PIL.ImageFont import FreeTypeFont

from palign.enums import Horizontal, Vertical
from palign.types import Color


@dataclass
class Style:
    """
    Text style.

    `background_color` describes the background colour. A background will not
    be painted if this is omitted.

    `color` describes the text colour. Text will not be painted if this is
    omitted.

    `font` describes the font. Pillow's default font will be used where
    possible if this is omitted, but many text operations will fail.

    `horizontal` describes the text's horizontal alignment within its bounds.
    Defaults to left.

    `tracking` describes the space to insert between each character. Defaults
    to none.

    `vertical` describes the text's vertical alignment within its bounds.
    Defaults to top.
    """

    background: Optional[Color] = None
    """
    Background colour.

    A background will not be painted if this is omitted.
    """

    color: Optional[Color] = None
    """
    Text colour.

    Text will not be painted if this is omitted.
    """

    font: Optional[FreeTypeFont] = None
    """
    Font.

    Pillow's default font will be used where possible if this is omitted, but
    many text operations will fail.
    """

    horizontal: Optional[Horizontal] = None
    """
    Horizontal alignment.
    """

    tracking: Optional[float] = None
    """
    Character tracking.
    """

    vertical: Optional[Vertical] = None
    """
    Vertical alignment.
    """

    def __add__(self, o: Any) -> "Style":
        if not isinstance(o, Style):
            raise TypeError("Can merge only Style to Style")

        V = TypeVar("V")

        def _or(a: V, b: V) -> V:
            return a if b is None else b

        return Style(
            background=_or(self.background, o.background),
            color=_or(self.color, o.color),
            font=_or(self.font, o.font),
            horizontal=_or(self.horizontal, o.horizontal),
            tracking=_or(self.tracking, o.tracking),
            vertical=_or(self.vertical, o.vertical),
        )
