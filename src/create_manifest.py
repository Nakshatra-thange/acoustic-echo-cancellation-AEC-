
from pathlib import Path
import soundfile as sf
import pandas as pd

PROJECT_ROOT = Path.home() / "projects" / "aec-research"
DATASET_DIR = PROJECT_ROOT / "data/raw/librispeech/LibriSpeech/dev-clean"
OUTPUT_FILE = PROJECT_ROOT / "data/human_manifest.csv"

records = []

# Find every transcript file
for transcript_file in DATASET_DIR.rglob("*.trans.txt"):

    # Read each line: audio filename + transcript
    for line in transcript_file.read_text().splitlines():
        audio_id, transcript = line.split(" ", 1)

        audio_file = transcript_file.parent / f"{audio_id}.flac"

        if not audio_file.exists():
            continue

        # Read audio metadata
        info = sf.info(str(audio_file))

        records.append({
            "audio_id": audio_id,
            "speaker_id": audio_id.split("-")[0],
            "audio_path": str(audio_file),
            "transcript": transcript.strip(),
            "duration_seconds": info.duration,
            "sample_rate": info.samplerate,
        })

# Sort and select the first 20 recordings
df = pd.DataFrame(records)
df = df.sort_values("audio_id").head(20)

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_FILE, index=False)

print(f"Total recordings in dataset: {len(records)}")
print(f"Selected recordings: {len(df)}")
print(f"Manifest saved to: {OUTPUT_FILE}")
print("\nFirst 5 recordings:")
print(df[["audio_id", "duration_seconds", "transcript"]].head())
