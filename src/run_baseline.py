
from pathlib import Path
import csv
import numpy as np
import soundfile as sf
from pywebrtc_audio import AudioProcessor

ROOT = Path.home() / "projects/aec-research"
BASE = ROOT / "data/experiments"
OUTPUT = BASE / "aec_output"

SR = 16000
DELAY_MS = 40

OUTPUT.mkdir(exist_ok=True)

def load_audio(path):
    audio, sr = sf.read(str(path), dtype="float32")

    if sr != SR:
        raise ValueError(f"{path}: expected 16000 Hz, got {sr}")

    if audio.ndim > 1:
        audio = audio.mean(axis=1)

    return audio

def rms(audio):
    return float(np.sqrt(np.mean(audio ** 2)))

def process_aec(near, far):
    processor = AudioProcessor(
        sample_rate=SR,
        num_channels=1,
        echo_cancellation=True,
        noise_suppression=False,
        high_pass_filter=False,
        auto_gain_control=False,
        stream_delay_ms=DELAY_MS,
    )

    return processor.process(near, far)

results = []

for pair_num in range(1, 21):
    pair_id = f"pair_{pair_num:03d}"

    far = load_audio(BASE / "references" / f"{pair_id}.wav")

    for scenario in ["far_end_only", "double_talk"]:
        near = load_audio(
            BASE / scenario / f"{pair_id}.wav"
        )

        if len(near) != len(far):
            raise ValueError(f"Length mismatch: {pair_id}")

        cleaned = process_aec(near, far)

        sf.write(
            OUTPUT / f"{pair_id}_{scenario}_before.wav",
            near,
            SR
        )

        sf.write(
            OUTPUT / f"{pair_id}_{scenario}_after.wav",
            cleaned,
            SR
        )

        before_rms = rms(near)
        after_rms = rms(cleaned)

        reduction_db = 20 * np.log10(
            max(after_rms, 1e-12) /
            max(before_rms, 1e-12)
        )

        results.append({
            "pair_id": pair_id,
            "scenario": scenario,
            "before_rms": before_rms,
            "after_rms": after_rms,
            "level_change_db": reduction_db,
        })

    print(f"Processed {pair_id}")

csv_path = OUTPUT / "baseline_results.csv"

with open(csv_path, "w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "pair_id",
            "scenario",
            "before_rms",
            "after_rms",
            "level_change_db",
        ],
    )
    writer.writeheader()
    writer.writerows(results)

print("\nBATCH EVALUATION COMPLETE")
print(f"Total recordings processed: {len(results)}")
print(f"Results saved to: {csv_path}")

for scenario in ["far_end_only", "double_talk"]:
    values = [
        r["level_change_db"]
        for r in results
        if r["scenario"] == scenario
    ]

    print(
        f"{scenario}: "
        f"average level change = {np.mean(values):.2f} dB"
    )
