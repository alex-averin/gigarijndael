import random

import pytest

from gigarijndael.encryption.sbox import GigaInvSBox, GigaSBox, InvSBox, SBox


def test_s_box(reference_s_box):
    s_box = SBox()

    result_s_box = [s_box[i] for i in range(s_box.finite_field.q)]

    assert result_s_box == reference_s_box


def test_inv_s_box(reference_inv_s_box):
    inv_s_box = InvSBox()

    result_inv_s_box = [inv_s_box[i] for i in range(inv_s_box.finite_field.q)]

    assert result_inv_s_box == reference_inv_s_box


@pytest.mark.parametrize("value", [0, 1, 2, 100500, *(random.getrandbits(32) for _ in range(100))])
def test_giga_s_box(value):
    s_box = GigaSBox()
    inv_s_box = GigaInvSBox()

    assert inv_s_box[s_box[value]] == value
