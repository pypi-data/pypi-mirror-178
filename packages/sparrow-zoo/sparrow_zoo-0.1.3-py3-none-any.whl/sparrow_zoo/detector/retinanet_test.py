import torch

from .retinanet import RetinaNet


def test_shapes():
    x = torch.randn(2, 3, 128, 128)
    model = RetinaNet(10, (128, 128)).train()
    outputs = model(x)
    boxes = outputs["boxes"]
    scores = outputs["scores"]
    assert boxes.shape[:2] == scores.shape[:2]


def test_compute_loss():
    x = torch.randn(2, 3, 128, 128)
    model = RetinaNet(10, (128, 128)).train()
    outputs = model(x)
    targets = [
        {
            "boxes": torch.cat(
                [torch.rand((n_boxes, 2)) * 112, torch.rand((n_boxes, 2)) * 112 + 112],
                dim=1,
            ),
            "labels": torch.randint(0, 10, (n_boxes,)),
        }
        for n_boxes in [5, 7]
    ]
    for loss in model.compute_loss(targets, outputs).values():
        assert loss > 0
