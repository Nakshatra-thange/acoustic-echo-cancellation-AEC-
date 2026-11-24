
Part 1 — Get existing audio datasets

Download recordings of human speech and agent-like speech. No recording required.



Part 2 — Generate simulated echo

Use software to mix the two recordings, introduce delays, room effects and different echo strengths.



Part 3 — Build the AEC pipeline

Feed the simulated microphone audio and original agent audio into an echo cancellation system.



Part 4 — Run speech recognition

Transcribe the audio both with AEC enabled and with AEC disabled.



Part 5 — Evaluate the results

Measure agent-word leakage, human WER and performance during double-talk.



Part 6 — Compare different conditions

Test low, medium and high echo, different delays and different room responses.



Part 7 — Create the final research report

Graph results, compare systems, explain failures and document conclusions.



Finish the 20-recording WebRTC experiment

Establish a reliable baseline.



Implement NKF-AEC

Run the same recordings through a neural AEC system.



Compare both systems

Compare WER, echo removal, human speech preservation and processing latency.



Investigate ByteAudio-18

See whether we can reproduce its inference pipeline.



Test realistic acoustic conditions

Add room reverberation, different echo delays, changing echo levels and real recordings.