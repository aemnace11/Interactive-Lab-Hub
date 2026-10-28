import argparse
import json
from datetime import datetime, timedelta

import config

NIGHTS = {
    "guilty": [(0, "start"), (5, "nobody"), (190, "cat elsewhere"), (192, "cat in zone"), (194, "nobody"),
               (320, "cat in zone"), (321, "cat elsewhere"), (325, "nobody"), (480, "end")],
    "suspicious": [(0, "start"), (5, "nobody"), (200, "cat in zone"), (200.33, "nobody"), (480, "end")],
    "quiet": [(0, "start"), (5, "nobody"), (480, "end")],
}


# write a fake night log, minutes after 11 p.m.
if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("night", choices=NIGHTS, nargs="?", default="guilty")
    night = p.parse_args().night
    config.DATA_DIR.mkdir(exist_ok=True)
    start = datetime.now().replace(hour=23, minute=0, second=0, microsecond=0)
    with open(config.LOG_FILE, "w") as f:
        for minutes, reading in NIGHTS[night]:
            t = (start + timedelta(minutes=minutes)).isoformat(timespec="seconds")
            f.write(json.dumps({"t": t, "reading": reading}) + "\n")
    print(f"wrote a {night} night to {config.LOG_FILE}")
