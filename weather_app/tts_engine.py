from transformers import VitsModel, AutoTokenizer
import torch
import scipy.io.wavfile
import os

def generate_odia_audio(text, output_filename="response.wav"):
    """
    Converts Odia text to spoken audio using Meta's MMS TTS model.
    """
    print("Loading AI Voice Model (this might take a few seconds)...")
    
    # Load the pre-trained Meta model for Odia (ory)
    model = VitsModel.from_pretrained("facebook/mms-tts-ory")
    tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-ory")

    print(f"Generating audio for: {text}")
    
    # Convert text to mathematical tokens
    inputs = tokenizer(text, return_tensors="pt")
    
    # Synthesize the waveform without tracking gradients 
    with torch.no_grad():
        output = model(**inputs).waveform

    # Save the output as a standard WAV file
    output_path = os.path.join(os.getcwd(), output_filename)
    scipy.io.wavfile.write(output_path, rate=model.config.sampling_rate, data=output[0].numpy())
    
    print(f"Success! 🔊 Audio saved to: {output_path}")
    return output_path
