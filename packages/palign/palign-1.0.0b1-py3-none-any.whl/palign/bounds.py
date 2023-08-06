from palign.position import Position


class Bounds(Position):
    """
    A region of an image.

    `x` is the left-most position of the region in pixels.

    `y` is the top-most position of the region in pixels.

    `width` is the width of the region in pixels.

    `height` is the height of the region in pixels.
    """

    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
    ) -> None:
        super().__init__(x, y)
        self._width = width
        self._height = height

    @property
    def bottom(self) -> float:
        """
        Bottom-most position in pixels.
        """

        return self.y + self.height

    @property
    def height(self) -> float:
        """
        Height in pixels.
        """

        return self._height

    @property
    def right(self) -> float:
        """
        Right-most position in pixels.
        """

        return self.x + self.width

    @property
    def top_left_bottom_right(self) -> tuple[float, float, float, float]:
        """
        Translates the region to a tuple of coordinates.
        """

        return (self.x, self.y, self.right, self.bottom)

    @property
    def width(self) -> float:
        """
        Width in pixels.
        """

        return self._width
