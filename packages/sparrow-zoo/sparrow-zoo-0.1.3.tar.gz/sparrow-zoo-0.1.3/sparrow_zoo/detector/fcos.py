"""FCOS object detector."""
from __future__ import annotations

from collections import OrderedDict
from typing import Optional

import torch
from torchvision.models import ResNet50_Weights
from torchvision.models.detection import FCOS_ResNet50_FPN_Weights, fcos_resnet50_fpn

from ..transforms import Normalize
from .base import SparrowDetector


class FCOS(SparrowDetector):
    def __init__(
        self,
        num_classes: Optional[int] = None,
        image_shape: tuple[int, int] = (224, 224),
    ) -> None:
        super().__init__()
        self.transform = Normalize()
        if num_classes is None:
            self.detector = fcos_resnet50_fpn(weights=FCOS_ResNet50_FPN_Weights.DEFAULT)
        else:
            self.detector = fcos_resnet50_fpn(
                num_classes=num_classes, weights_backbone=ResNet50_Weights.DEFAULT
            )

        self.anchors, self.num_anchors_per_level = self._generate_anchors(image_shape)

    def forward(self, x: torch.Tensor) -> dict[str, torch.Tensor]:
        x = self.transform(x)
        features: OrderedDict[str, torch.Tensor] = self.detector.backbone(x)
        result = self.detector.head(list(features.values()))
        boxes = self._decode_box_offsets(result["bbox_regression"], self.anchors)
        scores, labels = torch.sigmoid(result["cls_logits"]).max(-1)
        return OrderedDict(boxes=boxes, scores=scores, labels=labels, **result)

    def compute_loss(
        self,
        targets: list[dict[str, torch.Tensor]],
        head_outputs: dict[str, torch.Tensor],
    ) -> dict[str, torch.Tensor]:
        return self.detector.compute_loss(
            targets,
            head_outputs,
            [self.anchors] * len(targets),
            self.num_anchors_per_level,
        )

    def _decode_box_offsets(
        self, box_offsets: torch.Tensor, anchors: torch.Tensor
    ) -> torch.Tensor:
        if box_offsets.device != anchors.device:
            anchors = anchors.to(box_offsets.device)
            self.anchors = anchors

        anchors_center_x = 0.5 * (anchors[:, 0] + anchors[:, 2])
        anchors_center_y = 0.5 * (anchors[:, 1] + anchors[:, 3])
        anchors_w = anchors[:, 2] - anchors[:, 0]
        anchors_h = anchors[:, 3] - anchors[:, 1]
        anchors_scale = torch.stack((anchors_w, anchors_h, anchors_w, anchors_h), dim=1)
        box_offsets = box_offsets * anchors_scale
        boxes1 = anchors_center_x - box_offsets[..., 0]
        boxes2 = anchors_center_y - box_offsets[..., 1]
        boxes3 = anchors_center_x + box_offsets[..., 2]
        boxes4 = anchors_center_y + box_offsets[..., 3]
        boxes = torch.stack((boxes1, boxes2, boxes3, boxes4), dim=-1)
        return boxes
