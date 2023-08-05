from typing import Union

import torch
from torch import Tensor

from model.base_model import BaseSequentialSpatioTemporal
from model.utils import GnnWrap


class Linear(BaseSequentialSpatioTemporal):
    def __init__(self, input_feature_size, output_feature_size, hidden_feature_size):
        super().__init__(input_feature_size, output_feature_size, hidden_feature_size)

    def __init_spatio_temporal_layer__(self) -> torch.nn.Module:
        return GnnWrap(torch.nn.Linear(self.input_feature_size, self.hidden_feature_size))
