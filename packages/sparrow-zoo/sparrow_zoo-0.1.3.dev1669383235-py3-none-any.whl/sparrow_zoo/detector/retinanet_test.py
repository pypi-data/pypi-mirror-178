import torch

from .retinanet import RetinaNet


def test_shapes():
    x = torch.randn(2, 3, 128, 128)
    model = RetinaNet(10, (128, 128)).train()
    outputs = model(x)
    boxes = outputs["boxes"]
    scores = outputs["scores"]
    assert boxes.shape[:2] == scores.shape[:2]
