import cv2
from ultralytics import YOLO

import config

_model = None


# load yolo once
def model():
    global _model
    if _model is None:
        _model = YOLO(str(config.MODEL_PATH), task="detect")
    return _model


# open camera, let exposure settle, grab one frame
def snap(path=None):
    cam = cv2.VideoCapture(config.CAMERA_INDEX)
    frame = None
    try:
        for _ in range(config.WARMUP_FRAMES):
            ok, f = cam.read()
            if ok:
                frame = f
    finally:
        cam.release()
    if frame is None:
        raise RuntimeError("camera returned no frame")
    if path:
        cv2.imwrite(str(path), frame)
    return frame


# run yolo, return (class name, confidence, box) per detection
def detect(frame):
    r = model()(frame, verbose=False)[0]
    return [(r.names[int(b.cls)], float(b.conf), b.xyxy[0].tolist()) for b in r.boxes]


# find the bowl and pad its box into the zone
def find_bowl(frame):
    h, w = frame.shape[:2]
    bowls = [d for d in detect(frame) if d[0] == "bowl" and d[1] >= config.BOWL_CONF]
    if not bowls:
        return None
    x1, y1, x2, y2 = max(bowls, key=lambda d: d[1])[2]
    px = (x2 - x1) * config.ZONE_PAD / 2
    py = (y2 - y1) * config.ZONE_PAD / 2
    return [max(0, x1 - px), max(0, y1 - py), min(w, x2 + px), min(h, y2 + py)]


# true if two boxes overlap
def overlaps(a, b):
    return a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]


# interpreter: one frame -> one reading
def interpret(frame, zone):
    cats = [box for name, conf, box in detect(frame)
            if name in config.CAT_CLASSES and conf >= config.CAT_CONF]
    if not cats:
        return "nobody"
    if any(overlaps(c, zone) for c in cats):
        return "cat in zone"
    return "cat elsewhere"
