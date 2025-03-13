import os
import pprint as pp
import sys
from dataclasses import dataclass
from typing import Iterable, Self

import numpy as np

import interpolation
import least_squares
from parse_temps import parse_raw_temps

# Note: the type keyword requires Python 3.12 or newer
LineDataTuple = tuple[list[int], list[int], list[float], list[float]]


def write_core_file(
    base_name: str,
    core_idx: int,
    line_data: LineDataTuple,
) -> None:
    """
    Output the computed "line" data for a single core where each output line
    takes the form...

       0 <= x <=       30 ; y =      61.0000 +       0.6333 x ; interpolation

    or

       0 <= x <=     3520 ; y =      61.0000 +       0.0003 x ; least-squares
    """

    core_filename = f"{base_name}-core-{core_idx}.txt"

    with open(core_filename, "w") as core_file:
        for time, time_next, y_int, slope in zip(*line_data):
            core_file.write(
                f"{time:>6} <= x <= {time_next:>6} ;"
                f"y = {y_int:>8.4f} + {slope:>8.4f} x ; interpolation\n"
            )

        # TODO: Least Squares Approximation output
        time = 0
        time_next = 0
        y_int = 0
        slope = 0
        core_file.write(
            f"{time:>6} <= x <= {time_next:>6} ;"
            f"y = {y_int:>8.4f} + {slope:>8.4f} x ; least-squares\n"
        )


def main():
    """
    This main function serves as the driver for the demo. Such functions
    are not required in Python. However, we want to prevent unnecessary module
    level (i.e., global) variables.
    """

    # ---------------------------------------------------------------------------
    # Handle CLI
    # ---------------------------------------------------------------------------
    # TODO: Add command line argument validation
    temperature_filename = sys.argv[1]

    # ---------------------------------------------------------------------------
    # Handle input and preprocssing
    # ---------------------------------------------------------------------------
    with open(temperature_filename, "r") as temps_file:
        raw_temperature_data = parse_raw_temps(temps_file)

        times = []
        core_temps = [[] for _ in range(0, 4)]

        for time, readings in raw_temperature_data:
            times.append(time)

            for core_idx, core_reading in enumerate(readings):
                core_temps[core_idx].append(core_reading)

    # ---------------------------------------------------------------------------
    # Process each core and output the results
    # ---------------------------------------------------------------------------
    # Remove the file extension (get everything up to the '.')
    base_filename = os.path.splitext(temperature_filename)[0]

    pp.pprint(times)
    times_lower = times[0:-1]
    times_upper = times[1:]
    for core_idx, core_temps in enumerate(core_temps):
        # interpolation
        raw_line_data = interpolation.piecewise_linear(times, core_temps)

        y_ints = []
        slopes = []
        for _, _, y_int, slope in raw_line_data:
            y_ints.append(y_int)
            slopes.append(slope)

        # TODO: least squares approximation

        write_core_file(
            base_filename, core_idx, (times_lower, times_upper, y_ints, slopes)
        )


if __name__ == "__main__":
    main()
