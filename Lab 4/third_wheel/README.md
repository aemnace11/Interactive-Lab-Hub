# The Third Wheel

A dinner guest who turns his back when the lights dim for a romantic candlelit dinner and stays turned away until the lights are fully back on. Every so often he can't help himself: he slowly creeps all the way back around for a look, then jerks away. If the lights are back on when he peeks, he stays facing the table.

## Files

| File | What it does |
|---|---|
| `third_wheel.py` | The main program. Run this for the demo. |
| `config.py` | Every setting: angles, speeds, light thresholds. |
| `light_sensor.py` | Reads and smooths room brightness from the APDS-9960. |
| `turner.py` | Moves the servo smoothly (turn away, turn back, sneak peek). |
| `calibrate.py` | Measures your room and suggests light thresholds. |

## Hardware

- Servo pHAT on the Pi, powered by **its own USB-C cable**
- Servo in **channel 0** (brown/black wire to GND)
- APDS-9960 on Qwiic, mounted in the base facing the ceiling

## Run it

From `Lab 4/third_wheel`, with the Lab 4 virtual environment active (`source ../.venv/bin/activate`):

1. `i2cdetect -y 1` should show `39` (sensor) and `40` (servo pHAT).
3. `python calibrate.py`: follow the prompts, then paste the two suggested thresholds into `config.py`.
4. `python third_wheel.py`: dim the lights and watch him turn away. Ctrl+C to stop.

Sneak peek timing and speed are in the "Sneak peeks" section of `config.py`. Set `SNEAK_PEEKS = False` to turn them off.
