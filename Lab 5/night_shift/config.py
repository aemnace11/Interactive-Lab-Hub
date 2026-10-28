from pathlib import Path

# folders
HERE = Path(__file__).resolve().parent
LAB_DIR = HERE.parent
DATA_DIR = HERE / "data"

# camera and model
MODEL_PATH = LAB_DIR / "yolo26n_ncnn_model"
CAMERA_INDEX = 0
WARMUP_FRAMES = 10

# sampling
SAMPLE_SECONDS = 10
CONFIRM_SAMPLES = 2

# detection
CAT_CLASSES = ("cat", "dog")
CAT_CONF = 0.4
BOWL_CONF = 0.25
ZONE_PAD = 0.5

# verdict
GUILTY_SECONDS = 30

# files
ZONE_FILE = DATA_DIR / "zone.json"
LOG_FILE = DATA_DIR / "night_log.jsonl"
BEFORE_PHOTO = DATA_DIR / "before.jpg"
AFTER_PHOTO = DATA_DIR / "after.jpg"
REPORT_FILE = DATA_DIR / "report.txt"
SCREEN_FILE = DATA_DIR / "morning_screen.png"

# qwen
OLLAMA_URL = "http://localhost:11434/api/generate"
QWEN_MODEL = "qwen3.5:0.8b"
QWEN_MAX_TOKENS = 80
QWEN_TIMEOUT = 120

# piper
PIPER_VOICE = "en_US-joe-medium"
PIPER_DATA_DIR = Path.home() / "Interactive-Lab-Hub" / "Lab 3" / "speech-scripts"

AUDIO_DEVICE = "plughw:CARD=UACDemoV10,DEV=0"
