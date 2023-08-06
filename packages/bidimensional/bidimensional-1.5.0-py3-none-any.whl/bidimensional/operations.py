"""2D operations module.

This module contains methods used to perform operations on 2D coordinates, such
as calculating distances and angles between them.

Author:
    Paulo Sanchez (@erlete)
"""


import math

from bidimensional.coordinates import Coordinate


def distance(a: Coordinate, b: Coordinate) -> float:
    """Calculates the distance between two coordinates.

    Args:
        a (Coordinate2D): First coordinate.
        b (Coordinate2D): Second coordinate.

    Raises:
        TypeError: If a or b are not Coordinate2D objects.

    Returns:
        float: Distance between the two coordinates.
    """

    if not isinstance(a, Coordinate):
        raise TypeError("a must be a Coordinate2D instance")
    elif not isinstance(b, Coordinate):
        raise TypeError("b must be a Coordinate2D instance")

    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


def angle(a: Coordinate, b: Coordinate, c: Coordinate) -> float:
    """Calculates the angle between three coordinates.

    Args:
        a (Coordinate2D): First coordinate.
        b (Coordinate2D): Second coordinate.
        c (Coordinate2D): Third coordinate.

    Raises:
        TypeError: If a, b or c are not Coordinate2D objects.

    Returns:
        float: Angle between the three coordinates.
    """

    if not isinstance(a, Coordinate):
        raise TypeError("a must be a Coordinate2D instance")
    elif not isinstance(b, Coordinate):
        raise TypeError("b must be a Coordinate2D instance")
    elif not isinstance(c, Coordinate):
        raise TypeError("c must be a Coordinate2D instance")

    e1 = distance(b, c)
    e2 = distance(a, c)
    e3 = distance(a, b)

    return math.degrees(math.acos(
        (math.pow(e2, 2) + math.pow(e3, 2) - math.pow(e1, 2)) / (2 * e2 * e3)
    ))


def midpoint(a: Coordinate, b: Coordinate) -> Coordinate:
    """Calculates the midpoint between two coordinates.

    Args:
        a (Coordinate2D): First coordinate.
        b (Coordinate2D): Second coordinate.

    Raises:
        TypeError: If a or b are not Coordinate2D objects.

    Returns:
        Coordinate2D: Midpoint between the two coordinates.
    """

    if not isinstance(a, Coordinate):
        raise TypeError("a must be a Coordinate2D instance")
    elif not isinstance(b, Coordinate):
        raise TypeError("b must be a Coordinate2D instance")

    return Coordinate((a.x + b.x) / 2, (a.y + b.y) / 2)
