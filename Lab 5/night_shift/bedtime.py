import json
import time
from datetime import datetime

import config
import screen
import vision


# hand-off: press button, find bowl, save zone and before photo
def bedtime():
    config.DATA_DIR.mkdir(exist_ok=True)
    screen.backlight(True)
    screen.text(["Korra's Night Shift", "Set the bowl,", "press the button"])
    while True:
        screen.wait_for_button()
        screen.text(["Looking for", "the bowl..."])
        frame = vision.snap(config.BEFORE_PHOTO)
        zone = vision.find_bowl(frame)
        if zone:
            break
        screen.text(["Can't find the bowl.", "Move it or the camera,", "then press again"], size=16)
    config.ZONE_FILE.write_text(json.dumps({"zone": zone, "set_at": datetime.now().isoformat(timespec="seconds")}))
    config.LOG_FILE.unlink(missing_ok=True)
    screen.text(["Bowl located.", "Korra's on watch."])
    time.sleep(5)
    screen.backlight(False)
    return zone


if __name__ == "__main__":
    print(bedtime())
