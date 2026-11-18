
from pathlib import Path
import numpy as np
import soundfile as sf

ROOT = Path.home() / "projects" / "aec-research"
BASE = ROOT / "data/experiments"

files = {
    "Clean human": BASE / "clean_human/pair_001.wav",
    "Agent reference": BASE / "references/pair_001.wav",
    "Far-end only": BASE / "far_end_only/pair_001.wav",
    "Double-talk": BASE / "double_talk/pair_001.wav",
}

for name, path in files.items():
    audio, sr = sf.read(str(path))

    print(f"\n{name}")
    print("  Sample rate:", sr)
    print("  Duration:", round(len(audio) / sr, 2), "seconds")
    print("  Peak amplitude:", round(float(np.max(np.abs(audio))), 4))
    print("  RMS:", round(float(np.sqrt(np.mean(audio**2))), 4))
