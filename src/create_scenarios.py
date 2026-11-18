
from pathlib import Path
import numpy as np
import pandas as pd
import soundfile as sf

ROOT = Path.home() / "projects" / "aec-research"
SR = 16000

human_df = pd.read_csv(ROOT / "data/human_manifest.csv")
agent_df = pd.read_csv(ROOT / "data/agent_manifest.csv")

BASE = ROOT / "data/experiments"

for folder in [
    "far_end_only",
    "double_talk",
    "references",
    "clean_human",
]:
    (BASE / folder).mkdir(parents=True, exist_ok=True)


def load_audio(path):
    audio, sr = sf.read(str(path))

    if sr != SR:
        raise ValueError(f"Expected {SR} Hz, got {sr}")

    if audio.ndim > 1:
        audio = audio.mean(axis=1)

    return audio.astype(np.float32)


def save_audio(path, audio):
    # Prevent clipping without changing relative levels
    peak = np.max(np.abs(audio)) if len(audio) else 0

    if peak > 0.99:
        audio = audio * (0.99 / peak)

    sf.write(str(path), audio, SR, subtype="PCM_16")


def place_audio(signal, background_length, start_sample):
    output = np.zeros(background_length, dtype=np.float32)

    end_sample = min(
        start_sample + len(signal),
        background_length
    )

    if end_sample > start_sample:
        output[start_sample:end_sample] = (
            signal[:end_sample - start_sample]
        )

    return output


records = []

for i in range(20):
    hrow = human_df.iloc[i]
    arow = agent_df.iloc[i]

    human = load_audio(hrow["audio_path"])

    agent_path = (
        ROOT / "data/agent_audio_16k" /
        f"{arow['audio_id']}.wav"
    )
    agent = load_audio(agent_path)

    # Agent starts at 25% of the human recording.
    # This produces overlap for most selected recordings.
    start = int(len(human) * 0.25)

    # Keep the agent utterance inside the recording.
    start = min(start, max(0, len(human) - len(agent)))

    agent_reference = place_audio(
        agent, len(human), start
    )

    # Simplified echo path: delayed agent playback.
    delay = int(0.040 * SR)  # 40 ms
    delayed_agent = np.zeros_like(human)

    if delay < len(human):
        delayed_agent[delay:] = agent_reference[:-delay]

    echo = 0.3 * delayed_agent

    # Far-end-only microphone: no human speech.
    far_end = echo.copy()

    # Double-talk microphone: human + agent echo.
    double_talk = human + echo

    recording_id = f"pair_{i+1:03d}"

    save_audio(
        BASE / "far_end_only" / f"{recording_id}.wav",
        far_end
    )

    save_audio(
        BASE / "double_talk" / f"{recording_id}.wav",
        double_talk
    )

    save_audio(
        BASE / "references" / f"{recording_id}.wav",
        agent_reference
    )

    save_audio(
        BASE / "clean_human" / f"{recording_id}.wav",
        human
    )

    records.append({
        "recording_id": recording_id,
        "human_transcript": hrow["transcript"],
        "agent_transcript": arow["transcript"],
        "duration_seconds": len(human) / SR,
        "agent_start_seconds": start / SR,
        "echo_delay_seconds": 0.040,
        "echo_gain": 0.3,
    })


pd.DataFrame(records).to_csv(
    BASE / "scenario_manifest.csv",
    index=False
)

print("Scenario generation complete.")
print("Pairs created:", len(records))
print("Far-end only:", len(list((BASE / "far_end_only").glob("*.wav"))))
print("Double-talk:", len(list((BASE / "double_talk").glob("*.wav"))))
print("Agent references:", len(list((BASE / "references").glob("*.wav"))))
print("Clean human:", len(list((BASE / "clean_human").glob("*.wav"))))
