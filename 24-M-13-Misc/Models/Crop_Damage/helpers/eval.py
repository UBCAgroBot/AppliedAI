import torch

def cross_entropy(predictions, targets):
    predictions = predictions.sigmoid()
    return torch.where(targets==1, 1-predictions, predictions).mean()   # why 1 - predictions, and why just 'predictions'?

