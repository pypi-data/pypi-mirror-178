from typing import Optional

from PIL.ImageDraw import ImageDraw

from palign.enums import Horizontal, Vertical
from palign.style import Style
from palign.text import Text
from palign.types import Bounds


def draw_text(
    text: Optional[str],
    draw: ImageDraw,
    style: Style,
    bounds: Bounds,
) -> None:
    if style.background is not None:
        draw.rectangle(bounds, fill=style.background)

    if text:
        if not style.font:
            raise ValueError("draw_text requires a font")

        line_height = style.font.size

        t = Text(text, style, draw.textlength)

        top = bounds[1]

        width = bounds[2] - bounds[0]
        height = bounds[3] - top

        for index, line in enumerate(t):

            match style.horizontal:
                case Horizontal.Center:
                    origin_x = bounds[0] + (width / 2) - (line.width / 2)
                case Horizontal.Right:
                    origin_x = bounds[0] + width - line.width
                case _:
                    origin_x = bounds[0]

            match style.vertical:
                case Vertical.Center:
                    origin_y = (
                        top
                        + (height / 2)
                        - (t.height / 2)
                        + (line_height * index)
                    )
                case Vertical.Bottom:
                    origin_y = top + height - t.height + (line_height * index)
                case _:
                    origin_y = top + (line_height * index)

            for char in line:
                render_x = char.x + origin_x
                render_y = origin_y
                draw.text(
                    (render_x, render_y),
                    char.character,
                    fill=style.color,
                    font=style.font,
                )
