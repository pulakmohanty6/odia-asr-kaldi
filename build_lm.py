import math
import os

PROJECT_PATH = "/home/kiit/asr_workspace/odia-asr-kaldi"
text_file = f"{PROJECT_PATH}/data/train/text"

# 1. Gather all unique words
unique_words = set()
with open(text_file, "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) > 1:
            unique_words.update(parts[1:])

# 2. Calculate Uniform Probability
vocab_size = len(unique_words) + 2 
prob = math.log10(1.0 / vocab_size)

# 3. Write standard ARPA format (NO backoff weights for highest order n-grams)
arpa_path = f"{PROJECT_PATH}/data/local/lm.arpa"

# Remove the old .gz file if it exists so we can safely compress the new one later
if os.path.exists(arpa_path + ".gz"):
    os.remove(arpa_path + ".gz")

with open(arpa_path, "w", encoding="utf-8") as f:
    f.write("\\data\\\n")
    f.write(f"ngram 1={vocab_size}\n\n")
    f.write("\\1-grams:\n")
    f.write(f"{prob:.4f}\t<s>\n")
    for w in sorted(unique_words):
        f.write(f"{prob:.4f}\t{w}\n")
    f.write(f"{prob:.4f}\t</s>\n\n")
    f.write("\\end\\\n")

print(f"Uniform ARPA Language Model built with {vocab_size} mathematical parameters!")