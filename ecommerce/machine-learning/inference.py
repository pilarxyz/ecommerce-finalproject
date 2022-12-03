import torch
import torch.nn.functional as F

from initialization import Model


def inference_process(image_input, model):
    # Data Label
    labels_data = {
        0: "Ankle Boot",
        1: "Bag",
        2: "Coat",
        3: "Dress",
        4: "Hat / Cap",
        5: "Pullover",
        6: "Sandal",
        7: "Shirt",
        8: "Sneaker",
        9: "T-Shirt",
        10: "Trouser" 
    }

    # Prediction
    result = model(image_input)
    probs = F.softmax(result, dim=1)

    # Confidence and class predict result
    conf, classes = torch.max(probs, 1)

    return labels_data[classes.item()], round(conf.item(), 3)