
from pathlib import Path
import csv
import soundfile as sf
from faster_whisper import WhisperModel
from jiwer import wer

ROOT = Path.home() / "projects/aec-research"
BASE = ROOT / "data/experiments"
OUTPUT = BASE / "stt_results"

SR = 16000

OUTPUT.mkdir(exist_ok=True)

# Use the same model for every recording.
# First run downloads the model automatically.
print("Loading Whisper model...")
model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

def load_audio(path):
    audio, sr = sf.read(str(path), dtype="float32")

    if sr != SR:
        raise ValueError(f"Expected 16kHz, got {sr}: {path}")

    if audio.ndim > 1:
        audio = audio.mean(axis=1)

    return audio

def transcribe(path):
    audio = load_audio(path)

    segments, info = model.transcribe(
        audio,
        language="en",
        beam_size=5,
        vad_filter=False
    )

    text = " ".join(segment.text.strip() for segment in segments)
    return text.strip()

# Read original human ground-truth transcripts.
manifest_path = ROOT / "data/human_manifest.csv"

with open(manifest_path, newline="", encoding="utf-8") as f:
    human_manifest = list(csv.DictReader(f))

results = []

for row in human_manifest:
    pair_id = row["audio_id"]
    reference = row["transcript"].strip()

    conditions = {
        "clean_human": (
            Path(row["audio_path"])
        ),
        "double_talk_before_aec": (
            BASE / "double_talk" / f"{pair_id}.wav"
        ),
        "double_talk_after_aec": (
            BASE / "aec_output" /
            f"{pair_id}_double_talk_after.wav"
        ),
    }

    for condition, audio_path in conditions.items():
        print(f"Transcribing {pair_id}: {condition}")

        hypothesis = transcribe(audio_path)

        results.append({
            "pair_id": pair_id,
            "condition": condition,
            "reference": reference,
            "hypothesis": hypothesis,
            "wer": wer(reference, hypothesis),
        })

        print(f"WER: {results[-1]['wer']:.3f}")

# Save individual transcription results.
csv_path = OUTPUT / "transcriptions.csv"

with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "pair_id",
            "condition",
            "reference",
            "hypothesis",
            "wer",
        ]
    )
    writer.writeheader()
    writer.writerows(results)

# Calculate average WER per condition.
print("\n========== STT EVALUATION SUMMARY ==========")

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
        f"Average WER = {sum(values) / len(values):.4f}"
    )

print("\nTotal transcriptions:", len(results))
print("Saved results:", csv_path)
