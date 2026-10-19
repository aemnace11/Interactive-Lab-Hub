"""
Measures your room's light levels and suggests thresholds for config.py.

Set the figure up where it will actually sit, then run:
    python calibrate.py

It samples three scenes (lights on, lights dimmed, dimmed with the candle
on the table) and prints two lines to paste into config.py.
"""

import time

import config
from light_sensor import LightSensor

SAMPLE_SECONDS = 3

SCENES = [
    ("bright", "Lights fully ON, exactly as they'll be in the demo"),
    ("dim", "Lights DIMMED for the romantic dinner"),
    ("candle", "Lights DIMMED with the LED candle on the table (type s to skip)"),
]


def sample(sensor, seconds):
    # Throw away readings that may have started before the scene was set up.
    for _ in range(2):
        sensor.read_raw()

    values = []
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        value = sensor.read_raw()
        values.append(value)
        print(f"  reading: {value:6d}", end="\r")
    print(" " * 30, end="\r")
    return values


def main():
    sensor = LightSensor()
    print("Calibrating the Third Wheel's light sensor.")
    print(f"(gain setting {config.COLOR_GAIN}, max possible reading {sensor.max_count})\n")

    results = {}
    saturated = False
    for key, description in SCENES:
        answer = input(f"Set up: {description}, then press Enter... ").strip().lower()
        if answer == "s":
            print("  skipped\n")
            continue

        values = sample(sensor, SAMPLE_SECONDS)
        avg = sum(values) / len(values)
        results[key] = avg
        print(f"  average {avg:.0f}   (min {min(values)}, max {max(values)})")
        if max(values) >= sensor.max_count:
            print("  WARNING: sensor maxed out.")
            saturated = True
        print()

    if saturated:
        print("The sensor maxed out, so these readings aren't trustworthy.")
        print("Lower COLOR_GAIN in config.py by one step and rerun this script.")
        return

    if "bright" not in results or "dim" not in results:
        print("Need at least the bright and dim scenes to suggest thresholds.")
        return

    bright = results["bright"]
    # Use whichever dark scene reads brighter: that's the hardest case to detect.
    dark = max(results["dim"], results.get("candle", 0))

    if "candle" in results and results["candle"] > results["dim"] * 1.5:
        print("Note: the candle raises the reading a lot. Consider a small cardboard")
        print("shield between the candle and the sensor window.\n")

    if dark >= bright * 0.7:
        print("Not enough difference between bright and dim for a reliable trigger.")
        print("Try: dimming the lights further, shielding the sensor from the candle,")
        print("or raising COLOR_GAIN. Then rerun this script.")
        return

    # Turn away once the room is about halfway to dim. Only turn back once
    # the lights are nearly all the way on (85% of the way back to full).
    gap = bright - dark
    dark_threshold = round(dark + gap * 0.50)
    bright_threshold = round(dark + gap * 0.85)

    print("He'll turn away once the lights are about halfway down, and only")
    print("turn back when they're nearly all the way back on.\n")
    print("Paste these into config.py:\n")
    print(f"DARK_THRESHOLD = {dark_threshold}")
    print(f"BRIGHT_THRESHOLD = {bright_threshold}")


if __name__ == "__main__":
    main()
