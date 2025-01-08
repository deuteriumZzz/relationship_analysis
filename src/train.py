import pandas as pd
from sklearn.model_selection import train_test_split
import torch
from torch.utils.data import DataLoader, Dataset
from model import RelationshipModel

class RelationshipDataset(Dataset):
    def __init__(self, texts, labels):
        self.texts = texts
        self.labels = labels

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        return self.texts[idx], self.labels[idx]

def train_model(df):
    model = RelationshipModel()
    X_train, X_test, y_train, y_test = train_test_split(df['cleaned_text'], df['label'], test_size=0.2)
    
    train_dataset = RelationshipDataset(X_train.tolist(), y_train.tolist())
    train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)

    # Обучение модели
    model.model.train()
    for epoch in range(3):  # Пример: 3 эпохи
        for texts, labels in train_loader:
            # Обучение кода здесь
            pass
    
    return model
