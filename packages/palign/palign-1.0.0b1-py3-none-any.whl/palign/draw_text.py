from logging import getLogger
from typing import Optional

from PIL.ImageDraw import ImageDraw

from palign.bounds import Bounds
from palign.enums import Horizontal, Vertical
from palign.position import Position
from palign.style import Style
from palign.text import Text

DEFAULT_FONT_SIZE = 21

log = getLogger("palign")


def _render_text(
    text: str,
    draw: ImageDraw,
    style: Style,
    b: Bounds | Position,
) -> None:
    lh = style.font.size if style.font else DEFAULT_FONT_SIZE

    if not isinstance(b, Bounds) and not (style.horizontal and style.vertical):
        log.warning("Text will not be aligned when bounds are a position")

    t = Text(text, style, draw.textlength)

    for index, line in enumerate(t):
        match style.horizontal:
            case Horizontal.Center if isinstance(b, Bounds):
                x = b.x + (b.width / 2) - (line.width / 2)
            case Horizontal.Right if isinstance(b, Bounds):
                x = b.x + b.width - line.width
            case _:
                x = b.x

        match style.vertical:
            case Vertical.Center if isinstance(b, Bounds):
                y = b.y + (b.height / 2) - (t.height / 2) + (lh * index)
            case Vertical.Bottom if isinstance(b, Bounds):
                y = b.y + b.height - t.height + (lh * index)
            case _:
                y = b.y + (lh * index)

        for character in line:
            draw.text(
                (character.x + x, y),
                character.character,
                fill=style.color,
                font=style.font,
            )


def draw_text(
    text: Optional[str],
    draw: ImageDraw,
    style: Style,
    bounds: Bounds | Position,
) -> None:
    if style.background is not None:
        if isinstance(bounds, Bounds):
            draw.rectangle(bounds.top_left_bottom_right, fill=style.background)
        else:
            log.warning("Will not draw background when bounds is a position")

    if text:
        _render_text(text, draw, style, bounds)
