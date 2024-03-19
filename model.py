import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel


# LABELS = ['remember', 'understand', 'apply', 'analyze', 'evaluate', 'create']
LABELS = ['Lembrar', 'Entender', 'Aplicar', 'Analisar', 'Avaliar', 'Criar']

class CognitiveClassifier(nn.Module):
    def __init__(
        self,
        num_cognitive_processes=6,
        bert_model='neuralmind/bert-base-portuguese-cased',
        freeze_bert=True,
        labels=LABELS,
    ):
        super().__init__()
        self.num_cognitive_processes = num_cognitive_processes
        self.tokenizer = AutoTokenizer.from_pretrained(bert_model)
        self.encoder = AutoModel.from_pretrained(bert_model)
        self.fc = nn.Linear(self.encoder.config.hidden_size, num_cognitive_processes)
        self.labels = labels

        if freeze_bert:
            for param in self.encoder.parameters():
                param.requires_grad = False

    def forward(self, **kwargs):
        encodings = self.encoder(**kwargs).last_hidden_state
        encodings = encodings[:, 0, :]
        outputs = self.fc(encodings)
        outputs = torch.sigmoid(outputs)
        return outputs

    def encode(self, **kwargs):
        encodings = self.encoder(**kwargs).last_hidden_state
        encodings = encodings[:, 0, :]
        return encodings

    def encode_text(self, text):
        inputs = self.tokenizer(text, return_tensors='pt', padding=True).to(self.encoder.device)
        encodings = self.encode(**inputs)
        return encodings

    def predict_labels(self, text, return_labels=True, threshold=0.5):
        inputs = self.tokenizer(text, return_tensors='pt', padding=True).to(self.encoder.device)
        outputs = (self.forward(**inputs) > threshold).int().squeeze()

        if return_labels:
            outputs = [LABELS[i] for i in range(len(self.labels)) if outputs[i]]

        return outputs

    def classify(self, text, multilabel=True):
        inputs = self.tokenizer(text, return_tensors='pt', padding=True).to(self.encoder.device)
        encodings = self.encode(**inputs)
        outputs = self.fc(encodings)
        if multilabel:
            outputs = torch.sigmoid(outputs).squeeze()
        else:
            outputs = torch.softmax(outputs, dim=-1).squeeze()

        # outputs = self.forward(**inputs).squeeze()
        outputs = {self.labels[i]: outputs[i].item() for i in range(len(self.labels))}
        return outputs
