# Acoustic Echo Cancellation and Voice Activity Detection for Real-Time Barge-In

## 1. Project Overview

This project investigates how effectively Voice Activity Detection (VAD) systems can identify genuine human interruptions during an AI voice agent's playback.

In a conversational voice agent, the agent's own speech can be captured by the microphone and mistakenly detected as human speech. This can cause false interruptions, unreliable speech detection and poor conversational behaviour.

The objective of this research is to evaluate whether applying Acoustic Echo Cancellation (AEC) before VAD can reduce this problem while preserving the ability to detect genuine human speech.

**Central research question:**

Can acoustic echo cancellation improve voice activity detection during human interruptions in an AI agent's playback?

## 2. Experimental Setup

A synthetic dataset of 50 recordings was created using Piper TTS, LibriSpeech human speech and measured SLR28 room impulse responses.

| Scenario | Recordings | Description |
|---|---:|---|
| A | 10 | Agent playback only, without human speech |
| B | 10 | Normal human interruptions |
| C | 30 | Controlled interruptions with different speech-to-echo ratios, echo strengths and onset timings |
| **Total** | **50** | |

All recordings use 16 kHz, mono audio.

The experiments evaluate:

- **VAD:** Silero VAD, WebRTC VAD, TEN VAD and FSMN-VAD.
- **AEC:** WebRTC Acoustic Echo Canceller 3 (AEC3).
- **Reference condition:** Clean-human oracle recordings, used to evaluate VAD without agent echo.

## 3. Experiments Conducted

The research was conducted in four main stages.

### Stage 1 — Original VAD Benchmark

Silero, WebRTC and TEN VAD were evaluated using different thresholds, aggressiveness modes and frame/hop sizes.

The purpose was to establish how the detectors behave when processing microphone audio containing agent playback and human speech.

### Stage 2 — FSMN-VAD Benchmark

FunASR ONNX FSMN-VAD was integrated and evaluated separately.

Unlike the other tested systems, FSMN-VAD produces native speech segments rather than the same frame-level outputs. Its results are therefore reported separately where metric definitions differ.

### Stage 3 — WebRTC AEC3 Evaluation

WebRTC AEC3 was applied to all 50 recordings using the aligned agent playback as the far-end reference.

Echo reduction, human speech preservation and computational performance were measured.

### Stage 4 — Post-AEC VAD Evaluation

The VAD systems were evaluated again using AEC3-processed microphone recordings.

The results were compared across three important conditions:

1. Raw microphone audio.
2. AEC3-processed microphone audio.
3. Clean-human oracle audio.

This allowed the effect of echo cancellation on subsequent VAD performance to be evaluated.

## 4. Key Results

The following headline results are averages across the 13 frame-based VAD configurations.

| Metric | Raw microphone | After AEC3 | Clean-human oracle |
|---|---:|---:|---:|
| Already active at human onset | 98.1% | 21.3% | 18.8% |
| Clean onset detection | 1.9% | 78.5% | 81.2% |
| Detection within 200 ms | 1.5% | 33.1% | 46.7% |

The onset comparison uses 40 B/C recordings per configuration, giving 520 configuration-recording rows.

### Echo-only evaluation

In Scenario A, where there is no human speech:

| Metric | Raw audio | After AEC3 |
|---|---:|---:|
| Echo-only active time | 63.0% | 18.4% |

AEC3 substantially reduced the amount of agent playback incorrectly marked as speech.

However, residual echo continued to trigger VAD activity in 90 of 130 Scenario A configuration-recording rows.

### FSMN-VAD

FSMN-VAD showed the same underlying difficulty:

- All 10 agent-only recordings triggered activity.
- All 40 microphone recordings were already active at human onset before AEC3.
- After AEC3, clean onset detection reached 20%.

FSMN results are reported separately because its native segment-based evaluation differs from the frame-based metrics.

## 5. Main Observations

1. All tested VAD approaches could detect clean human speech reliably.
2. Agent playback alone triggered every tested VAD approach.
3. Raw microphone audio caused extensive false speech activity.
4. VAD was frequently already active before a human interruption began.
5. An existing echo-triggered event overlapping human speech does not necessarily indicate successful barge-in detection.
6. Changing VAD thresholds or aggressiveness alone did not solve the echo problem.
7. FSMN-VAD showed the same fundamental limitation.
8. Applying AEC3 reduced echo-triggered activity substantially.
9. AEC3 improved clean onset detection from 1.9% to 78.5%, approaching the 81.2% clean-human oracle result.
10. Residual echo and detection latency remain important challenges.

## 6. Computational Performance

All tested systems operated faster than real time in the measured benchmark environment.

| Component | Approximate RTF |
|---|---:|
| WebRTC VAD | 0.0001 |
| Silero VAD | 0.0037 |
| FSMN-VAD | 0.0055 |
| TEN VAD | 0.0128 |
| WebRTC AEC3 | 0.0073 |

RTF (Real-Time Factor) is processing time divided by audio duration. A value below 1 indicates processing faster than real time.

These measurements were obtained in the project's Apple Silicon CPU environment and should not be interpreted as universal hardware performance figures.

## 7. Conclusion

The experiments demonstrate that applying acoustic echo cancellation before voice activity detection substantially improves the detection of genuine human interruptions in the tested synthetic conversational audio.

Without AEC, agent playback frequently triggers VAD before the human begins speaking. This makes it difficult for the system to distinguish genuine interruptions from its own playback.

After applying WebRTC AEC3, the clean onset detection rate increased from 1.9% to 78.5%, approaching the clean-human oracle result of 81.2%.

This supports the use of an **AEC → VAD processing pipeline** for voice-agent barge-in detection.

However, AEC3 does not completely eliminate residual echo, and detection within 200 ms remains below the clean-human oracle result. Further improvements are needed for reliable, low-latency real-world deployment.

## 8. Limitations and Future Work

The evaluation has several limitations:

- Audio was synthetically generated using a known linear echo path.
- No physical loudspeaker-and-microphone validation was performed.
- Real-world background noise, clock drift and nonlinear loudspeaker behaviour were not evaluated.
- No perceptual or listening validation was conducted.
- The experiments used a limited number of rooms, one TTS voice and a finite set of human speakers.
- NKF-AEC was not benchmarked because its implementation and checkpoint were unavailable.

Future work should include physical-device testing, more realistic acoustic conditions, perceptual validation, and evaluation of additional AEC approaches such as NKF-AEC.

## 9. Project Structure

```text
barge_in_50/
│
├── FINAL_RESEARCH_REPORT.md
├── FINAL_EXECUTIVE_SUMMARY.md
├── REPRODUCIBILITY.md
├── PROJECT_INDEX.md
├── FINAL_AUDIT.md
│
├── dataset/
│   └── (audio data and manifest)
│
├── models/
│   └── (VAD model files and configurations)
│
├── scripts/
│   └── (experiment scripts)
│
└── results/
    ├── vad_benchmark/
    ├── fsmn_benchmark/
    ├── aec_benchmark/
    ├── post_aec_vad_webrtc/
    └── final_figures/
```

The directory tree above is a conceptual overview; consult `PROJECT_INDEX.md` for the actual file locations.

## 10. Reproducibility

The project includes separate Python environments for the original VAD experiments and FSMN-VAD.

Refer to:

- `REPRODUCIBILITY.md` for environment details and execution instructions.
- `PROJECT_INDEX.md` for the location of datasets, models, scripts and results.
- `FINAL_RESEARCH_REPORT.md` for the complete methodology and detailed analysis.
- `FINAL_AUDIT.md` for integrity and validation checks.

The completed benchmarks and original experiment outputs have been preserved.

---

**Final takeaway:** Voice activity detection alone struggles to distinguish human interruptions from an AI agent's own playback. Applying acoustic echo cancellation before VAD substantially improves barge-in detection, although residual echo and detection latency remain open challenges.
