# weather_app/app.py
import gradio as gr
import subprocess
import os

# Import our custom modules
from nlp_brain import parse_odia_query
from weather_fetcher import fetch_weather_data
from tts_engine import generate_odia_audio

def run_kaldi_stt(audio_file_path):
    """
    This is the bridge to your Kaldi workspace. 
    Because multi-pass fMLLR (tri3b) is difficult to run live, 
    we use a mock override for testing the UI flow, 
    but we leave the subprocess structure ready for your Kaldi decode script.
    """
    # ---------------------------------------------------------
    # REAL KALDI EXECUTION (Uncomment when you write a live decode.sh)
    # ---------------------------------------------------------
    # command = f"./decode_live.sh {audio_file_path}"
    # result = subprocess.run(command, shell=True, capture_output=True, text=True)
    # decoded_text = result.stdout.strip()
    # return decoded_text
    
    # ---------------------------------------------------------
    # MOCK KALDI OUTPUT (For UI Testing)
    # ---------------------------------------------------------
    print(f"Received audio from microphone: {audio_file_path}")
    print("Simulating Kaldi Tri3b Decode...")
    return "ଆଜି ଭୁବନେଶ୍ୱରରେ ବର୍ଷା ହେବ କି?" 

def process_voice_query(audio_path):
    """The master 4-Stage Pipeline"""
    if audio_path is None:
        return "Please record an audio query first.", None, None
        
    try:
        # STAGE 1: Kaldi Ear (Mocked for UI test)
        user_text = run_kaldi_stt(audio_path)
        
        # STAGE 2: Python Brain
        city, intent, time_frame = parse_odia_query(user_text)
        
        # STAGE 3: API Fetcher
        weather_text = fetch_weather_data(city, intent, time_frame)
        
        # STAGE 4: Meta MMS Mouth
        output_audio_path = generate_odia_audio(weather_text)
        
        return user_text, weather_text, output_audio_path
        
    except Exception as e:
        return f"System Error: {str(e)}", None, None

# STAGE 5: The Web Interface
with gr.Blocks(theme=gr.themes.Soft()) as ui:
    gr.Markdown("# 🌤️ Odia Voice Weather Assistant")
    gr.Markdown("Ask about the weather in any district of Odisha in your native language!")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 1. Ask Your Question")
            # The Microphone Input
            audio_input = gr.Audio(sources=["microphone"], type="filepath", label="Record Odia Audio")
            submit_btn = gr.Button("Send to Assistant", variant="primary")
            
        with gr.Column():
            gr.Markdown("### 2. Assistant Response")
            # The Outputs
            transcript_output = gr.Textbox(label="Kaldi Heard:", interactive=False)
            text_output = gr.Textbox(label="Weather Data:", interactive=False)
            audio_output = gr.Audio(label="Listen to Assistant", autoplay=True)

    # Wire the button to the master pipeline function
    submit_btn.click(
        fn=process_voice_query,
        inputs=audio_input,
        outputs=[transcript_output, text_output, audio_output]
    )

if __name__ == "__main__":
    print("Starting Web Server...")
    # share=True creates a public link you can share with anyone!
    ui.launch(server_name="0.0.0.0", share=True)