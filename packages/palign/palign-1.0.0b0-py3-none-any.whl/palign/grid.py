from typing import Optional

from nvalues import Volume
from PIL.ImageDraw import ImageDraw

from palign.cell import Cell
from palign.draw_text import draw_text
from palign.style import Style
from palign.types import Bounds


class Grid:
    """
    Text grid.
    """

    def __init__(
        self,
        columns: int,
        rows: int,
        cell_style: Optional[Style] = None,
    ) -> None:
        def validate_key(key: tuple[int, int]) -> None:
            x = key[0]
            if x < 0 or x >= columns:
                raise ValueError(f"No column {x} (grid has {columns})")

            y = key[1]
            if y < 0 or y >= rows:
                raise ValueError(f"No row {y} (grid has {rows})")

        self._columns = columns
        self._rows = rows

        def make_cell(_: tuple[int, int]) -> Cell:
            return Cell(style=Style())

        self._cells = Volume[tuple[int, int], Cell](
            default_maker=make_cell,
            key_validator=validate_key,
        )

        self._default_style = cell_style

    def __delitem__(self, key: tuple[int, int]) -> None:
        del self._cells[key]

    def __getitem__(self, key: tuple[int, int]) -> Cell:
        return self._cells[key]

    def __setitem__(self, key: tuple[int, int], value: Cell) -> None:
        self._cells[key] = value

    def _cell_bounds(
        self,
        column: int,
        row: int,
        grid_left: float,
        grid_top: float,
        grid_width: float,
        grid_height: float,
    ) -> Bounds:
        column_width = grid_width / self._columns
        row_height = grid_height / self._rows
        left = grid_left + (column * column_width)
        top = grid_top + (row * row_height)
        return (left, top, left + column_width, top + row_height)

    def render(
        self,
        draw: ImageDraw,
        left: float,
        top: float,
        width: float,
        height: float,
    ) -> None:
        """
        Renders the grid.
        """

        for x in range(self._columns):
            for y in range(self._rows):
                bounds = self._cell_bounds(
                    x,
                    y,
                    left,
                    top,
                    width,
                    height,
                )
                cell = self[x, y]

                style = (
                    self._default_style + cell.style
                    if self._default_style
                    else cell.style
                )
                draw_text(cell.text, draw, style, bounds)
