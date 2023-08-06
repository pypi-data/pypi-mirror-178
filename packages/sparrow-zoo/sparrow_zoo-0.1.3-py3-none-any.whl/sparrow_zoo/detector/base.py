from __future__ import annotations

from typing import Union

import torch
from torchvision.models.detection import FCOS, RetinaNet
from torchvision.models.detection.image_list import ImageList

from ..base import SparrowModel


class SparrowDetector(SparrowModel):
    """Sparrow object detection model."""

    output_names: tuple[str, str, str] = ("boxes", "scores", "labels")
    detector: Union[FCOS, RetinaNet]

    def _generate_anchors(self, image_shape: tuple[int, int]) -> torch.Tensor:
        _fake_images = torch.randn(1, 3, *image_shape)
        image_list = ImageList(_fake_images, [_fake_images.shape[-2:]])
        features = list(self.detector.backbone(_fake_images).values())
        num_anchors_per_level = [x.size(2) * x.size(3) for x in features]
        return (
            self.detector.anchor_generator(image_list, features)[0],
            num_anchors_per_level,
        )
