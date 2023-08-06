from __future__ import annotations

import torchvision.transforms as T


class Normalize(T.Normalize):
    """Normalize with standard default rgb mean/std."""

    def __init__(
        self,
        mean: tuple[float, float, float] = (0.485, 0.456, 0.406),
        std: tuple[float, float, float] = (0.229, 0.224, 0.225),
        inplace: bool = False,
    ) -> None:
        super().__init__(mean, std, inplace)
