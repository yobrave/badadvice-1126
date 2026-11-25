"""Worst-advice one-liner builder.

Loads entry.txt from the script folder, audits it against the
140-character gate for this bounty, and emits the audited line into
$MAKEFUN_OUTPUT_DIR with a JSON summary on stdout.
"""
import json
import os
import pathlib
import sys

FOLDER = pathlib.Path(__file__).resolve().parent
CAP = 140
BADGE = "advice-desk: confidently wrong, tidily phrased"
FOLLOWUP = "results may vary; the assistant takes no responsibility"


def audit(text):
    out = {"chars": len(text), "blank": not bool(text.strip())}
    out["ok"] = (not out["blank"]) and out["chars"] <= CAP and out["chars"] >= 1
    return out


def emit(text):
    where = os.environ.get("MAKEFUN_OUTPUT_DIR") or "out"
    path = pathlib.Path(where)
    path.mkdir(parents=True, exist_ok=True)
    payload = (text + "\n").encode("utf-8")
    (path / "entry.txt").write_bytes(payload)
    if (path / "entry.txt").read_bytes() != payload:
        sys.exit("emit mismatch")


def main():
    text = (FOLDER / "entry.txt").read_bytes().decode("utf-8").strip("\r\n")
    result = audit(text)
    emit(text)
    result["badge"] = BADGE
    result["verdict"] = "go" if result["ok"] else "no"
    sys.stdout.write(json.dumps(result) + "\n")


main()
