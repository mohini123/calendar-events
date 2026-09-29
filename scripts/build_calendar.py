#!/usr/bin/env python3
"""Merge every Sankashti_Chaturthi_*.ics file into one subscribable calendar.

Usage: python3 scripts/build_calendar.py [output_dir]   (default: _site)
"""
import glob
import os
import sys

HEADER = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//mohini123//Sankashti Chaturthi//EN",
    "CALSCALE:GREGORIAN",
    "METHOD:PUBLISH",
    "X-WR-CALNAME:Sankashti Chaturthi",
    "X-WR-TIMEZONE:Europe/Amsterdam",
    "REFRESH-INTERVAL;VALUE=DURATION:P1D",
    "X-PUBLISHED-TTL:P1D",
]


def read_events(path):
    """Yield (uid, dtstart, lines) for each VEVENT, keeping folded lines intact."""
    with open(path, encoding="utf-8") as f:
        lines = f.read().replace("\r\n", "\n").split("\n")
    event = None
    for line in lines:
        if line == "BEGIN:VEVENT":
            event = [line]
        elif event is not None:
            event.append(line)
            if line == "END:VEVENT":
                props = {l.split(":", 1)[0].split(";", 1)[0]: l.split(":", 1)[-1]
                         for l in event if l and not l.startswith((" ", "\t"))}
                yield props.get("UID", ""), props.get("DTSTART", ""), event
                event = None


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "_site"
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sources = sorted(glob.glob(os.path.join(root, "Sankashti_Chaturthi_*.ics")))

    events = {}
    for path in sources:
        for uid, dtstart, lines in read_events(path):
            events[uid or f"{path}:{dtstart}"] = (dtstart, lines)

    body = [l for _, lines in sorted(events.values(), key=lambda e: e[0]) for l in lines]
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "sankashti-chaturthi.ics"), "w", encoding="utf-8", newline="") as f:
        f.write("\r\n".join(HEADER + body + ["END:VCALENDAR"]) + "\r\n")
    print(f"Merged {len(events)} events from {len(sources)} files into {out_dir}/sankashti-chaturthi.ics")


if __name__ == "__main__":
    main()
