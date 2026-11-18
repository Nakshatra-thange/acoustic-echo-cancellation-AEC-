
from pathlib import Path
import csv
import re
import string

import soundfile as sf
from faster_whisper import WhisperModel
from jiwer import wer

ROOT = Path.home() / "projects/aec-research"
BASE = ROOT / "data/experiments"
OUTPUT = BASE / "stt_results"
OUTPUT.mkdir(exist_ok=True)

SR = 16000

print("Loading Whisper model...")
model = WhisperModel("small", device="cpu", compute_type="int8")


def normalize(text):
    text = text.lower()

    # Normalize common title abbreviations.
    text = re.sub(r"\bmr\.?\b", "mister", text)
    text = re.sub(r"\bmrs\.?\b", "missus", text)

    # Remove punctuation.
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Normalize whitespace.
    text = re.sub(r"\s+", " ", text).strip()

    return text


def transcribe(path):
    audio, sr = sf.read(str(path), dtype="float32")

    if sr != SR:
        raise ValueError(f"Expected 16kHz: {path}")

    if audio.ndim > 1:
        audio = audio.mean(axis=1)

    segments, _ = model.transcribe(
        audio,
        language="en",
        beam_size=5,
        vad_filter=False
    )

    return " ".join(
        segment.text.strip() for segment in segments
    ).strip()


with open(ROOT / "data/human_manifest_reviewed.csv", newline="", encoding="utf-8") as f:
    manifest = list(csv.DictReader(f))

results = []

for index, row in enumerate(manifest, start=1):
    pair_id = f"pair_{index:03d}"
    reference = row["transcript"].strip()

    conditions = {
        "clean_human": Path(row["audio_path"]),
        "double_talk_before_aec":
            BASE / "double_talk" / f"{pair_id}.wav",
        "double_talk_after_aec":
            BASE / "aec_output" /
            f"{pair_id}_double_talk_after.wav",
    }

    for condition, path in conditions.items():
        print(f"\n{pair_id}: {condition}")

        if not path.exists():
            raise FileNotFoundError(path)

        hypothesis = transcribe(path)

        normalized_reference = normalize(reference)
        normalized_hypothesis = normalize(hypothesis)

        error = wer(
            normalized_reference,
            normalized_hypothesis
        )

        results.append({
            "pair_id": pair_id,
            "condition": condition,
            "reference": reference,
            "hypothesis": hypothesis,
            "normalized_reference": normalized_reference,
            "normalized_hypothesis": normalized_hypothesis,
            "wer": error,
        })

        print(f"WER: {error:.4f}")

csv_path = OUTPUT / "transcriptions_normalized.csv"

with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("\n========== NORMALIZED WER SUMMARY ==========")

for condition in [
    "clean_human",
    "double_talk_before_aec",
    "double_talk_after_aec",
]:
    values = [
        r["wer"] for r in results
        if r["condition"] == condition
    ]

    print(
        f"{condition}: "
        f"{sum(values) / len(values):.4f}"
    )

print("\nTotal transcriptions:", len(results))
print("Saved:", csv_path)
