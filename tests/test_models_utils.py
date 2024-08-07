import pytest
import torch

from valle.models.utils import build_attn_mask, build_pad_mask


@pytest.mark.parametrize(
    'x_len, y_len, expected_mask',
    [
        (
            5,
            5,
            torch.tensor(
                [
                    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
                    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                ],
                dtype=torch.bool,
            ),
        )
    ],
)
def test_build_attn_mask(x_len: int, y_len: int, expected_mask: torch.Tensor):
    mask = build_attn_mask(x_len, y_len, device='cpu')
    assert mask.shape == expected_mask.shape
    assert torch.equal(mask, expected_mask)


@pytest.mark.parametrize(
    'lens, expected_mask',
    [
        (
            torch.tensor([5, 5, 5, 5]),
            torch.tensor(
                [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
                dtype=torch.bool,
            ),
        ),
        (
            torch.tensor([5, 4, 3, 2]),
            torch.tensor(
                [[0, 0, 0, 0, 0], [0, 0, 0, 0, 1], [0, 0, 0, 1, 1], [0, 0, 1, 1, 1]],
                dtype=torch.bool,
            ),
        ),
    ],
)
def test_build_pad_mask(lens, expected_mask):
    mask = build_pad_mask(lens, device='cpu')
    assert mask.shape == expected_mask.shape
    assert torch.equal(mask, expected_mask)
