
from pathlib import Path
import csv

ROOT = Path.home() / "projects/aec-research"

MANIFEST = ROOT / "data/human_manifest.csv"
LIBRISPEECH = ROOT / "data/raw/librispeech/LibriSpeech/dev-clean"

OUTPUT = ROOT / "data/human_manifest_corrected.csv"

# Load the original LibriSpeech transcripts.
transcript_map = {}

for transcript_file in LIBRISPEECH.rglob("*.trans.txt"):
    with open(transcript_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            parts = line.split(maxsplit=1)

            if len(parts) != 2:
                continue

            audio_id, transcript = parts
            transcript_map[audio_id] = transcript

print("Original LibriSpeech transcripts loaded:", len(transcript_map))

# Read our existing manifest.
with open(MANIFEST, newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
    fieldnames = rows[0].keys()

corrected = 0
missing = []

for row in rows:
    audio_id = row["audio_id"]

    if audio_id not in transcript_map:
        missing.append(audio_id)
        continue

    original = row["transcript"]
    official = transcript_map[audio_id]

    if original != official:
        corrected += 1
        print(f"\nCorrecting: {audio_id}")
        print("Old:", original)
        print("New:", official)

    row["transcript"] = official

# Save a separate corrected manifest.
with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("\n========== TRANSCRIPT AUDIT ==========")
print("Manifest recordings:", len(rows))
print("Transcripts corrected:", corrected)
print("Missing transcript IDs:", len(missing))

if missing:
    print("Missing IDs:", missing)

print("\nCorrected manifest saved to:")
print(OUTPUT)
