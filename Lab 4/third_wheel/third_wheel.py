"""
The Third Wheel
A dinner guest who never got the hint. When the lights dim for a romantic
candlelit dinner, he turns his back on the couple and stays that way until
the lights are fully back on. He can't help himself, though: every so often
he slowly creeps back around for a look, then jerks away in horror.

Run from this folder, inside the Lab 4 virtual environment:
    python third_wheel.py

Press Ctrl+C to stop. He turns back to face the table before exiting.
"""

import random
import time

import config
from light_sensor import LightSensor
from turner import Turner

TURN_AWAY_LINES = [
    "I do NOT need to see this.",
    "Pretend I'm not here.",
    "Wow. Lovely wall.",
    "I'll just... admire the wallpaper.",
]
SNEAK_LINES = [
    "(...just one little look)",
    "(slowly turning around...)",
    "(are they still...?)",
]
JERK_LINES = [
    "NOPE.",
    "Oh no. Oh no no no.",
    "Can't unsee that.",
    "Wallpaper. Wallpaper is nice.",
]
TURN_BACK_LINES = [
    "Is it safe to look?",
    "Everyone decent?",
    "So... how's the bread?",
    "Did I miss anything?",
]


def schedule_sneak_peek():
    low, high = config.SNEAK_PEEK_EVERY
    return time.monotonic() + random.uniform(low, high)


def lights_fully_on(sensor):
    """Take a few fresh readings while he stares, and report whether the lights are back."""
    sensor.reset()
    sensor.read_raw()  # discard: it may have started while he was still turning
    for _ in range(config.SNEAK_STARE_READINGS):
        sensor.update()
    return sensor.average > config.BRIGHT_THRESHOLD


def main():
    if config.DARK_THRESHOLD >= config.BRIGHT_THRESHOLD:
        raise ValueError("In config.py, DARK_THRESHOLD must be lower than BRIGHT_THRESHOLD.")

    sensor = LightSensor()
    turner = Turner()
    turned_away = False
    next_sneak_peek = None
    warned_saturated = False

    print("The Third Wheel has taken his seat.")
    print(f"Turns away below {config.DARK_THRESHOLD}, turns back above "
          f"{config.BRIGHT_THRESHOLD}. Ctrl+C to stop.\n")

    try:
        while True:
            value = sensor.update()
            state = "AWAY" if turned_away else "WATCHING"
            print(f"light: {value:6d}   avg: {sensor.average:8.1f}   {state:8s}", end="\r")

            if sensor.is_saturated(value) and not warned_saturated:
                print("\nSensor is maxed out. Lower COLOR_GAIN in config.py.")
                warned_saturated = True

            if not sensor.is_ready:
                continue

            if not turned_away and sensor.average < config.DARK_THRESHOLD:
                print(f"\nLights dimmed. \"{random.choice(TURN_AWAY_LINES)}\"")
                turner.turn_away()
                turned_away = True
                if config.SNEAK_PEEKS:
                    next_sneak_peek = schedule_sneak_peek()
                sensor.reset()

            elif turned_away and sensor.average > config.BRIGHT_THRESHOLD:
                print(f"\nLights fully on. \"{random.choice(TURN_BACK_LINES)}\"")
                turner.turn_back()
                turned_away = False
                next_sneak_peek = None
                sensor.reset()

            elif turned_away and next_sneak_peek and time.monotonic() >= next_sneak_peek:
                print(f"\n{random.choice(SNEAK_LINES)}")
                turner.peek_slowly()
                if lights_fully_on(sensor):
                    print("Oh! The lights are back on. \"...Acting natural.\"")
                    turned_away = False
                    next_sneak_peek = None
                else:
                    print(f"\"{random.choice(JERK_LINES)}\"")
                    turner.jerk_away()
                    next_sneak_peek = schedule_sneak_peek()
                sensor.reset()

    except KeyboardInterrupt:
        print("\nDinner's over. Facing the table again.")
        turner.face_couple()


if __name__ == "__main__":
    main()
