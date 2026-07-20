from deepmultilingualpunctuation import PunctuationModel
import torch
# Load model (it automatically detects CPU/GPU)
model = PunctuationModel()

# Ensure PyTorch uses CPU
torch_device = torch.device("cpu")
torch.set_default_device(torch_device)  # Forces CPU usage for PyTorch operations

class RePunctuator:
    def __init__(self, speech):
        self.text = speech

    def repunctuate_text(self):
        return model.restore_punctuation(self.text)

    def capitalize_text(self, punc_text):
        tokens = punc_text.split()
        sentences = []
        sent = ''
        for token in tokens:
            if '.' in token or '?' in token or '!' in token:
                sent += token + " "
                cap = sent.capitalize()
                sentences.append(cap.strip())
                sent = ''
            else:
                sent += token + " "
        return " ".join(sentences)
