
from pathlib import Path
import csv

ROOT = Path.home() / "projects/aec-research"

with open(ROOT / "data/human_manifest_corrected.csv",
          newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

for i, row in enumerate(rows, 1):
    print(f"\nPAIR {i:03d} | {row['audio_id']}")
    print(row["transcript"])
