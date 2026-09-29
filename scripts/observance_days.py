#!/usr/bin/env python3
"""Rewrite Sankashti Chaturthi .ics files as all-day events on the observance day.

Sankashti Chaturthi is kept on the day when Krishna paksha Chaturthi tithi is
running at moonrise. This script recomputes the tithi window and the moonrise
for Amsterdam, then replaces each timed VEVENT with an all-day event on that
day and puts the local moonrise time in the description.

The existing DTSTART of each event is only used to find which Chaturthi it
refers to, so the script can be re-run on already converted files.

Usage: python3 scripts/observance_days.py Sankashti_Chaturthi_*.ics
Requires: pip install ephem
"""

import math
import re
import sys
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import ephem

TZ = ZoneInfo("Europe/Amsterdam")
LAT, LON = "52.3676", "4.9041"  # Amsterdam

# Krishna paksha Chaturthi: Moon-Sun elongation between 216 and 228 degrees.
TITHI_START, TITHI_END = 216.0, 228.0


def elongation(dt):
    d = ephem.Date(dt)
    moon, sun = ephem.Moon(d), ephem.Sun(d)
    lm = ephem.Ecliptic(moon, epoch=d).lon
    ls = ephem.Ecliptic(sun, epoch=d).lon
    return math.degrees(lm - ls) % 360.0


def crossing(target, near):
    """UTC datetime when the elongation reaches `target`, searching around `near`."""
    lo, hi = near - timedelta(days=3), near + timedelta(days=3)
    # Walk forward in steps to bracket the crossing, then bisect.
    t = lo
    step = timedelta(hours=2)
    prev = (elongation(t) - target + 180) % 360 - 180
    while t < hi:
        nxt = t + step
        cur = (elongation(nxt) - target + 180) % 360 - 180
        if prev < 0 <= cur:
            a, b = t, nxt
            while b - a > timedelta(seconds=1):
                m = a + (b - a) / 2
                if (elongation(m) - target + 180) % 360 - 180 < 0:
                    a = m
                else:
                    b = m
            return b.replace(microsecond=0)
        t, prev = nxt, cur
    raise ValueError(f"no crossing of {target} near {near}")


def moonrise(day):
    """Moonrise (UTC) on the given local calendar day in Amsterdam, or None."""
    obs = ephem.Observer()
    obs.lat, obs.lon, obs.elevation = LAT, LON, 0
    start = datetime(day.year, day.month, day.day, tzinfo=TZ).astimezone(timezone.utc)
    obs.date = ephem.Date(start.replace(tzinfo=None))
    try:
        rise = obs.next_rising(ephem.Moon()).datetime().replace(tzinfo=timezone.utc)
    except (ephem.AlwaysUpError, ephem.NeverUpError):
        return None
    return rise if rise.astimezone(TZ).date() == day else None


def observance(hint):
    """Return (day, tithi_start, tithi_end, moonrise) for the Chaturthi near `hint`."""
    start = crossing(TITHI_START, hint)
    end = crossing(TITHI_END, start + timedelta(hours=24))
    first, last = start.astimezone(TZ).date(), end.astimezone(TZ).date()
    days = [first + timedelta(days=i) for i in range((last - first).days + 1)]
    candidates = []
    for d in days:
        rise = moonrise(d)
        if rise and start <= rise < end:
            candidates.append((d, rise))
    if candidates:
        # If Chaturthi is present at moonrise on two days, the first day is taken.
        day, rise = candidates[0]
    else:
        # Chaturthi falls entirely between two moonrises. Take the first day:
        # Chaturthi begins after that evening's moonrise, so the Moon is up
        # during Chaturthi that night, while on the next day the tithi is over
        # before the Moon rises. Flagged for a manual check.
        day = first
        rise = moonrise(day)
        print(f"WARNING: no moonrise inside Chaturthi {start}..{end}, using {day}", file=sys.stderr)
    return day, start, end, rise


def fold(line):
    out = []
    while len(line.encode()) > 75:
        cut = 75 if not out else 74
        out.append(line[:cut])
        line = line[cut:]
    out.append(line)
    return "\r\n ".join(out)


def fmt(dt):
    return dt.astimezone(TZ).strftime("%H:%M, %b %d")


def convert(path, stamp):
    text = open(path, encoding="utf-8").read()
    unfolded = re.sub(r"\r?\n[ \t]", "", text)
    lines = unfolded.splitlines()
    out, event = [], None
    for line in lines:
        if line == "BEGIN:VEVENT":
            event = {}
            continue
        if line == "END:VEVENT":
            hint = event.get("DTSTART")
            if hint.startswith("VALUE=DATE:"):
                d = hint.split(":")[-1]
                hint_dt = datetime.strptime(d, "%Y%m%d").replace(tzinfo=timezone.utc)
            else:
                hint_dt = datetime.strptime(hint.split(":")[-1], "%Y%m%dT%H%M%SZ").replace(
                    tzinfo=timezone.utc
                )
            day, start, end, rise = observance(hint_dt)
            seq = int(event.get("SEQUENCE", "0"))
            if not event.get("DTSTART", "").startswith("VALUE=DATE"):
                seq += 1
            desc = (
                f"Sankashti Chaturthi: {event['SUMMARY']}\\n"
                f"Moonrise in Amsterdam: {fmt(rise)}\\n"
                f"Chaturthi tithi: {fmt(start)} to {fmt(end)} (Europe/Amsterdam)"
            )
            props = [
                ("SUMMARY", event["SUMMARY"]),
                ("DTSTART;VALUE=DATE", day.strftime("%Y%m%d")),
                ("DTEND;VALUE=DATE", (day + timedelta(days=1)).strftime("%Y%m%d")),
                ("DTSTAMP", stamp),
                ("UID", event["UID"]),
                ("DESCRIPTION", desc.replace(",", "\\,")),
                ("STATUS", event.get("STATUS", "CONFIRMED")),
                ("SEQUENCE", str(seq)),
                ("TRANSP", "TRANSPARENT"),
            ]
            out.append("BEGIN:VEVENT")
            out += [fold(f"{k}:{v}") for k, v in props]
            out.append("END:VEVENT")
            print(f"{path}: {event['SUMMARY']:32} {day}  moonrise {fmt(rise)}")
            event = None
            continue
        if event is not None:
            key, _, value = line.partition(":")
            name = key.split(";")[0]
            event[name] = (key[len(name) + 1 :] + ":" + value) if name == "DTSTART" and ";" in key else value
            continue
        if line.startswith("X-WR-TIMEZONE"):
            continue
        out.append(line)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write("\r\n".join(out) + "\r\n")


if __name__ == "__main__":
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for p in sys.argv[1:]:
        convert(p, stamp)
