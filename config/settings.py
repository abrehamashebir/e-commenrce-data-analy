class ModelSettings:
    MODEL_NAME = "xlm-roberta-base"
    TOKENIZER_NAME = "xlm-roberta-base"
    LABELS = {
        "O": 0,
        "B-PRODUCT": 1, "I-PRODUCT": 2,
        "B-PRICE": 3, "I-PRICE": 4,
        "B-LOC": 5, "I-LOC": 6
    }
    ID2LABEL = {v: k for k, v in LABELS.items()}
    
class TrainingSettings:
    BATCH_SIZE = 8
    LEARNING_RATE = 3e-5
    EPOCHS = 5
    MAX_LENGTH = 128