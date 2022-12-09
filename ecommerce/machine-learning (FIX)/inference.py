import torch
import torch.nn.functional as F
import numpy as np

class Inference:
    def __init__(self, model, input_image):
        self.model = model
        self.input_image = input_image

    def forward(self):
        # with torch.no_grad():
        result = self.model(self.input_image)
        probs = F.softmax(result, dim=1)
        confidence, classes = torch.max(probs, 1)
        
        print("Predict Done")
        print("Confidence :", confidence, "Prediction :", classes)
        
        return classes