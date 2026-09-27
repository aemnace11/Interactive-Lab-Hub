import subprocess
from pathlib import Path
from faster_whisper import WhisperModel

VOICES_DIR = Path(__file__).resolve().parent.parent / "voices"

model = WhisperModel("tiny.en", device="cpu", compute_type="int8")

# Ask the question
subprocess.run(
    f'python3 -m piper --model en_US-joe-medium --data-dir "{VOICES_DIR}" --output-raw '
    f'-- "What is your zipcode?" | aplay -q -r 22050 -f S16_LE -t raw -',
    shell=True)

# Record the answer
print("Listening...")
subprocess.run(["arecord", "-q", "-f", "S16_LE", "-r", "16000", "-c", "1",
                "-d", "5", "answer.wav"])

# Transcribe and print
segments, _ = model.transcribe("answer.wav")
print(" ".join(seg.text.strip() for seg in segments))

