
from pathlib import Path
import soundfile as sf

ROOT = Path.home() / "projects" / "aec-research"

human_df_path = ROOT / "data/human_manifest.csv"
agent_df_path = ROOT / "data/agent_manifest.csv"

import pandas as pd

human_df = pd.read_csv(human_df_path)
agent_df = pd.read_csv(agent_df_path)

# Inspect recording number 1
human_path = human_df.iloc[0]["audio_path"]
agent_id = agent_df.iloc[0]["audio_id"]

agent_path = ROOT / "data/agent_audio_16k" / f"{agent_id}.wav"
mixed_path = ROOT / "data/simulated_mic/mic_001.wav"

for name, path in [
    ("Human original", human_path),
    ("Agent original", agent_path),
    ("Mixed microphone", mixed_path),
]:
    audio, sr = sf.read(str(path))
    print(f"{name}: {len(audio)/sr:.2f}s, {sr} Hz, {path}")
