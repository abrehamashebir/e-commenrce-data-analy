from transformers import AutoTokenizer
from config.settings import ModelSettings, TrainingSettings
from datasets import Dataset
import numpy as np

class Tokenizer:
    def __init__(self):
        self.settings = ModelSettings()
        self.train_settings = TrainingSettings()
        self.tokenizer = AutoTokenizer.from_pretrained(self.settings.TOKENIZER_NAME)
    
    def tokenize_and_align_labels(self, examples):
        tokenized_inputs = self.tokenizer(
            examples["tokens"],
            truncation=True,
            is_split_into_words=True,
            max_length=self.train_settings.MAX_LENGTH,
            padding="max_length"
        )
        
        labels = []
        for i, label in enumerate(examples["ner_tags"]):
            word_ids = tokenized_inputs.word_ids(batch_index=i)
            previous_word_idx = None
            label_ids = []
            for word_idx in word_ids:
                if word_idx is None:
                    label_ids.append(-100)
                elif word_idx != previous_word_idx:
                    label_ids.append(label[word_idx])
                else:
                    label_ids.append(-100)
                previous_word_idx = word_idx
            labels.append(label_ids)
        
        tokenized_inputs["labels"] = labels
        return tokenized_inputs
    
    def prepare_dataset(self, dataset: Dataset) -> Dataset:
        return dataset.map(
            self.tokenize_and_align_labels,
            batched=True,
            remove_columns=["tokens", "ner_tags"]
        )