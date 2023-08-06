from __future__ import annotations

from typing import Optional

import torch
from torchvision.models import ResNet50_Weights
from torchvision.models.detection import (
    RetinaNet_ResNet50_FPN_V2_Weights,
    retinanet_resnet50_fpn_v2,
)

from ..transforms import Normalize
from .base import SparrowDetector


class RetinaNet(SparrowDetector):
    def __init__(
        self,
        num_classes: Optional[int] = None,
        image_shape: tuple[int, int] = (224, 224),
    ) -> None:
        super().__init__()
        self.transform = Normalize()
        if num_classes is None:
            self.detector = retinanet_resnet50_fpn_v2(
                weights=RetinaNet_ResNet50_FPN_V2_Weights.DEFAULT
            )
        else:
            self.detector = retinanet_resnet50_fpn_v2(
                num_classes=num_classes, weights_backbone=ResNet50_Weights.DEFAULT
            )

        self.anchors, self.num_anchors_per_level = self._generate_anchors(image_shape)

    def forward(self, x: torch.Tensor) -> dict[str, torch.Tensor]:
        batch_size = x.shape[0]
        x = self.transform(x)
        features = self.detector.backbone(x)
        features = list(features.values())
        result = self.detector.head(features)
        if result["bbox_regression"].device != self.anchors.device:
            self.anchors = self.anchors.to(result["bbox_regression"].device)
        result["boxes"] = self.detector.box_coder.decode(
            result["bbox_regression"], [self.anchors] * batch_size
        ).permute(1, 0, 2)
        result["scores"], result["labels"] = torch.sigmoid(result["cls_logits"]).max(-1)
        return result

    def compute_loss(
        self,
        targets: list[dict[str, torch.Tensor]],
        head_outputs: dict[str, torch.Tensor],
    ) -> dict[str, torch.Tensor]:
        return self.detector.compute_loss(
            targets,
            head_outputs,
            [self.anchors] * len(targets),
        )
