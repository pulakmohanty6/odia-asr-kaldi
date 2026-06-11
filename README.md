# Odia Automatic Speech Recognition (ASR) Pipeline (Kaldi)

This repository contains an end-to-end Automatic Speech Recognition (ASR) pipeline built from scratch using the **Kaldi** toolkit, specifically engineered for **Odia**, an underrepresented Indic language. 

Currently at **Version 1.0 (Baseline)**, this project demonstrates the complete construction of an acoustic model, custom data preparation, feature extraction, and graph compilation without relying on black-box wrappers.

## 🛠️ Architecture & Tech Stack
* **Framework:** Kaldi (C++ Engine)
* **Scripting:** Bash (Pipeline automation, graph compilation), Python 3 (Data wrangling, ARPA generation)
* **Audio Processing:** SoX (16kHz downsampling, 1-channel mono conversion)
* **Acoustic Features:** MFCC (Mel-Frequency Cepstral Coefficients) with CMVN
* **Acoustic Model:** Monophone GMM-HMM

## 🚀 Engineering Highlights & Problem Solving
Building an Indic language ASR on Kaldi (which is historically English-centric) required significant custom engineering:

1. **Custom Unicode Data Pipeline:** Kaldi's default C++ string validators frequently crash on complex Unicode. I wrote a custom Python regex pipeline to strictly filter invisible formatting artifacts (Zero-Width Joiners) and parse the Mozilla Common Voice TSV dataset into Kaldi-compliant `.scp` and tracking files.
2. **Algorithmic Phonetic Lexicon:** Instead of relying on manual linguistic phonetic mappings (which are unavailable for Odia), I leveraged the perfectly phonetic nature of the Odia script. I wrote a generator to mathematically map all 3,895 unique vocabulary words to their 63 raw Unicode character bases, compiling it into an optimized `L.fst` graph.
3. **From-Scratch Language Modeling:** Bypassed heavy external tools like SRILM to generate a strictly formatted Unigram ARPA model using custom Python logic, avoiding backoff-weight violations and compiling it natively into Kaldi's `G.fst`.

## 📊 Current Results (v1.0 Baseline)
* **Model Type:** Monophone (Isolated phoneme training)
* **Dataset:** 500-sentence random subset (Mozilla Common Voice)
* **Word Error Rate (WER): 93.19%**

*Note on WER:* This high baseline error rate is scientifically expected at this stage. It mathematically validates that the `HCLG.fst` graph and audio alignments are structurally sound, despite being limited by a Unigram Language Model and a context-independent monophone acoustic model. 

## ⏭️ Next Steps (Phase 13+)
* **Triphone Training:** Implement context-dependent acoustic modeling to account for co-articulation.
* **N-Gram Language Model:** Upgrade from a Unigram to a Trigram model using SRILM to give the AI contextual grammar probability.
* **Dataset Expansion:** Scale training from 500 sentences to the full dataset using cloud compute clusters.
