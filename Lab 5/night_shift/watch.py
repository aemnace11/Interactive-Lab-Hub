import json
from datetime import datetime

import config
import screen
import vision


def now():
    return datetime.now().isoformat(timespec="seconds")


def write(t, reading):
    with open(config.LOG_FILE, "a") as f:
        f.write(json.dumps({"t": t, "reading": reading}) + "\n")
    print(t, reading)


# night shift: sample every SAMPLE_SECONDS, log a reading once it holds for CONFIRM_SAMPLES
def watch(zone):
    logged, candidate, count, start = None, None, 0, None
    write(now(), "start")
    try:
        while True:
            t = now()
            try:
                reading = vision.interpret(vision.snap(), zone)
            except Exception as e:
                print(t, "sample failed:", e)
                reading = None
            if reading is not None:
                if reading == candidate:
                    count += 1
                else:
                    candidate, count, start = reading, 1, t
                if candidate != logged and count >= config.CONFIRM_SAMPLES:
                    write(start, candidate)
                    logged = candidate
            if screen.wait_or_button(config.SAMPLE_SECONDS):
                break
    except KeyboardInterrupt:
        pass
    write(now(), "end")


if __name__ == "__main__":
    watch(json.loads(config.ZONE_FILE.read_text())["zone"])
