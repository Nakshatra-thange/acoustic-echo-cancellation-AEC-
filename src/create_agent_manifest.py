
from pathlib import Path
import soundfile as sf
import pandas as pd

ROOT = Path.home() / "projects" / "aec-research"
AUDIO_DIR = ROOT / "data/agent_audio"
SENTENCES_FILE = ROOT / "data/agent_sentences.txt"
OUTPUT_FILE = ROOT / "data/agent_manifest.csv"

sentences = [
    line.strip()
    for line in SENTENCES_FILE.read_text().splitlines()
    if line.strip()
]

audio_files = sorted(AUDIO_DIR.glob("*.wav"))

if len(audio_files) != len(sentences):
    raise ValueError(
        f"Found {len(audio_files)} audio files "
        f"but {len(sentences)} sentences."
    )

records = []

for audio_file, sentence in zip(audio_files, sentences):
    info = sf.info(str(audio_file))

    records.append({
        "audio_id": audio_file.stem,
        "audio_path": str(audio_file),
        "transcript": sentence,
        "duration_seconds": info.duration,
        "sample_rate": info.samplerate,
    })

df = pd.DataFrame(records)
df.to_csv(OUTPUT_FILE, index=False)

print(f"Agent recordings: {len(df)}")
print(f"Manifest saved: {OUTPUT_FILE}")
print("\nSample records:")
print(df[["audio_id", "duration_seconds", "sample_rate", "transcript"]].head())
