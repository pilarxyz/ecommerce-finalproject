import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models

class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()

        self.model = models.mobilenet_v2(pretrained=True)
        self.model.features[0][0] = nn.Conv2d(1, 32, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), bias=False)
        self.model.classifier[1] = nn.Sequential(
            nn.Linear(self.model.last_channel, 1000),
            nn.ReLU(),
            nn.Linear(1000, 11)
        )

    def forward(self, x):
        return F.log_softmax(self.model(x), dim=1)
