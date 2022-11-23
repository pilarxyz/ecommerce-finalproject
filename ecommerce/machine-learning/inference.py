import torch
import torch.nn.functional as F

from initialization import Model


def inference_process(image_input, model):
    # Data Label
    labels_data ={
        0: "T-Shirt",
        1: "Trouser",
        2: "Pullover",
        3: "Dress",
        4: "Coat",
        5: "Sandal",
        6: "Shirt",
        7: "Sneaker",
        8: "Bag",
        9: "Ankle Boot"
    }

    # Prediction
    result = model(image_input)
    probs = F.softmax(result, dim=1)

    # Confidence and class predict result
    conf, classes = torch.max(probs, 1)

    return labels_data[classes.item()], round(conf.item(), 3)