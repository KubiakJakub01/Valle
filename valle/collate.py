from dataclasses import dataclass

import torch
import torch.nn.functional as F
from torch import Tensor
from torch.nn.utils.rnn import pad_sequence

from .config import ConfigValle


def get_collate(model_name: str):
    collate_dict = {
        'valle_ar': ValleARCollate,
    }
    return collate_dict[model_name]


@dataclass
class ValleARCollate:
    config: ConfigValle

    def __call__(self, batch: list[dict[str, Tensor]]) -> dict[str, Tensor]:
        codes_list = []
        targets_list = []
        tokens_list = []
        for item in batch:
            codes_ = item['codes']
            codes = F.pad(codes_, (1, 0), value=self.config.bos_token)
            targets = F.pad(codes_, (0, 1), value=self.config.eos_token)
            codes_list.append(codes)
            targets_list.append(targets)
            tokens_list.append(item['tokens'])
        codes, codes_lens = collate_list(codes_list)
        targets, _ = collate_list(targets_list)
        tokens, tokens_lens = collate_list(tokens_list)
        assert codes_lens > tokens_lens, 'Codes length must be greater than tokens length.'
        return {
            'codes': codes,
            'codes_lens': codes_lens,
            'targets': targets,
            'tokens': tokens,
            'tokens_lens': tokens_lens,
        }


def collate_list(x_list: list[Tensor]) -> tuple[Tensor, Tensor]:
    x_lens = torch.tensor(list(map(len, x_list)), dtype=torch.int64)
    x = pad_sequence(x_list, batch_first=True)
    return x, x_lens
