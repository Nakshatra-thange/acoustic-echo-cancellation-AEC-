
from pathlib import Path
import soundfile as sf
import numpy as np
from pywebrtc_audio import AudioProcessor

ROOT = Path.home() / "projects/aec-research"
BASE = ROOT / "data/experiments"

SR = 16000

def load(path):
    audio, sr = sf.read(str(path), dtype="float32")
    if sr != SR:
        raise ValueError(f"Expected 16kHz, got {sr}")
    return audio

# Agent echo in microphone, with no human voice
near = load(BASE / "far_end_only/pair_001.wav")

# Original agent playback reference
far = load(BASE / "references/pair_001.wav")

processor = AudioProcessor(
    sample_rate=SR,
    num_channels=1,
    echo_cancellation=True,
    noise_suppression=False,
    auto_gain_control=False,
    stream_delay_ms=40,
)

cleaned = processor.process(near, far)

output = BASE / "aec_output"
output.mkdir(exist_ok=True)

sf.write(output / "far_end_before.wav", near, SR)
sf.write(output / "far_end_after.wav", cleaned, SR)

print("Before AEC RMS:", np.sqrt(np.mean(near ** 2)))
print("After AEC RMS:", np.sqrt(np.mean(cleaned ** 2)))
print("Saved both recordings in:", output)
