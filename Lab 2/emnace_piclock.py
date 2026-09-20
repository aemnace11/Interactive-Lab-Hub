import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw
import adafruit_rgb_display.st7789 as st7789

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.D5) 
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

COLOR_KEYFRAMES = [
    (0,    (0,   0,   0)),     # midnight - black
    (5,    (0,   0,   80)),    # pre-dawn - deep blue
    (6.5,  (255, 200, 80)),    # sunrise - golden yellow
    (12,   (255, 255, 255)),   # noon - white
    (17.5, (255, 120, 0)),     # sunset start - orange
    (19,   (180, 0,   0)),     # after sunset - red
    (21,   (0,   0,   0)),     # night - black
    (24,   (0,   0,   0)),     # wraps back to midnight - black
]

def _blend_color(c1, c2, frac):
    """Blend linearly between two (r,g,b) colors."""
    return tuple(int(round(c1[i] + (c2[i] - c1[i]) * frac)) for i in range(3))

def time_to_rgb(t=None, keyframes=COLOR_KEYFRAMES):
    """Map a time value to an RGB color using a custom day/night spectrum.

    t: optional parameter to set time manually
    """
    if t is None:
        t = time.time()

    local = time.localtime(t)
    hour = local.tm_hour + local.tm_min / 60 + local.tm_sec / 3600

    # Find the two keyframes the current hour falls between, and blend.
    for i in range(len(keyframes) - 1):
        h1, c1 = keyframes[i]
        h2, c2 = keyframes[i + 1]
        if h1 <= hour <= h2:
            frac = (hour - h1) / (h2 - h1) if h2 != h1 else 0
            return _blend_color(c1, c2, frac)

    return keyframes[-1][1]

while True:
    bg_color = time_to_rgb()
    draw.rectangle((0, 0, width, height), outline=0, fill=bg_color)

    # Display image.
    disp.image(image, rotation)
    time.sleep(1)
