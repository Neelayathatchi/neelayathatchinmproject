import sounddevice as sd
import numpy as np
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import queue

# Load model
print("Loading model...")
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
model.eval()

# Stream config
SAMPLE_RATE = 16000
BLOCK_DURATION = 5  # seconds
BUFFER = queue.Queue()

# Audio callback to collect data
def callback(indata, frames, time, status):
    if status:
        print(status)
    BUFFER.put(indata.copy())

# Start streaming from mic
with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=callback, blocksize=int(SAMPLE_RATE * BLOCK_DURATION)):
    print("\n🎤 Speak into your microphone...\n(Press Ctrl+C to stop)\n")
    try:
        while True:
            audio_chunk = BUFFER.get()
            audio_input = np.squeeze(audio_chunk)
            input_tensor = processor(audio_input, sampling_rate=SAMPLE_RATE, return_tensors="pt").input_values

            with torch.no_grad():
                logits = model(input_tensor).logits
                predicted_ids = torch.argmax(logits, dim=-1)
                transcription = processor.batch_decode(predicted_ids)[0]
                print("📝", transcription.lower())

    except KeyboardInterrupt:
        print("\n🛑 Stopped.")
