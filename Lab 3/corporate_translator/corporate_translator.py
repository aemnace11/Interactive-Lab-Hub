
import argparse
import difflib
import json
import re
import sys
import threading
import time
import urllib.request
from pathlib import Path
 
import numpy as np
import sounddevice as sd
from PIL import Image, ImageDraw, ImageFont
 
# =============================== Configuration ===============================
 
APP_DIR = Path(__file__).resolve().parent          # Lab 3/corporate_translator
LAB_DIR = APP_DIR.parent                           # Lab 3
VAD_MODEL = LAB_DIR / "models" / "silero_vad.onnx"
VOICE_NAME = "en_US-joe-medium"
VOICE_FOLDERS = [LAB_DIR / "voices", LAB_DIR / "speech-scripts"]   # folders searched for Piper .onnx voices
 
PERSONAS = ["Corporate", "Yoda"]
 
PROMPT_SENTENCE = "Please say what you would like to be translated."
PROMPT_FOLLOWUP = "Want to hear that again, try another, or are you done?"
SORRY = "Sorry I didn't understand that, please say it again."
TRANSLATE_ERROR = "Sorry, I couldn't translate that. Let's try another."
GOODBYE = "Goodbye!"            # empty string = silent exit
 
# Turn-taking
SAMPLE_RATE = 16000
SILENCE_SECONDS = 1.2           # silence that ends a turn; overridden by --min-silence
MIN_SPEECH_SECONDS = 0.25       # minimum speech duration
NO_SPEECH_TIMEOUT = 10.0        # seconds without speech before listen() returns ""
WHISPER_MODEL = "tiny.en"       # overridden by --model
# Whisper initial_prompt for follow-up commands; None disables
COMMAND_HINT = "Hear it again. Try another. I'm done."
 
# Ollama
OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "qwen2.5:1.5b"
OLLAMA_TIMEOUT = 60
 
# Qwiic Button I2C address and registers
BUTTON_ADDRESS = 0x6F
STATUS_REG = 0x03               # bit 1 = clicked flag, latched until cleared
BEEN_CLICKED = 0x02
LED_REG = 0x19                  # LED brightness, 0-255
LED_BRIGHTNESS = 255
 
SHOW_STATUS = True              # status line below persona name
SCREEN_HINT = "press button to switch"    # hint line at top of screen; empty string disables
 
 
# ================================== Screen ===================================
 
class Screen:
    """Mini PiTFT display: centered persona name, hint line, status line."""
 
    FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
 
    def __init__(self):
        self.width, self.height = 240, 135      # landscape
        self.rotation = 90
        self.persona = PERSONAS[0]
        self.status = ""
        self.image = None
        self.disp = None
        self.backlight = None
        self._lock = threading.Lock()
        self._fonts = {}
        try:
            # ST7789 init, Lab 2 screen_clock.py pinout
            import board
            import digitalio
            import adafruit_rgb_display.st7789 as st7789
 
            self.disp = st7789.ST7789(
                board.SPI(),
                cs=digitalio.DigitalInOut(board.D5),
                dc=digitalio.DigitalInOut(board.D25),
                rst=None,
                baudrate=64000000,
                width=135,
                height=240,
                x_offset=53,
                y_offset=40,
            )
            self.backlight = digitalio.DigitalInOut(board.D22)
            self.backlight.switch_to_output()
            self.backlight.value = True
        except Exception as e:
            print(f"[screen] not available ({e}). Did you run: sudo systemctl stop piscreen.service ?")
 
    def _font(self, size, bold=True):
        key = (size, bold)
        if key not in self._fonts:
            try:
                self._fonts[key] = ImageFont.truetype(self.FONT_BOLD if bold else self.FONT_REGULAR, size)
            except OSError:
                self._fonts[key] = ImageFont.load_default()
        return self._fonts[key]
 
    @staticmethod
    def _draw_centered(draw, text, font, cx, cy, fill):
        left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
        draw.text((int(cx - (right - left) / 2 - left), int(cy - (bottom - top) / 2 - top)),
                  text, font=font, fill=fill)
 
    def _render(self):
        img = Image.new("RGB", (self.width, self.height), "white")
        draw = ImageDraw.Draw(img)
        cy = self.height // 2
 
        for size in range(36, 11, -2):          # largest font size that fits screen width
            font = self._font(size)
            left, _, right, _ = draw.textbbox((0, 0), self.persona, font=font)
            if right - left <= self.width - 20:
                break
        self._draw_centered(draw, self.persona, font, self.width / 2, cy, "black")
 
        if SCREEN_HINT:
            self._draw_centered(draw, SCREEN_HINT, self._font(13, bold=False),
                                self.width / 2, 16, (110, 110, 110))
 
        if SHOW_STATUS and self.status:
            self._draw_centered(draw, self.status, self._font(14, bold=False),
                                self.width / 2, self.height - 16, (110, 110, 110))
 
        self.image = img
        if self.disp is not None:
            self.disp.image(img, self.rotation)
 
    def show(self, persona=None, status=None):
        with self._lock:
            if persona is not None:
                self.persona = persona
            if status is not None:
                self.status = status
            try:
                self._render()
            except Exception as e:
                print(f"[screen] draw failed: {e}")
 
    def off(self):
        with self._lock:
            try:
                if self.disp is not None:
                    self.disp.image(Image.new("RGB", (self.width, self.height), "black"), self.rotation)
                if self.backlight is not None:
                    self.backlight.value = False
            except Exception:
                pass
 
 
# ================================ Qwiic Button ================================
 
class Button:
    """Qwiic Button over I2C: click detection and LED control. Bus access is serialized by a lock."""
 
    def __init__(self):
        self.lock = threading.Lock()
        self.device = None
        try:
            import board
            import busio
            from adafruit_bus_device.i2c_device import I2CDevice
            self.device = I2CDevice(busio.I2C(board.SCL, board.SDA), BUTTON_ADDRESS)
            # LED: pulsing disabled, brightness 0
            self._write(0x1A, 1)
            self._write(0x1B, 0, 2)
            self._write(LED_REG, 0)
            self._write(STATUS_REG, 0)          # clear latched click
            print("[button] found")
        except Exception as e:
            self.device = None
            print(f"[button] not found at {hex(BUTTON_ADDRESS)} ({e}); LED and persona switching disabled")
 
    def _write(self, register, value, n_bytes=1):
        with self.device:
            self.device.write(bytearray([register]) + value.to_bytes(n_bytes, "little"))
 
    def _read(self, register):
        buf = bytearray(1)
        with self.device:
            self.device.write_then_readinto(bytes([register]), buf)
        return buf[0]
 
    def led(self, on):
        if self.device is None:
            return
        with self.lock:
            try:
                self._write(LED_REG, LED_BRIGHTNESS if on else 0)
            except OSError as e:
                print(f"[button] LED error: {e}")
 
    def was_clicked(self):
        """Returns True if the latched click flag is set, then clears it."""
        if self.device is None:
            return False
        with self.lock:
            try:
                if self._read(STATUS_REG) & BEEN_CLICKED:
                    self._write(STATUS_REG, 0)
                    return True
            except OSError:
                pass
        return False
 
 
class PersonaSelector:
    """Thread-safe persona index; updates the screen on change."""
 
    def __init__(self, screen):
        self._index = 0
        self._lock = threading.Lock()
        self._screen = screen
 
    @property
    def current(self):
        with self._lock:
            return PERSONAS[self._index]
 
    def advance(self):
        with self._lock:
            self._index = (self._index + 1) % len(PERSONAS)
            name = PERSONAS[self._index]
        print(f"[persona] {name}")
        self._screen.show(persona=name)
 
 
def watch_button(button, selector, stop_event):
    """Background thread: polls the button, advances persona on click."""
    while not stop_event.is_set():
        if button.was_clicked():
            selector.advance()
        time.sleep(0.05)
 
 
# =============================== Text-to-speech ==============================
 
def find_voice(name):
    for folder in VOICE_FOLDERS:
        path = folder / f"{name}.onnx"
        if path.is_file():
            return path
    return None
 
 
class Speaker:
    """Piper TTS with sounddevice playback. Synthesized audio is cached per text."""
 
    def __init__(self, voice_path):
        from piper import PiperVoice
        self.voice = PiperVoice.load(str(voice_path))
        self._cache = {}
 
    def prepare(self, text):
        """Synthesizes and caches text without playback."""
        if text and text not in self._cache:
            chunks, rate = [], 22050
            for chunk in self.voice.synthesize(text):
                chunks.append(np.frombuffer(chunk.audio_int16_bytes, dtype=np.int16))
                rate = chunk.sample_rate
            if chunks:
                self._cache[text] = (np.concatenate(chunks), rate)
 
    def say(self, text):
        print(f"[say] {text}")
        if text in self._cache:
            audio, rate = self._cache[text]
            sd.play(audio, samplerate=rate)
            sd.wait()
            return
        chunks, rate = [], 22050
        for chunk in self.voice.synthesize(text):   # play each chunk as it is synthesized
            audio = np.frombuffer(chunk.audio_int16_bytes, dtype=np.int16)
            rate = chunk.sample_rate
            chunks.append(audio)
            sd.play(audio, samplerate=rate)
            sd.wait()
        if chunks:
            self._cache[text] = (np.concatenate(chunks), rate)
 
 
# =============================== Speech-to-text ==============================
 
class Listener:
    """Microphone capture, VAD endpointing, Whisper transcription."""
 
    def __init__(self, button, screen, whisper_model, min_silence):
        import sherpa_onnx
        from faster_whisper import WhisperModel
        self._sherpa = sherpa_onnx
        self.button = button
        self.screen = screen
        self.min_silence = min_silence
        print(f"[stt] loading Whisper {whisper_model}...")
        self.recognizer = WhisperModel(whisper_model, device="cpu", compute_type="int8")
 
    def _new_vad(self):
        config = self._sherpa.VadModelConfig()
        config.silero_vad.model = str(VAD_MODEL)
        config.silero_vad.min_silence_duration = self.min_silence
        config.silero_vad.min_speech_duration = MIN_SPEECH_SECONDS
        config.sample_rate = SAMPLE_RATE
        vad = self._sherpa.VoiceActivityDetector(config, buffer_size_in_seconds=30)
        return vad, config.silero_vad.window_size
 
    def _transcribe(self, utterance, hint):
        segments, _ = self.recognizer.transcribe(utterance, beam_size=1, language="en",
                                                 initial_prompt=hint)
        text = " ".join(s.text.strip() for s in segments)
        return re.sub(r"\[.*?\]|\(.*?\)", "", text).strip()   # strip bracketed tags, e.g. [BLANK_AUDIO]
 
    def listen(self, hint=None):
        """Captures one utterance with the LED on; returns its transcript, or "" on timeout."""
        vad, window = self._new_vad()      # new VAD per call
        buffer = np.empty(0, dtype=np.float32)
        samples_per_read = int(0.1 * SAMPLE_RATE)
        deadline = time.monotonic() + NO_SPEECH_TIMEOUT
 
        self.button.led(True)
        self.screen.show(status="Listening...")
        print("[mic] listening...")
        try:
            with sd.InputStream(channels=1, dtype="float32", samplerate=SAMPLE_RATE) as stream:
                while True:
                    chunk, _ = stream.read(samples_per_read)
                    buffer = np.concatenate([buffer, chunk.reshape(-1)])
                    while len(buffer) > window:
                        vad.accept_waveform(buffer[:window])
                        buffer = buffer[window:]
 
                    if vad.is_speech_detected():
                        deadline = time.monotonic() + NO_SPEECH_TIMEOUT   # extend timeout while speech is active
 
                    if not vad.empty():
                        utterance = np.array(vad.front.samples, dtype=np.float32)
                        vad.pop()
                        self.button.led(False)                 # end of utterance
                        self.screen.show(status="Transcribing...")
                        heard = self._transcribe(utterance, hint)
                        print(f"[heard] {heard!r}")
                        if heard:
                            return heard
                        # empty transcript: resume listening
                        self.button.led(True)
                        self.screen.show(status="Listening...")
                        deadline = time.monotonic() + NO_SPEECH_TIMEOUT
 
                    elif time.monotonic() > deadline:
                        print("[heard] (nothing)")
                        return ""
        finally:
            self.button.led(False)
            self.screen.show(status="")
 
 
# ================================ Translation ================================
 
PERSONA_PROMPTS = {
    "Corporate": {
        "system": (
            "Rewrite the user's sentence the way an overly polished corporate employee would say it: "
            "sugar-coated, diplomatic, never blunt, full of business jargon like circle back, bandwidth, "
            "alignment, leverage, synergy, action items, take it offline. Keep the original meaning. "
            "If it is a question, rewrite the question; do not answer it. "
            "Reply with only the rewritten sentence, at most two sentences, no quotes or explanation."
        ),
        "examples": [
            ("I don't want to go to this meeting.",
             "I'm not sure I'm the right stakeholder for this sync, but I'd love to review the key takeaways async."),
            ("Your idea is bad.",
             "Love the energy here! Let's take this offline and stress-test a few alternative approaches."),
        ],
    },
    "Yoda": {
        "system": (
            "You are Yoda from Star Wars. Rewrite the user's sentence the way Yoda would say it, "
            "using his inverted word order (object or description first, then subject, then verb), "
            "sometimes adding 'Hmm.' or 'Yes.'. Keep the original meaning. "
            "If it is a question, rewrite the question; do not answer it. "
            "Reply with only the rewritten sentence, at most two sentences, no quotes or explanation."
        ),
        "examples": [
            ("I am going to the store.", "To the store, going I am. Hmm."),
            ("I don't understand this homework.", "Understand this homework, I do not. Confusing, it is."),
        ],
    },
}
 
 
def clean_llm_output(text):
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    text = lines[0] if lines else ""
    text = re.sub(r"^(translation|rewritten|corporate|yoda|answer|output)\s*:\s*", "", text, flags=re.I)
    return text.strip(" \"\u201c\u201d")[:300]
 
 
class Translator:
    """Ollama chat client. Translations are cached per (sentence, persona)."""
 
    def __init__(self):
        self._cache = {}
        self._check_ollama()
        print(f"[translate] loading {OLLAMA_MODEL}...")
        self._ask_llm("Corporate", "Hello.")    # warm-up request loads the model
 
    @staticmethod
    def _check_ollama():
        try:
            with urllib.request.urlopen(f"{OLLAMA_URL}/api/tags", timeout=3) as resp:
                names = [m.get("name", "") for m in json.load(resp).get("models", [])]
        except Exception:
            sys.exit("Ollama isn't running. Start it with:  sudo systemctl start ollama")
        if OLLAMA_MODEL not in names and f"{OLLAMA_MODEL}:latest" not in names:
            sys.exit(f"Ollama model '{OLLAMA_MODEL}' isn't downloaded. Get it with:  ollama pull {OLLAMA_MODEL}")
 
    def _ask_llm(self, persona, sentence):
        spec = PERSONA_PROMPTS[persona]
        messages = [{"role": "system", "content": spec["system"]}]
        for user_text, reply in spec["examples"]:
            messages += [{"role": "user", "content": user_text},
                         {"role": "assistant", "content": reply}]
        messages.append({"role": "user", "content": sentence})
        body = json.dumps({
            "model": OLLAMA_MODEL,
            "messages": messages,
            "stream": False,
            "keep_alive": "30m",
            "options": {"temperature": 0.7, "num_predict": 80},
        }).encode()
        request = urllib.request.Request(f"{OLLAMA_URL}/api/chat", data=body,
                                         headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(request, timeout=OLLAMA_TIMEOUT) as resp:
            return json.load(resp)["message"]["content"]
 
    def translate(self, sentence, persona):
        """Returns the translation, or "" on failure."""
        key = (sentence, persona)
        if key in self._cache:
            return self._cache[key]
        try:
            result = clean_llm_output(self._ask_llm(persona, sentence))
        except Exception as e:
            print(f"[translate] Ollama request failed: {e}")
            return ""
        if result:
            self._cache[key] = result
        return result
 
 
# ============================== Command matching =============================
 
AGAIN, ANOTHER, DONE = "again", "another", "done"
INTENT_PHRASES = {          # exact-match priority order
    AGAIN: ["hear it again", "again", "repeat", "replay", "one more time", "say that again", "pardon"],
    ANOTHER: ["try another", "another", "new one", "next", "different", "something else",
              "not done", "not finished"],
    DONE: ["done", "finished", "that's all", "that's it", "stop", "quit", "exit", "goodbye",
           "bye", "no thanks", "i'm good"],
}
 
 
def parse_intent(text):
    """Maps a transcript to AGAIN, ANOTHER, DONE, or None."""
    t = re.sub(r"[^a-z' ]+", " ", text.lower().replace("\u2019", "'"))
    t = " ".join(t.split())
    if not t:
        return None
 
    for intent, phrases in INTENT_PHRASES.items():
        for phrase in phrases:
            if re.search(rf"\b{re.escape(phrase)}\b", t):
                return intent
 
    # fuzzy match for misrecognized commands
    words = t.split()
    best_intent, best_score = None, 0.0
    for intent, phrases in INTENT_PHRASES.items():
        for phrase in phrases:
            scores = [difflib.SequenceMatcher(None, t, phrase).ratio()]
            if " " not in phrase and len(phrase) >= 4:
                scores += [difflib.SequenceMatcher(None, w, phrase).ratio() for w in words if len(w) >= 3]
            if max(scores) > best_score:
                best_intent, best_score = intent, max(scores)
    return best_intent if best_score >= 0.75 else None
 
 
# ================================== Main flow ================================
 
def run(screen, selector, speaker, listener, translator):
    while True:
        # Steps 3-5: prompt and capture sentence
        speaker.say(PROMPT_SENTENCE)
        sentence = listener.listen()
        while not sentence:
            speaker.say(SORRY)
            sentence = listener.listen()
 
        while True:
            # Step 6: translate with current persona
            persona = selector.current
            screen.show(status="Translating...")
            translation = translator.translate(sentence, persona)
            screen.show(status="")
            if not translation:                 # translation failure: return to step 3
                speaker.say(TRANSLATE_ERROR)
                break
            print(f"[{persona}] {translation}")
            speaker.say(translation)
 
            # Steps 7-8: follow-up prompt and command capture
            speaker.say(PROMPT_FOLLOWUP)
            intent = parse_intent(listener.listen(hint=COMMAND_HINT))
            while intent is None:                       # Step 9: unrecognized command
                speaker.say(SORRY)
                intent = parse_intent(listener.listen(hint=COMMAND_HINT))
            print(f"[intent] {intent}")
 
            if intent == AGAIN:
                continue            # back to step 6
            if intent == ANOTHER:
                break               # back to step 3
            if GOODBYE:
                speaker.say(GOODBYE)
            return                  # end session
 
 
def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--model", default=WHISPER_MODEL, help=f"whisper model size (default: {WHISPER_MODEL})")
    parser.add_argument("--voice", default=VOICE_NAME, help=f"Piper voice name (default: {VOICE_NAME})")
    parser.add_argument("--min-silence", type=float, default=SILENCE_SECONDS,
                        help=f"seconds of silence that end your turn (default: {SILENCE_SECONDS})")
    args = parser.parse_args()
 
    voice_path = find_voice(args.voice)
    if voice_path is None:
        sys.exit(f"Piper voice '{args.voice}' not found in {[str(f) for f in VOICE_FOLDERS]}.\n"
                 f"Download it with:  python3 -m piper.download_voices {args.voice} --data-dir \"{LAB_DIR / 'voices'}\"")
    if not VAD_MODEL.is_file():
        sys.exit(f"VAD model not found at {VAD_MODEL}. Run Lab 3's speech-scripts/setup.sh first.")
 
    screen = Screen()
    screen.show(status="Starting up...")                # Step 2: initial display
    button = Button()
    selector = PersonaSelector(screen)
    stop_event = threading.Event()
    threading.Thread(target=watch_button, args=(button, selector, stop_event), daemon=True).start()
 
    try:
        screen.show(status="Loading translator...")
        translator = Translator()                       # exits if Ollama is unavailable
        screen.show(status="Loading speech...")
        speaker = Speaker(voice_path)
        listener = Listener(button, screen, args.model, args.min_silence)
        for line in (PROMPT_SENTENCE, PROMPT_FOLLOWUP, SORRY, TRANSLATE_ERROR, GOODBYE):
            speaker.prepare(line)
        screen.show(status="")
        print("Ready.\n")
        run(screen, selector, speaker, listener, translator)
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        stop_event.set()
        button.led(False)
        screen.off()
 
 
if __name__ == "__main__":
    main()
 
