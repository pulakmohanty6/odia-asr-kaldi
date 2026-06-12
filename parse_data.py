import os
import pandas as pd
import subprocess
import re

# Paths
# UPDATE THIS PATH TO MATCH YOUR EXACT FOLDER NAME!
DATASET_PATH = "/home/kiit/asr_workspace/cv-corpus-25.0-2026-03-09/or" 
PROJECT_PATH = "/home/kiit/asr_workspace/odia-asr-kaldi"

def clean_odia_text(text):
    text = str(text)
    # The Nuclear Option: KEEP ONLY Odia Unicode characters and standard spaces
    text = ''.join(c for c in text if '\u0B00' <= c <= '\u0B7F' or c == ' ')
    # Collapse multiple spaces into one and trim edges
    text = ' '.join(text.split())
    return text

def process_split(split_name):
    print(f"Processing {split_name} split...")
    tsv_file = os.path.join(DATASET_PATH, f"{split_name}.tsv")
    df = pd.read_csv(tsv_file, sep='\t')
    
    # SHUFFLE the data to grab 5000 random sentences (multiple speakers!)
    df_subset = df.sample(n=5000, random_state=42) if len(df) >= 5000 else df
    
    # FIX: Automatically create the required data and wav directories if they are missing
    os.makedirs(f"{PROJECT_PATH}/data/{split_name}", exist_ok=True)
    os.makedirs(f"{PROJECT_PATH}/wav/{split_name}", exist_ok=True)
    
    with open(f"{PROJECT_PATH}/data/{split_name}/text", "w", encoding="utf-8") as f_text, \
         open(f"{PROJECT_PATH}/data/{split_name}/wav.scp", "w") as f_wav, \
         open(f"{PROJECT_PATH}/data/{split_name}/utt2spk", "w") as f_utt2spk:
        
        for idx, row in df_subset.iterrows():
            client_id = str(row['client_id'])[:8] 
            clip_name = str(row['path'])
            sentence = clean_odia_text(row['sentence'])
            
            # Skip if the cleaning removed everything
            if not sentence:
                continue
                
            utt_id = f"{client_id}-{clip_name.replace('.mp3', '')}"
            
            # Write tracking files
            f_text.write(f"{utt_id} {sentence}\n")
            f_utt2spk.write(f"{utt_id} {client_id}\n")
            
            # Audio Conversion
            src_mp3 = os.path.join(DATASET_PATH, "clips", clip_name)
            dest_wav = os.path.join(PROJECT_PATH, "wav", split_name, clip_name.replace(".mp3", ".wav"))
            
            # Only run SoX if we haven't converted this specific file yet
            if not os.path.exists(dest_wav):
                sox_cmd = f"sox {src_mp3} -r 16000 -c 1 {dest_wav}"
                subprocess.run(sox_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            f_wav.write(f"{utt_id} {dest_wav}\n")

process_split("train")
process_split("test")
print("Data parsing complete!")