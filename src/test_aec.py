
from pathlib import Path
import numpy as np
import soundfile as sf
from pywebrtc_audio import AudioProcessor

ROOT = Path.home() / "projects" / "aec-research"
BASE = ROOT / "data/experiments"
OUTPUT = BASE / "aec_output"

SR = 16000
DELAY_MS = 40

def load_audio(path):
    audio, sr = sf.read(str(path), dtype="float32")

    if sr != SR:
        raise ValueError(f"Expected {SR} Hz, got {sr}")

    if audio.ndim > 1:
        audio = audio.mean(axis=1)

    return audio

# Microphone input: human + echo
near = load_audio(BASE / "double_talk/pair_001.wav")

# Reference: what the agent speaker played
far = load_audio(BASE / "references/pair_001.wav")

# AEC3 processor
processor = AudioProcessor(
    sample_rate=SR,
    num_channels=1,
    echo_cancellation=True,
    noise_suppression=False,
    high_pass_filter=False,
    auto_gain_control=False,
    stream_delay_ms=DELAY_MS,
)

# Process the microphone using the agent reference
cleaned = processor.process(near, far)

# Save output
OUTPUT.mkdir(parents=True, exist_ok=True)

sf.write(
    str(OUTPUT / "pair_001_aec.wav"),
    cleaned,
    SR
)

# Save original input for comparison
sf.write(
    str(OUTPUT / "pair_001_before_aec.wav"),
    near,
    SR
)

print("AEC processing completed!")
print("Input duration:", round(len(near) / SR, 2), "seconds")
print("Output duration:", round(len(cleaned) / SR, 2), "seconds")

print("\nRMS comparison:")
print("Before AEC:", round(float(np.sqrt(np.mean(near**2))), 5))
print("After AEC:", round(float(np.sqrt(np.mean(cleaned**2))), 5))
print("Output saved:", OUTPUT / "pair_001_aec.wav")
