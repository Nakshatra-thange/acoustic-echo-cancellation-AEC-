import pandas as pd

PATH = "data/human_manifest_reviewed.csv"

df = pd.read_csv(PATH, dtype={"audio_id": str})

corrections = {
    "1272-128104-0002": {
        "SIMILESDRAWN": "SIMILES DRAWN",
    },
    "1272-128104-0004": {
        "NATIONALAS": "NATIONAL AS",
        "USEDTO": "USED TO",
        "LIKEA": "LIKE A",
    },
    "1272-128104-0011": {
        "OFMAN": "OF MAN",
        "FELICITOUSGRACE": "FELICITOUS GRACE",
    },
    "1272-135031-0001": {
        "WHOHAD": "WHO HAD",
    },
}

total = 0

for audio_id, replacements in corrections.items():
    mask = df["audio_id"].str.strip() == audio_id

    if not mask.any():
        print(f"RECORDING NOT FOUND: {audio_id}")
        continue

    index = df.index[mask][0]
    transcript = str(df.at[index, "transcript"])

    for old, new in replacements.items():
        if old in transcript:
            transcript = transcript.replace(old, new)
            total += 1
            print(f"FIXED: {audio_id}: {old} -> {new}")
        else:
            print(f"ALREADY FIXED OR NOT FOUND: {audio_id}: {old}")

    df.at[index, "transcript"] = transcript

df.to_csv(PATH, index=False)

print(f"\nTotal corrections made: {total}")
print(f"Updated file: {PATH}")
