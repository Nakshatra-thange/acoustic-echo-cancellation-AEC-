
from pathlib import Path
import soundfile as sf
import numpy as np
from scipy.signal import resample_poly
import math

ROOT = Path.home() / "projects" / "aec-research"
INPUT_DIR = ROOT / "data/agent_audio"
OUTPUT_DIR = ROOT / "data/agent_audio_16k"

TARGET_RATE = 16000

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

files = sorted(INPUT_DIR.glob("*.wav"))

for audio_file in files:
    audio, original_rate = sf.read(str(audio_file))

    # Convert to mono if necessary
    if audio.ndim > 1:
        audio = np.mean(audio, axis=1)

    # Resample only if needed
    if original_rate != TARGET_RATE:
        divisor = math.gcd(original_rate, TARGET_RATE)
        up = TARGET_RATE // divisor
        down = original_rate // divisor

        audio = resample_poly(audio, up, down)

    output_file = OUTPUT_DIR / audio_file.name

    sf.write(
        str(output_file),
        audio,
        TARGET_RATE,
        subtype="PCM_16"
    )

    print(f"Resampled: {audio_file.name}")

print(f"\nCompleted: {len(files)} files")
