# tts_engine.py
from transformers import VitsModel, AutoTokenizer
import torch
import scipy.io.wavfile
import os

print("\n[INIT] Loading Meta MMS Odia Voice Model into RAM...")
print("This happens exactly once at server startup...")

# Moving the model loading OUTSIDE the function so it stays cached in memory
MODEL = VitsModel.from_pretrained("facebook/mms-tts-ory")
TOKENIZER = AutoTokenizer.from_pretrained("facebook/mms-tts-ory")
print("[INIT] AI Voice Model successfully loaded and ready!\n")

def generate_odia_audio(text, output_filename="response.wav"):
    """
    Converts Odia text to spoken audio instantly using the pre-loaded global model.
    """
    # Convert text to mathematical tokens
    inputs = TOKENIZER(text, return_tensors="pt")
    
    # Synthesize the waveform without tracking gradients
    with torch.no_grad():
        output = MODEL(**inputs).waveform

    # Save the output as a standard WAV file
    output_path = os.path.join(os.getcwd(), output_filename)
    scipy.io.wavfile.write(output_path, rate=MODEL.config.sampling_rate, data=output[0].numpy())
    
    return output_path

if __name__ == "__main__":
    test_text = "ନା, ଆଜି ଭୁବନେଶ୍ୱରରେ ବର୍ଷା ହେବାର ସମ୍ଭାବନା ନାହିଁ।"
    generate_odia_audio(test_text)