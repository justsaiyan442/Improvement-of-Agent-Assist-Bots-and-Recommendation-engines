import pyaudio
import queue
import threading
import json
from vosk import Model, KaldiRecognizer
from punctuator import RePunctuator
from keyword_extractor import KeywordExtractor

MODEL_PATH = "./vosk-model-small-en-us-0.15"
SAMPLE_RATE = 16000
CHUNK_SIZE = 512

model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, SAMPLE_RATE)
keyword = KeywordExtractor()

audio_queue = queue.Queue()
transcript = []
keywords = []
speech_text = ""

# Shared state for frontend
shared_state = {
    "speech": "",
    "keywords": [],
}

def record_audio():
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=SAMPLE_RATE, input=True, frames_per_buffer=CHUNK_SIZE)
    print("Recording started...")
    try:
        while True:
            data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
            audio_queue.put(data)
    except Exception as e:
        print("Recording stopped.", e)
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()

def transcribe_audio():
    buffer = b""
    global speech_text
    while True:
        data = audio_queue.get()
        buffer += data
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result["text"]
            if text.strip():
                punc = RePunctuator(text)
                punctuated = punc.repunctuate_text()
                final_text = punc.capitalize_text(punctuated)
                transcript.append(final_text)
                keywords = keyword.extract(final_text)
                speech_text = " ".join(transcript)
                shared_state["speech"] = speech_text
                shared_state["keywords"] = keywords

        buffer = b""  # reset

def start_background_threads():
    t1 = threading.Thread(target=record_audio, daemon=True)
    t2 = threading.Thread(target=transcribe_audio, daemon=True)
    t1.start()
    t2.start()
