from typing import List, Tuple
from config.paths import paths
from config.settings import ModelSettings

class CoNLLFormatter:
    def __init__(self):
        self.settings = ModelSettings()
    
    def convert_to_conll(self, tokens: List[str], tags: List[str]) -> str:
        """Convert token-tag pairs to CoNLL format"""
        lines = []
        for i, (token, tag) in enumerate(zip(tokens, tags), start=1):
            lines.append(f"{i}\t{token}\t_\t{tag}\t_\t_\t_\t_\t_\t_")
        return "\n".join(lines)
    
    def save_conll_file(self, data: List[Tuple[List[str], List[str]]], filename: str):
        """Save multiple labeled sentences to a CoNLL file"""
        path = paths.LABELED_DATA / filename
        with open(path, 'w', encoding='utf-8') as f:
            for tokens, tags in data:
                f.write(self.convert_to_conll(tokens, tags))
                f.write("\n\n")  # Sentence separator