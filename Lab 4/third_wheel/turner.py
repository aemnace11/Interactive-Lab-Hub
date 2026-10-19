"""
Drives the servo under the turntable, with smooth, eased movements so the
figure looks like it is turning on purpose instead of snapping.
"""

import math
import time

import pi_servo_hat

import config

STEP_TIME = 0.02  # seconds between servo updates (50 updates per second)


def clamp(angle):
    return max(config.SAFE_MIN_ANGLE, min(config.SAFE_MAX_ANGLE, angle))


class Turner:
    def __init__(self):
        try:
            self.hat = pi_servo_hat.PiServoHat()
            self.hat.restart()
        except Exception as err:
            raise RuntimeError(
                "Couldn't reach the Servo pHAT (I2C address 0x40). Check that it is "
                "seated on the header and powered through its own USB-C cable."
            ) from err

        self.angle = clamp(config.FACING_ANGLE)
        self._write(self.angle)

    def _write(self, angle):
        self.hat.move_servo_position(config.SERVO_CHANNEL, clamp(angle))

    def glide_to(self, target, speed):
        """Move to `target` at roughly `speed` degrees per second, easing in and out."""
        target = clamp(target)
        start = self.angle
        distance = abs(target - start)
        if distance == 0:
            return

        duration = distance / speed
        steps = max(1, round(duration / STEP_TIME))
        for i in range(1, steps + 1):
            t = i / steps
            eased = (1 - math.cos(math.pi * t)) / 2  # slow start, slow stop
            self._write(start + (target - start) * eased)
            time.sleep(duration / steps)
        self.angle = target

    # --- The Third Wheel's moves -------------------------------------------

    def turn_away(self):
        """Lights went down: quick, flustered turn to face away."""
        self.glide_to(config.AWAY_ANGLE, config.TURN_AWAY_SPEED)

    def turn_back(self):
        """Lights came up: slowly turn halfway, hesitate, then face the couple."""
        self.glide_to(config.PEEK_ANGLE, config.TURN_BACK_SPEED)
        time.sleep(config.PEEK_PAUSE)
        self.glide_to(config.FACING_ANGLE, config.TURN_BACK_SPEED)

    def snap_to(self, target):
        """Jump straight to `target` at the servo's full speed: no easing."""
        target = clamp(target)
        self._write(target)
        self.angle = target
        time.sleep(config.JERK_SETTLE)

    def peek_slowly(self):
        """Sneak peek, part 1: creep all the way back around to face the couple."""
        self.glide_to(config.FACING_ANGLE, config.SNEAK_PEEK_SPEED)

    def jerk_away(self):
        """Sneak peek, part 2: saw too much, snap back to facing away."""
        self.snap_to(config.AWAY_ANGLE)

    def sneak_peek(self):
        """The whole peek in one go."""
        self.peek_slowly()
        time.sleep(0.6)
        self.jerk_away()

    def face_couple(self):
        self.glide_to(config.FACING_ANGLE, config.TURN_BACK_SPEED)
