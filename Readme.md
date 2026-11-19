# Acoustic Echo Cancellation (AEC) Research

## 1. About This Research

The goal of this research was to compare different **Acoustic Echo Cancellation (AEC)** systems and understand how well they remove speaker echo while keeping the human speaker's voice clear.

In a voice assistant, the assistant's voice can come out of a speaker and get picked up again by the microphone. This creates echo.

AEC tries to solve two problems:

- Remove the assistant's voice from the microphone recording.
- Keep the actual human speaker's voice clear and understandable.

We focused on comparing existing, runnable AEC models rather than training a new model from scratch.

## 2. Models We Tested

We tested four AEC approaches:

1. **NKF** – Neural Kalman Filter-based AEC.
2. **WebRTC AEC3** – WebRTC's built-in acoustic echo cancellation system.
3. **DTLN-128** – A pretrained DTLN model with a smaller model size.
4. **DTLN-256** – A pretrained DTLN model with a medium model size.
5. **DTLN-512** – A pretrained DTLN model with a larger model size.

The DTLN models were pretrained models. We used them for inference and did not train or fine-tune them.

The DTLN architecture was introduced by Westhausen and Meyer and achieved third place in the ICASSP 2021 Acoustic Echo Cancellation Challenge.

## 3. Dataset and Experiment Setup

We created a benchmark dataset to test the models under controlled conditions.

- 20 test recordings were used.
- Total recording duration was approximately 542 seconds.
- Audio was processed at 16 kHz.
- Each recording contained human speech and simulated speaker echo.
- Human speech came from LibriSpeech.
- The far-end assistant speech came from Piper TTS.
- Room impulse responses were used to simulate how sound travels through a room.
- We tested both double-talk recordings and echo-only recordings.

**Important limitation:** The echo was simulated using room impulse responses. We did not record the audio using a real physical speaker and microphone setup.

## 4. What We Measured

We used multiple measurements because no single metric can tell us whether an AEC model is good.

- **WER (Word Error Rate):** Measures how many words a speech recognition system gets wrong. Lower is better.
- **ERLE (Echo Return Loss Enhancement):** Measures how much echo is reduced when only echo is present. Higher is better.
- **SI-SDR:** Measures how closely the processed audio matches the original clean human speech. Higher is better.
- **Human Speech Preservation:** Measures how much of the human voice is retained after processing. A value closer to 1 is better.
- **Runtime:** Measures how long a model takes to process audio. Lower is faster.

We also checked whether the models completed inference successfully and whether the benchmark results were reproducible.

## 5. Main Findings

### Finding 1: NKF performed best for speech recognition

- NKF achieved the lowest WER among the tested AEC systems.
- Its WER was **0.078**.
- It performed better than WebRTC and all three DTLN models.
- It also preserved the human speaker's volume very well.

**What this means:** If our main goal is to remove echo and give a speech recognition system clearer human speech, NKF was the strongest option in this experiment.

### Finding 2: WebRTC was strongest at pure echo cancellation

- WebRTC achieved the highest average ERLE at **15.75 dB**.
- This means it removed echo most effectively in our echo-only tests.
- It was also the fastest system we tested.
- However, it reduced the human speaker's voice more than the other systems.

**What this means:** WebRTC is a strong choice when echo suppression and processing speed are important, but it may also reduce some of the human speech.

### Finding 3: DTLN preserved human speech well

- DTLN models retained a large amount of the human speaker's voice.
- DTLN-512 achieved the highest SI-SDR at **8.42 dB**.
- DTLN-512 also achieved the highest human speech correlation at **0.853**.
- DTLN models generally preserved the human voice better than WebRTC.

**What this means:** DTLN produced a good balance in terms of preserving the quality of human speech, especially with the larger model.

However, better audio similarity did not automatically mean better speech recognition results.

### Finding 4: Larger DTLN models were not always better

We compared DTLN-128, DTLN-256 and DTLN-512.

- DTLN-128 was the fastest DTLN model.
- DTLN-512 achieved the best SI-SDR and human speech correlation.
- DTLN-512 was significantly slower than the smaller DTLN models.
- Increasing the model size did not produce a clear improvement in WER.

**What this means:** A larger model does not automatically provide better results for every task. The best model depends on what we want to optimise.

### Finding 5: DTLN struggled when echo was much louder than human speech

One recording, `pair_009`, was particularly difficult.

- The echo was much louder than the human speaker.
- The Signal-to-Echo Ratio (SER) was approximately **-29.5 dB**.
- All three DTLN models struggled badly with this recording.
- Their speech recognition results were very poor.

**What this means:** DTLN had difficulty when the human voice was almost completely buried under the echo. This is an important weakness that needs further investigation.

### Finding 6: There is no single winner across every metric

Each system had different strengths:

- NKF performed best for downstream speech recognition.
- WebRTC performed best for echo-only suppression and processing speed.
- DTLN performed well at preserving human speech quality, especially DTLN-512.

The results show that choosing an AEC system depends on the application's main requirement.

## 6. Performance Comparison

| Measurement | Best System | Result |
|---|---|---:|
| Lowest WER | NKF | 0.078 |
| Highest ERLE | WebRTC | 15.75 dB |
| Best SI-SDR | DTLN-512 | 8.42 dB |
| Best Human Speech Correlation | DTLN-512 | 0.853 |
| Best Human Speech Level Preservation | NKF | 0.969 |
| Fastest Runtime | WebRTC | 0.0062 RTF |

*These are results from our particular benchmark, not universal rankings of the models.*

## 7. Runtime Comparison

We also compared how quickly the models processed audio.

| System | Real-Time Factor (RTF) | Approx. Processing Speed |
|---|---:|---:|
| WebRTC | 0.0062 | 160x real time |
| NKF | 0.0073 | 137x real time |
| DTLN-128 | 0.0220 | 45x real time |
| DTLN-256 | 0.0438 | 23x real time |
| DTLN-512 | 0.1171 | 9x real time |

All tested systems processed audio faster than real time on our test machine.

However, these runtime results also depend on the different software implementations and should not be treated as a perfectly controlled comparison of algorithm efficiency.

## 8. Final Conclusion

Based on our experiments:

1. **NKF was the best overall choice for our speech-recognition-focused benchmark.** It achieved the lowest WER and preserved human speech volume well.
2. **WebRTC was the strongest for echo-only cancellation.** It also had the fastest runtime, but reduced more human speech.
3. **DTLN showed good human speech preservation and waveform quality.** DTLN-512 achieved the best SI-SDR, but it was slower and did not achieve the best WER.
4. **DTLN struggled in extremely difficult low-SER conditions**, where echo was much louder than the human speaker.
5. **No model performed best on every measurement.** The choice depends on whether the priority is speech recognition, echo suppression, speech quality or processing speed.

For our current benchmark, we would choose NKF if the main objective is to provide clearer human speech to a downstream speech recognition system.

## 9. Limitations of This Research

Our findings should be understood within the limits of the experiment.

- We tested only 20 recordings.
- Echo was simulated using room impulse responses.
- We did not test a physical speaker and microphone setup.
- We did not include all real-world effects, such as nonlinear speaker distortion, background noise variations and clock drift.
- We used English speech data.
- We evaluated speech recognition using one downstream ASR system.
- We did not train or fine-tune the DTLN models.

Therefore, these results do not prove that the same ranking will hold in every real-world environment.

## 10. Research Status

The planned benchmark comparison has been completed.

We have:

- Set up multiple runnable AEC systems.
- Prepared a common test dataset.
- Processed all test recordings through the selected systems.
- Evaluated echo cancellation and human speech preservation.
- Compared downstream speech recognition performance.
- Measured processing speed.
- Checked reproducibility and benchmark outputs.
- Identified the strengths and weaknesses of each approach.

The next step, if we want to extend this research, would be to test the systems using real speaker-microphone recordings and more challenging real-world acoustic conditions.

---

**Overall takeaway:** NKF gave us the best speech-recognition results, WebRTC gave us the strongest pure echo suppression, and DTLN showed promising human speech preservation. Our research demonstrates that AEC performance is a trade-off: removing echo is important, but keeping the human speaker's voice clear is equally important.