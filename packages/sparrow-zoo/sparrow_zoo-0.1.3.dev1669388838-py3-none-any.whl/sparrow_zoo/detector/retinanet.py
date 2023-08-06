from __future__ import annotations

import math
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
        self.bbox_xform_clip: Optional[torch.Tensor] = None

    def forward(self, x: torch.Tensor) -> dict[str, torch.Tensor]:
        x = self.transform(x)
        features = self.detector.backbone(x)
        features = list(features.values())
        result = self.detector.head(features)
        result["boxes"] = self._decode_box_offsets(
            result["bbox_regression"], self.anchors
        )
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

    def _decode_box_offsets(
        self, box_offsets: torch.Tensor, anchors: torch.Tensor
    ) -> torch.Tensor:
        if box_offsets.device != anchors.device:
            anchors = anchors.to(box_offsets.device)
            self.anchors = anchors

        widths = anchors[:, 2] - anchors[:, 0]
        heights = anchors[:, 3] - anchors[:, 1]
        ctr_x = anchors[:, 0] + 0.5 * widths
        ctr_y = anchors[:, 1] + 0.5 * heights

        dx = box_offsets[..., 0::4]
        dy = box_offsets[..., 1::4]
        dw = box_offsets[..., 2::4]
        dh = box_offsets[..., 3::4]

        # # Prevent sending too large values into torch.exp()
        if self.bbox_xform_clip is None:
            self.bbox_xform_clip = torch.ones_like(dw) * math.log(1000.0 / 16)
        dw = torch.minimum(dw, self.bbox_xform_clip)
        dh = torch.minimum(dh, self.bbox_xform_clip)

        pred_ctr_x = dx * widths[:, None] + ctr_x[:, None]
        pred_ctr_y = dy * heights[:, None] + ctr_y[:, None]
        pred_w = torch.exp(dw) * widths[:, None]
        pred_h = torch.exp(dh) * heights[:, None]

        # Distance from center to box's corner.
        c_to_c_h = (
            torch.tensor(0.5, dtype=pred_ctr_y.dtype, device=pred_h.device) * pred_h
        )
        c_to_c_w = (
            torch.tensor(0.5, dtype=pred_ctr_x.dtype, device=pred_w.device) * pred_w
        )

        pred_boxes1 = pred_ctr_x - c_to_c_w
        pred_boxes2 = pred_ctr_y - c_to_c_h
        pred_boxes3 = pred_ctr_x + c_to_c_w
        pred_boxes4 = pred_ctr_y + c_to_c_h
        return torch.cat((pred_boxes1, pred_boxes2, pred_boxes3, pred_boxes4), dim=-1)
