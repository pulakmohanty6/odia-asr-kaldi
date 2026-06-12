import os
import pandas as pd
import subprocess

# Paths
DATASET_PATH = "/home/kiit/asr_workspace/cv-corpus-25.0-2026-03-09/or" 
PROJECT_PATH = "/home/kiit/asr_workspace/odia-asr-kaldi"

def clean_odia_text(text):
    text = str(text)
    # The Nuclear Option: KEEP ONLY Odia Unicode characters and standard spaces
    text = ''.join(c for c in text if '\u0B00' <= c <= '\u0B7F' or c == ' ')
    text = ' '.join(text.split())
    return text

print("Unlocking the Mozilla Validated AND Unvalidated Vaults...")

# 1. Load the TEST set first (so we know what to avoid)
test_df = pd.read_csv(os.path.join(DATASET_PATH, "test.tsv"), sep='\t')
test_clips = set(test_df['path'].tolist())

# 2. Load the Validated AND Other sets
val_df = pd.read_csv(os.path.join(DATASET_PATH, "validated.tsv"), sep='\t')
other_df = pd.read_csv(os.path.join(DATASET_PATH, "other.tsv"), sep='\t')

# Merge them into one gigantic pool
massive_pool = pd.concat([val_df, other_df], ignore_index=True)

# 3. Create the true Maximum Train Set (Everything EXCEPT the test clips)
train_df = massive_pool[~massive_pool['path'].isin(test_clips)]

print(f"Total Test Clips Found: {len(test_df)}")
print(f"Total Train Clips Pooled (Validated + Other): {len(train_df)}\n")

def process_dataframe(df, split_name):
    print(f"Processing {split_name} split...")
    os.makedirs(f"{PROJECT_PATH}/data/{split_name}", exist_ok=True)
    os.makedirs(f"{PROJECT_PATH}/wav/{split_name}", exist_ok=True)
    
    total_rows = len(df)
    processed_count = 0
    
    with open(f"{PROJECT_PATH}/data/{split_name}/text", "w", encoding="utf-8") as f_text, \
         open(f"{PROJECT_PATH}/data/{split_name}/wav.scp", "w") as f_wav, \
         open(f"{PROJECT_PATH}/data/{split_name}/utt2spk", "w") as f_utt2spk:
        
        for idx, row in df.iterrows():
            client_id = str(row['client_id'])[:8] 
            clip_name = str(row['path'])
            sentence = clean_odia_text(row['sentence'])
            
            if not sentence:
                continue
                
            utt_id = f"{client_id}-{clip_name.replace('.mp3', '')}"
            src_mp3 = os.path.join(DATASET_PATH, "clips", clip_name)
            dest_wav = os.path.join(PROJECT_PATH, "wav", split_name, clip_name.replace(".mp3", ".wav"))
            
            # Convert audio if needed
            if not os.path.exists(dest_wav):
                if os.path.exists(src_mp3):
                    sox_cmd = f"sox '{src_mp3}' -r 16000 -c 1 '{dest_wav}'"
                    subprocess.run(sox_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                else:
                    continue 
            
            f_text.write(f"{utt_id} {sentence}\n")
            f_utt2spk.write(f"{utt_id} {client_id}\n")
            f_wav.write(f"{utt_id} {dest_wav}\n")
            
            processed_count += 1
            if processed_count % 1000 == 0:
                print(f"-> Processed {processed_count}/{total_rows} valid utterances...")

    print(f"Finished {split_name}! Saved {processed_count} pure Odia utterances.\n")

# Execute the pipeline
process_dataframe(test_df, "test")
process_dataframe(train_df, "train")
print("Data parsing complete! 16-Core extraction is ready.")