# Vision-Language-Action (VLA) Systems

## What is a VLA?
VLA models are the physical equivalent of LLMs. They take Vision (images) and Language (instructions) as input, and output Actions (robot production commands).

## Examples
- **RT-2 (Google DeepMind)**: One of the first large scale VLA models.
- **Octo**: An open-source general purpose robot policy.

## Architecture
Typically uses a ViT (Vision Transformer) to encode images and a Transformer decoder (like GPT) to generate tokenized actions which are then detokenized into continuous motor commands.
