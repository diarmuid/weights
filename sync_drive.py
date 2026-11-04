#!/usr/bin/env python3
"""Copy the newest CSV from the public Google Drive folder into data/latest.csv."""

import shutil
import sys
import tempfile
from pathlib import Path

import gdown

FOLDER_ID = "1Z4XPVw74dzL7jtgqiXExs_6G8nJBfBU5"
DEST = Path(__file__).resolve().parent / "data" / "latest.csv"
HEADER_MARKER = "Exercise Name"


def is_lift_log(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8-sig", errors="replace") as handle:
            return HEADER_MARKER in handle.readline()
    except OSError:
        return False


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "weights"
        gdown.download_folder(id=FOLDER_ID, output=str(out), quiet=True, use_cookies=False)
        csvs = [p for p in out.rglob("*.csv") if p.is_file() and is_lift_log(p)]
        if not csvs:
            print("No lift log CSV files found in the Drive folder.", file=sys.stderr)
            return 1

        newest = max(csvs, key=lambda p: p.stat().st_mtime)
        print(f"Newest CSV: {newest.name} ({newest.stat().st_size} bytes)")

        DEST.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(newest, DEST)
        print(f"Wrote {DEST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())