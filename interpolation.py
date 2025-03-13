"""
This module is a collection of interpolation functions for the CPU Temperatures
Project.  All code may be used freely in the semester project, iff it is
imported using ``import interpolation`` or ``from interpolation import {...}``
where ``{...}`` represents one or more functions.
"""

from typing import Generator


def piecewise_linear(
    times: list[float], temperatures: list[float]
) -> Generator[tuple[int, int, float, float], None, None]:
    """
    T.B.W.

    Yields:
        tuples in the form...

        (start time, end time, y-intercept, slope)
    """

    raise NotImplementedError()
