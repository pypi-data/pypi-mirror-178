"""Type definitions / aliases for the sbft API."""
import typing as t

import torch

from torchsilk import type_defs as tdf


class FunctionalModuleWithoutBuffers(t.Protocol[tdf.P, tdf.R]):
    """A module that can be called like a function.

    A type-safe version of functorch's FunctionalModule which is obtained from the
    result of calling functorch.make_functional(...).
    """

    def __call__(
        self,
        parameters: tuple[torch.nn.Parameter, ...],
        *args: tdf.P.args,
        **kwargs: tdf.P.kwargs,
    ) -> tdf.R:
        ...


class FunctionalModuleWithBuffers(t.Protocol[tdf.P, tdf.R]):
    """A module that can be called like a function.

    A type-safe version of functorch's FunctionalModuleWithBuffers which is obtained
    from the result of calling functorch.make_functional(...).
    """

    def __call__(
        self,
        parameters: tuple[torch.nn.Parameter, ...],
        buffers: tuple[torch.Tensor, ...],
        *args: tdf.P.args,
        **kwargs: tdf.P.kwargs,
    ) -> tdf.R:
        ...
