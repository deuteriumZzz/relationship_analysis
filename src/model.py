import torch
from transformers import BertTokenizer, BertForSequenceClassification

class RelationshipModel:
    def __init__(self, model_name='bert-base-uncased', num_labels=4):
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)

    def predict(self, texts):
        inputs = self.tokenizer(texts, return_tensors='pt', padding=True, truncation=True)
        outputs = self.model(**inputs)
        return outputs.logits.argmax(dim=1)
