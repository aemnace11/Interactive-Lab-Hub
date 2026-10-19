"""
Every number you might want to tweak lives here.

Run calibrate.py first, then paste the two thresholds it suggests below.
"""

# ---------------------------------------------------------------------------
# Servo (SparkFun Servo pHAT, servo plugged into channel 0)
# ---------------------------------------------------------------------------
SERVO_CHANNEL = 0

# Angles are in the servo library's units: 0 is one end of the safe range,
# 120 is the class example's safe maximum for 9g servos. Never go outside
# SAFE_MIN_ANGLE..SAFE_MAX_ANGLE; every move is clamped to this range.
SAFE_MIN_ANGLE = 0
SAFE_MAX_ANGLE = 120

FACING_ANGLE = 0      # watching the couple
AWAY_ANGLE = 120      # back turned ("I do NOT need to see this")
PEEK_ANGLE = 60       # halfway point where he pauses when the lights come back on

# Speeds in degrees per second. Lower = slower, more dramatic.
TURN_AWAY_SPEED = 90  # quick, flustered turn when the lights dim
TURN_BACK_SPEED = 30  # slow, suspicious return when the lights are fully back on
PEEK_PAUSE = 1.5      # seconds he hesitates halfway back

# ---------------------------------------------------------------------------
# Sneak peeks (while the lights are dim and he's turned away)
# ---------------------------------------------------------------------------
# Every so often he slowly creeps all the way back around to look at the
# couple, stares for a split second, then jerks back to facing away.
SNEAK_PEEKS = True
SNEAK_PEEK_EVERY = (10, 25)   # random wait between peeks, in seconds
SNEAK_PEEK_SPEED = 25         # degrees/second for the slow creep (120 deg = ~5 s)

# While he stares at the couple he also checks the lights: if they're fully
# back on, he stays facing instead of jerking away. The stare lasts about
# (1 + SNEAK_STARE_READINGS) x 0.2 seconds.
SNEAK_STARE_READINGS = 2

# After the instant jerk away, wait this long for the servo to physically
# arrive before doing anything else.
JERK_SETTLE = 0.4

# ---------------------------------------------------------------------------
# Light sensor (APDS-9960 on Qwiic, facing the ceiling)
# ---------------------------------------------------------------------------
# Gain: 0 = 1x, 1 = 4x, 2 = 16x, 3 = 64x.
# If calibrate.py says the sensor is maxed out, lower this.
# If every reading is tiny (under ~50), raise it.
COLOR_GAIN = 1

# Integration time in 2.78 ms steps. 72 = 200 ms per reading.
# (The library default is 256 = 712 ms, which makes him slow to react.)
INTEGRATION_TIME = 72

# How many readings are averaged before he makes a decision.
# 8 readings x 200 ms = about 1.6 seconds, so a passing shadow is ignored.
SMOOTHING_WINDOW = 8

# He turns away when the average drops BELOW DARK_THRESHOLD, and only turns
# back when it rises ABOVE BRIGHT_THRESHOLD, which sits just under the
# "lights fully on" level. Partly raising the lights isn't enough.
# These are placeholders: replace them with what calibrate.py suggests.
DARK_THRESHOLD = 25
BRIGHT_THRESHOLD = 160
