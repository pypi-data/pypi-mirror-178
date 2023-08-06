from __future__ import annotations

import numpy as np
import torch

from gemovi.common.constants import get_device
from gemovi.common.utils import tensor_to_np

device = get_device(1)


def allow_none_xform_and_tensor_data(func):
    def wrapper(X, **kwargs) -> torch.Tensor:
        if func is None:
            return ensure_tensor(X)
        if isinstance(X, torch.Tensor):
            X = tensor_to_np(X)
        out_kwargs = {}
        for k, v in kwargs.items():
            if isinstance(v, torch.Tensor):
                v = tensor_to_np(v)
            out_kwargs[k] = v

        out = func(X, **out_kwargs)
        return ensure_tensor(out)

    def ensure_tensor(array):
        if isinstance(array, np.ndarray):
            return torch.from_numpy(array).to(device)
        return array

    return wrapper


def _xycallable(
    X: torch.Tensor | np.ndarray, *, y: torch.Tensor = None
) -> torch.Tensor:
    ...


def _xcallable(X: torch.Tensor | np.ndarray) -> torch.Tensor:
    ...


def NoneTransformer(*args, **kwargs):
    return None


class NpOrNoneTransformer:
    wrapped_traits = ["transform", "inverse_transform", "fit", "fit_transform"]
    transform = _xcallable
    inverse_transform = _xcallable
    fit = _xycallable
    fit_transform = _xycallable

    def __init__(self, tformer=None):
        self.tformer = None
        self.set_tformer(tformer)

    def set_tformer(self, tformer=None):
        self.tformer = tformer
        for trait in self.wrapped_traits:
            to_wrap = getattr(self.tformer, trait) if self.tformer else None
            wrapped = allow_none_xform_and_tensor_data(to_wrap)
            setattr(self, trait, wrapped)
