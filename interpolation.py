"""
This module is a collection of interpolation functions for the CPU Temperatures
Project.  All code may be used freely in the semester project, iff it is
imported using ``import interpolation`` or ``from interpolation import {...}``
where ``{...}`` represents one or more functions.
"""

from typing import Generator


def linear(
    time_start, time_end, reading_start, reading_end
) -> tuple[float, float]:
    """
    Compute the line between time_start and time end

    Returns:

        y-intercept and slope in the form of a tuple
    """

    slope = (reading_end - reading_start) / (time_end - time_start)
    y_int = reading_end - (slope * time_end)

    return (y_int, slope)


def piecewise_linear(
    times: list[float], temperatures: list[float]
) -> Generator[tuple[float, float, float, float], None, None]:
    """
    T.B.W.

    Yields:
        tuples in the form...

        (start time, end time, y-intercept, slope)
    """

    reading_generator = zip(
        times[0:-1], times[1:], temperatures[0:-1], temperatures[1:]
    )

    for start_time, end_time, start_reading, end_reading in reading_generator:
        y_int, slope = linear(start_time, end_time, start_reading, end_reading)

        yield start_time, end_time, y_int, slope
