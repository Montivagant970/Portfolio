import sys
sys.path.append("../")
import torch

from utils.feature import load_wav
from typing import Dict

class DefaultCollate:
    def __init__(self, processor, sr) -> None:
        self.processor = processor
        self.sr = sr

    def __call__(self, inputs) -> Dict[str, torch.tensor]:
        features, transcripts = zip(*inputs)
        features, transcripts = list(features), list(transcripts)

        # Normalize each feature (audio waveform) to be in range [-1, 1] JAY
        # features = [f / max(abs(f)) for f in features] JAY

        # Explicitly call feature extractor for audio processing
        batch = self.processor.feature_extractor(
            features, sampling_rate=self.sr, return_tensors="pt", padding="longest"
        )

        # Explicitly call tokenizer for transcripts
        labels_batch = self.processor.tokenizer(
            transcripts, return_tensors="pt", padding="longest"
        )

        # Add labels to batch with padding masked
        batch["labels"] = labels_batch["input_ids"].masked_fill(labels_batch.attention_mask.ne(1), -100)

        return batch

class Dataset:
    def __init__(self, data, sr, preload_data, transform = None):
        self.data = data
        self.sr = sr
        self.transform = transform
        self.preload_data = preload_data
        
    def __len__(self) -> int:
        return len(self.data)
        
    def __getitem__(self, idx) -> tuple:
        item = self.data.iloc[idx]
        if not self.preload_data:
            feature = load_wav(item['path'], sr = self.sr)
        else:
            feature = item['wav']
        
        return feature, item['transcript']
