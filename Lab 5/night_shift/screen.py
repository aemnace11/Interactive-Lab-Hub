import time

from PIL import Image, ImageDraw, ImageFont

import config

WIDTH, HEIGHT = 240, 135
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# mini pitft setup, falls back to terminal if missing
try:
    import board
    import digitalio
    from adafruit_rgb_display import st7789

    _disp = st7789.ST7789(
        board.SPI(),
        cs=digitalio.DigitalInOut(board.CE0),
        dc=digitalio.DigitalInOut(board.D25),
        rst=None,
        baudrate=64000000,
        width=135,
        height=240,
        x_offset=53,
        y_offset=40,
    )
    _light = digitalio.DigitalInOut(board.D22)
    _light.switch_to_output(value=True)
    _button = digitalio.DigitalInOut(board.D23)
    _button.switch_to_input(pull=digitalio.Pull.UP)
    HAS_SCREEN = True
except Exception:
    HAS_SCREEN = False


def font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except OSError:
        return ImageFont.load_default()


# push an image to the screen, or save it when there is no screen
def show(image, save_to=None):
    if save_to:
        image.save(save_to)
    if HAS_SCREEN:
        _disp.image(image, 90)


# draw centered lines of text
def text(lines, size=18):
    image = Image.new("RGB", (WIDTH, HEIGHT), "black")
    draw = ImageDraw.Draw(image)
    f = font(size)
    line_h = size + 6
    y = (HEIGHT - line_h * len(lines)) // 2
    for line in lines:
        w = draw.textlength(line, font=f)
        draw.text(((WIDTH - w) / 2, y), line, font=f, fill="white")
        y += line_h
    print(" | ".join(lines))
    show(image)


# turn the backlight on or off
def backlight(on):
    if HAS_SCREEN:
        _light.value = on


def pressed():
    return HAS_SCREEN and not _button.value


# block until the top button is pressed and released
def wait_for_button():
    if not HAS_SCREEN:
        input("press Enter ")
        return
    while not pressed():
        time.sleep(0.05)
    while pressed():
        time.sleep(0.05)


# sleep, return True early if the button is pressed
def wait_or_button(seconds):
    end = time.time() + seconds
    while time.time() < end:
        if pressed():
            while pressed():
                time.sleep(0.05)
            return True
        time.sleep(0.1)
    return False
