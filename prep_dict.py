import os

PROJECT_PATH = "/home/kiit/asr_workspace/odia-asr-kaldi"
text_files = [f"{PROJECT_PATH}/data/train/text", f"{PROJECT_PATH}/data/test/text"]

# 1. Extract all unique words
unique_words = set()
for text_file in text_files:
    with open(text_file, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            # Skip the first part (the utterance ID), keep the words
            if len(parts) > 1:
                unique_words.update(parts[1:])

# 2. Extract all unique characters (phonemes)
unique_chars = set()
for word in unique_words:
    unique_chars.update(list(word))

# Sort everything for Kaldi
unique_words = sorted(list(unique_words))
unique_chars = sorted(list(unique_chars))

# 3. Write Kaldi Dictionary Files
dict_dir = f"{PROJECT_PATH}/data/local/dict"

# Write lexicon.txt (Word -> phoneme phoneme phoneme)
with open(f"{dict_dir}/lexicon.txt", "w", encoding="utf-8") as f:
    f.write("<UNK> SPN\n") # Unknown words are Spoken Noise (SPN)
    for word in unique_words:
        spaced_chars = " ".join(list(word))
        f.write(f"{word} {spaced_chars}\n")

# Write nonsilence_phones.txt (All our Odia characters)
with open(f"{dict_dir}/nonsilence_phones.txt", "w", encoding="utf-8") as f:
    for char in unique_chars:
        f.write(f"{char}\n")

# Write silence_phones.txt
with open(f"{dict_dir}/silence_phones.txt", "w", encoding="utf-8") as f:
    f.write("SIL\nSPN\n")

# Write optional_silence.txt
with open(f"{dict_dir}/optional_silence.txt", "w", encoding="utf-8") as f:
    f.write("SIL\n")

# Write extra_questions.txt (Leave empty but required by Kaldi)
with open(f"{dict_dir}/extra_questions.txt", "w", encoding="utf-8") as f:
    f.write("\n")

print(f"Lexicon built! Found {len(unique_words)} unique words and {len(unique_chars)} unique phonemes.")