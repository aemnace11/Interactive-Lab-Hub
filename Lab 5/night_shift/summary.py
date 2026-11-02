import json
import random
from datetime import datetime

import config


# read the log into (time, reading) pairs
def load(path=config.LOG_FILE):
    if not path.exists():
        return []
    entries = []
    for line in path.read_text().splitlines():
        if line.strip():
            row = json.loads(line)
            entries.append((datetime.fromisoformat(row["t"]), row["reading"]))
    return entries


def clock(t):
    return t.strftime("%I:%M %p").lstrip("0").replace("AM", "a.m.").replace("PM", "p.m.")


def duration(seconds):
    if seconds < 60:
        return f"{round(seconds)} seconds"
    minutes = round(seconds / 60)
    return f"about {minutes} minute" + ("" if minutes == 1 else "s")


# count visits and time in zone in code, not in qwen
def summarize(entries):
    if len(entries) < 2:
        return None
    visits = []
    for i, (t, reading) in enumerate(entries):
        if reading == "cat in zone":
            end = entries[i + 1][0] if i + 1 < len(entries) else t
            visits.append((t, end))
    total = sum((end - start).total_seconds() for start, end in visits)
    if not visits:
        verdict = "Innocent"
    elif total < config.GUILTY_SECONDS:
        verdict = "Suspicious"
    else:
        verdict = "Guilty"
    return {
        "night_start": clock(entries[0][0]),
        "night_end": clock(entries[-1][0]),
        "visits": len(visits),
        "first_visit": clock(visits[0][0]) if visits else None,
        "last_visit": clock(visits[-1][0]) if visits else None,
        "time_in_zone": duration(total),
        "seen_elsewhere": any(r == "cat elsewhere" for _, r in entries),
        "verdict": verdict,
    }


# police-report lines, filled in with the facts from the log
OPENERS = ["Overnight report.", "Incident log.", "Case file."]
GUILTY = [
    "The suspect approached the treat bowl {visits} {times} {when}, spending {time} at the scene.",
    "Korra was observed at the treats {visits} {times} {when}, for {time} in total.",
    "The suspect returned to the scene {visits} {times} {when} and stayed {time}.",
]
SUSPICIOUS = [
    "The suspect was spotted at the treat bowl {visits} {times} {when}, but only for {time}. She may have been passing through.",
    "Korra entered the treat zone {visits} {times} {when} and left after {time}. Not enough time to confirm a theft.",
]
QUIET = [
    "Quiet night. The treats were not approached.",
    "No activity at the treat bowl. The evidence is untouched.",
]


# fill a random police-report line with the facts
def template(facts):
    if facts is None:
        return "No report. The night shift did not record a night."
    opener = random.choice(OPENERS)
    if facts["visits"] == 0:
        extra = " The suspect was seen elsewhere but kept away from the treats." if facts["seen_elsewhere"] else ""
        return f"{opener} {random.choice(QUIET)}{extra}"
    when = (f"at {facts['first_visit']}" if facts["visits"] == 1
            else f"between {facts['first_visit']} and {facts['last_visit']}")
    lines = GUILTY if facts["verdict"] == "Guilty" else SUSPICIOUS
    body = random.choice(lines).format(
        visits=facts["visits"],
        times="time" if facts["visits"] == 1 else "times",
        when=when,
        time=facts["time_in_zone"],
    )
    return f"{opener} {body} Verdict: {facts['verdict'].lower()}."
