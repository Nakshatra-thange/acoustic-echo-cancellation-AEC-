import pandas as pd

path = "data/human_manifest_reviewed.csv"
df = pd.read_csv(path, dtype={"audio_id": str})

corrections = {
    "1272-128104-0002": {
        "READILYTO": "READILY TO",
    },
    "1272-128104-0004": {
        "HISSITTER": "HIS SITTER",
    },
}

for audio_id, replacements in corrections.items():
    mask = df["audio_id"] == audio_id
    idx = df.index[mask][0]
    transcript = df.at[idx, "transcript"]

    for old, new in replacements.items():
        if old in transcript:
            transcript = transcript.replace(old, new)
            print(f"Fixed: {old} -> {new}")
        else:
            print(f"Not found: {old}")

    df.at[idx, "transcript"] = transcript

df.to_csv(path, index=False)
print("\nReviewed transcript file saved.")
