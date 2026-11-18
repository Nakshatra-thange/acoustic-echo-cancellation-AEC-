
from pathlib import Path
import numpy as np
import pandas as pd
import soundfile as sf

ROOT = Path.home() / "projects" / "aec-research"

HUMAN_MANIFEST = ROOT / "data/human_manifest.csv"
AGENT_MANIFEST = ROOT / "data/agent_manifest.csv"

OUTPUT_DIR = ROOT / "data/simulated_mic"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SAMPLE_RATE = 16000
ECHO_DELAY_MS = 500
ECHO_GAIN = 0.3

human_df = pd.read_csv(HUMAN_MANIFEST)
agent_df = pd.read_csv(AGENT_MANIFEST)

def load_audio(path):
    audio, sr = sf.read(path)

    if sr != SAMPLE_RATE:
        raise ValueError(f"Expected {SAMPLE_RATE} Hz, got {sr}")

    if audio.ndim > 1:
        audio = np.mean(audio, axis=1)

    return audio.astype(np.float32)

def normalize_peak(audio, target=0.7):
    peak = np.max(np.abs(audio))

    if peak == 0:
        return audio

    return audio * (target / peak)

records = []

for index, human_row in human_df.iterrows():
    agent_row = agent_df.iloc[index]

    human = load_audio(human_row["audio_path"])

    agent_path = (
        ROOT / "data/agent_audio_16k" /
        (str(agent_row["audio_id"]) + ".wav")
    )
    agent = load_audio(str(agent_path))

    # Repeat agent speech to cover the human recording.
    repetitions = int(np.ceil(len(human) / len(agent)))
    agent_extended = np.tile(agent, repetitions)[:len(human)]

    # Apply a 500 ms delay.
    delay_samples = int(SAMPLE_RATE * ECHO_DELAY_MS / 1000)

    delayed_agent = np.zeros_like(human)

    if delay_samples < len(human):
        delayed_agent[delay_samples:] = (
            agent_extended[:-delay_samples]
        )

    # Mix human voice and delayed agent voice.
    mic_audio = human + ECHO_GAIN * delayed_agent

    # Prevent clipping.
    mic_audio = normalize_peak(mic_audio)

    output_name = f"mic_{index + 1:03d}.wav"
    output_path = OUTPUT_DIR / output_name

    sf.write(
        str(output_path),
        mic_audio,
        SAMPLE_RATE,
        subtype="PCM_16"
    )

    records.append({
        "recording_id": output_name,
        "human_audio_id": human_row["audio_id"],
        "agent_audio_id": agent_row["audio_id"],
        "human_transcript": human_row["transcript"],
        "agent_transcript": agent_row["transcript"],
        "echo_delay_ms": ECHO_DELAY_MS,
        "echo_gain": ECHO_GAIN,
        "sample_rate": SAMPLE_RATE,
        "duration_seconds": len(mic_audio) / SAMPLE_RATE,
        "audio_path": str(output_path),
    })

manifest = pd.DataFrame(records)
manifest.to_csv(OUTPUT_DIR / "manifest.csv", index=False)

print("Simulated recordings created:", len(records))
print("Saved to:", OUTPUT_DIR)
print("\nFirst 5 recordings:")
print(manifest[[
    "recording_id",
    "duration_seconds",
    "echo_delay_ms",
    "echo_gain"
]].head())
