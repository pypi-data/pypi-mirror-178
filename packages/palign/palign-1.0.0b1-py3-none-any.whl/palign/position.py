class Position:
    """
    Position.

    `x` and `y` are the x and y coordinates.
    """

    def __init__(self, x: float, y: float) -> None:
        self._x = x
        self._y = y

    @property
    def x(self) -> float:
        """
        X coordinate.
        """

        return self._x

    @property
    def y(self) -> float:
        """
        Y coordinate.
        """

        return self._y
