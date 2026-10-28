import json
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


# plain report used when qwen is skipped or gets the facts wrong
def template(facts):
    if facts is None:
        return "No report. The night shift did not record a night."
    if facts["visits"] == 0:
        extra = " The suspect was seen elsewhere but kept away from the treats." if facts["seen_elsewhere"] else ""
        return "Overnight report. Quiet night. The treats were not approached." + extra
    times = "time" if facts["visits"] == 1 else "times"
    when = (f"at {facts['first_visit']}" if facts["visits"] == 1
            else f"first at {facts['first_visit']} and last at {facts['last_visit']}")
    return (f"Overnight report. The suspect entered the treat zone {facts['visits']} {times}, "
            f"{when}, for {facts['time_in_zone']} in total. Verdict: {facts['verdict'].lower()}.")
