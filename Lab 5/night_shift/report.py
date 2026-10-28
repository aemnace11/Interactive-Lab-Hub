import argparse
import json
import subprocess
import sys
import time
import urllib.request

from PIL import Image, ImageDraw

import config
import screen
import summary

# ask qwen to turn the facts into the spoken report
def ask_qwen(facts):
    short = {k: facts[k] for k in ("visits", "first_visit", "last_visit", "time_in_zone", "verdict")}
    rule = "Say the treats were not approached. " if facts["visits"] == 0 else "Say how many times she visited the bowl and when. "
    prompt = (
        "Write one sentence in the voice of a police report about a cat named Korra and a bowl of treats. "
        "Use only these facts, keep every number and time exactly as given, and do not add events. "
        + rule + f"\nFacts: {json.dumps(short)}"
    )
    body = json.dumps({
        "model": config.QWEN_MODEL,
        "prompt": prompt,
        "stream": False,
        "think": False,
        "options": {"num_predict": config.QWEN_MAX_TOKENS},
    }).encode()
    req = urllib.request.Request(config.OLLAMA_URL, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=config.QWEN_TIMEOUT) as r:
        return json.loads(r.read())["response"].strip()


# qwen writes the report, template only if qwen doesn't answer
def write_report(facts):
    if facts is None:
        return summary.template(facts)
    try:
        start = time.time()
        text = ask_qwen(facts)
        print(f"qwen ({time.time() - start:.1f} s): {text}")
        return text
    except Exception as e:
        print("qwen failed:", e)
        return summary.template(facts)


def thumb(path, size):
    if path.exists():
        return Image.open(path).convert("RGB").resize(size)
    return Image.new("RGB", size, (60, 60, 60))


# before/after photos on top, verdict underneath
def morning_screen(facts):
    image = Image.new("RGB", (screen.WIDTH, screen.HEIGHT), "black")
    draw = ImageDraw.Draw(image)
    size = (114, 72)
    image.paste(thumb(config.BEFORE_PHOTO, size), (4, 4))
    image.paste(thumb(config.AFTER_PHOTO, size), (122, 4))
    small = screen.font(12)
    draw.text((6, 78), "before", font=small, fill="white")
    draw.text((124, 78), "after", font=small, fill="white")
    if facts is None:
        line1, line2 = "No log", ""
    else:
        line1 = facts["verdict"]
        line2 = f"{facts['visits']} visit{'' if facts['visits'] == 1 else 's'}, {facts['time_in_zone']}"
    colors = {"Innocent": (90, 200, 120), "Suspicious": (240, 190, 60), "Guilty": (235, 80, 70)}
    draw.text((6, 96), line1, font=screen.font(18), fill=colors.get(line1, "white"))
    draw.text((6, 118), line2, font=small, fill="white")
    return image


# read the line aloud with piper, same call as lab 3
def speak(text):
    if not (config.PIPER_DATA_DIR / f"{config.PIPER_VOICE}.onnx").exists():
        print("piper voice not found, skipping speech")
        return
    piper = subprocess.Popen(
        [sys.executable, "-m", "piper", "--model", config.PIPER_VOICE,
         "--data-dir", str(config.PIPER_DATA_DIR), "--output-raw", "--", text],
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    subprocess.run(["aplay", "-q", "-D", config.AUDIO_DEVICE, "-r", "22050", "-f", "S16_LE", "-t", "raw", "-"],
                   stdin=piper.stdout)
    piper.wait()


# morning reveal
def morning(take_photo=True):
    screen.backlight(True)
    screen.text(["Good morning.", "Reviewing the tape..."])
    if take_photo:
        try:
            import vision
            vision.snap(config.AFTER_PHOTO)
        except Exception as e:
            print("after photo failed:", e)
    facts = summary.summarize(summary.load())
    line = write_report(facts)
    print(json.dumps(facts, indent=2))
    config.REPORT_FILE.write_text(f"facts:\n{json.dumps(facts, indent=2)}\n\nqwen report:\n{line}\n")
    screen.show(morning_screen(facts), save_to=config.SCREEN_FILE)
    speak(line)
    return line


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--no-camera", action="store_true")
    a = p.parse_args()
    morning(take_photo=not a.no_camera)
