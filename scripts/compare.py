#!/usr/bin/env python3
"""Put a film next to a reference film: pace, loudness over time and one-frame-per-second contact sheets.

    python3 scripts/compare.py out/film.mp4 --ref reference.mp4    (contact sheets go to out/compare/)

Pace is the share of the picture that changes from one frame to the next: pixels whose brightness moves by more than
10%, measured on a 160x90 greyscale copy, averaged over each second. A second under 2% counts as nearly still. A frozen
frame is an exact repeat of the one before. Loudness comes from ffmpeg's EBU R128 meter.

Needs ffmpeg and ffprobe on PATH, and Python 3 with numpy and Pillow.
"""
import argparse
import json
import re
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

W, H = 160, 90


def run(cmd):
    return subprocess.run(cmd, capture_output=True, check=True, stdin=subprocess.DEVNULL)


def probe(path):
    info = json.loads(run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)]).stdout)
    video = next(s for s in info["streams"] if s["codec_type"] == "video")
    num, den = map(int, video["r_frame_rate"].split("/"))
    return {"duration": float(info["format"]["duration"]), "fps": num / den,
            "audio": any(s["codec_type"] == "audio" for s in info["streams"])}


def pace(path, fps):
    raw = run(["ffmpeg", "-v", "error", "-i", str(path), "-fps_mode", "passthrough",
               "-vf", f"scale={W}:{H}:flags=area,format=gray", "-f", "rawvideo", "-"]).stdout
    frames = np.frombuffer(raw, np.uint8).reshape(-1, H, W)
    step = np.abs(np.diff(frames.astype(np.int16), axis=0))
    changed = np.concatenate([[0.0], (step > 0.10 * 255).mean(axis=(1, 2))])
    seconds = int(len(frames) / fps)
    per_second = [float(changed[round(i * fps):round((i + 1) * fps)].mean()) for i in range(seconds)]
    return {"per_second": per_second,
            "mean": float(np.mean(per_second)) if per_second else 0.0,
            "still": sum(v < 0.02 for v in per_second),
            "seconds": seconds,
            "frozen": int((step.max(axis=(1, 2)) == 0).sum())}


def loudness(path):
    log = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128=peak=true",
                          "-f", "null", "-"], capture_output=True, text=True, stdin=subprocess.DEVNULL).stderr
    rows = [(float(t), float(m), float(s)) for t, m, s in
            re.findall(r"t:\s*([\d.]+)\s+TARGET:\S+ LUFS\s+M:\s*(-?[\d.]+|-inf)\s+S:\s*(-?[\d.]+|-inf)", log)
            if "inf" not in m + s]
    summary = log[log.rfind("Summary:"):]

    def value(label):
        found = re.search(label + r":\s*(-?[\d.]+)", summary)
        return float(found.group(1)) if found else None

    def at(t, column):
        return min(rows, key=lambda r: abs(r[0] - t))[column] if rows else None

    end = rows[-1][0] if rows else 0
    return {"start": at(0.5, 1),
            "short_term": [(t, at(t, 2)) for t in np.arange(2.5, end + 0.01, 2.5) if t >= 3],
            "integrated": value("I"), "range": value("LRA"), "true_peak": value("Peak")}


def contact_sheet(path, duration, fps, out, cols=6, width=320):
    """One frame from the middle of every second: the exact frame at 0.5 s, 1.5 s, 2.5 s..."""
    height = width * 9 // 16
    picks = "+".join(f"eq(n\\,{round((k + 0.5) * fps)})" for k in range(int(duration)))
    with tempfile.TemporaryDirectory() as tmp:
        run(["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"select='{picks}',scale={width}:{height}",
             "-fps_mode", "passthrough", f"{tmp}/%04d.png"])
        shots = sorted(Path(tmp).glob("*.png"))
        rows = (len(shots) + cols - 1) // cols
        page = Image.new("RGB", (cols * (width + 4) + 4, rows * (height + 4) + 4), "white")
        for i, shot in enumerate(shots):
            frame = Image.open(shot).convert("RGB")
            draw = ImageDraw.Draw(frame)
            draw.rectangle([0, 0, 52, 16], fill="black")
            draw.text((4, 2), f"{i + 0.5:.1f}s", fill="white")
            page.paste(frame, (4 + (i % cols) * (width + 4), 4 + (i // cols) * (height + 4)))
        page.save(out, quality=88)


def measure(path, out_dir):
    info = probe(path)
    result = {"name": Path(path).name, "duration": info["duration"], **pace(path, info["fps"])}
    result["loudness"] = loudness(path) if info["audio"] else None
    sheet = out_dir / f"{Path(path).stem}-sheet.jpg"
    contact_sheet(path, info["duration"], info["fps"], sheet)
    result["sheet"] = str(sheet)
    return result


def fmt(value, unit="", digits=1):
    return "–" if value is None else f"{value:.{digits}f}{unit}"


def report(films):
    rows = [
        ("Length", lambda f: fmt(f["duration"], " s")),
        ("Change per second", lambda f: fmt(f["mean"], "", 3)),
        ("Nearly still seconds", lambda f: f"{f['still']} of {f['seconds']}"),
        ("Frozen frames", lambda f: str(f["frozen"])),
        ("Loudness at 0.5 s", lambda f: fmt(f["loudness"] and f["loudness"]["start"], " LUFS")),
        ("Integrated loudness", lambda f: fmt(f["loudness"] and f["loudness"]["integrated"], " LUFS")),
        ("Loudness range", lambda f: fmt(f["loudness"] and f["loudness"]["range"], " LU")),
        ("True peak", lambda f: fmt(f["loudness"] and f["loudness"]["true_peak"], " dBTP")),
    ]
    widths = [max(len(f["name"]), 16) for f in films]
    print(f"{'':24}" + "".join(f"{f['name']:>{w + 2}}" for f, w in zip(films, widths)))
    for label, cell in rows:
        print(f"{label:24}" + "".join(f"{cell(f):>{w + 2}}" for f, w in zip(films, widths)))
    for f in films:
        print(f"\n{f['name']}")
        print("  change per second:", " ".join(f"{v:.2f}" for v in f["per_second"]))
        if f["loudness"]:
            print("  short-term loudness every 2.5 s:",
                  " ".join(f"{t:g}s {v:.1f}" for t, v in f["loudness"]["short_term"]))
        print("  contact sheet:", f["sheet"])


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("film")
    ap.add_argument("--ref", help="a reference film to compare against")
    ap.add_argument("--out", help="folder for the contact sheets (default: compare/ next to the film)")
    args = ap.parse_args()
    out_dir = Path(args.out) if args.out else Path(args.film).resolve().parent / "compare"
    out_dir.mkdir(parents=True, exist_ok=True)
    report([measure(p, out_dir) for p in [args.film] + ([args.ref] if args.ref else [])])


if __name__ == "__main__":
    main()
