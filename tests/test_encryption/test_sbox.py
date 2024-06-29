from gigarijndael.encryption.sbox import InvSBox, SBox


def test_s_box(reference_s_box):
    s_box = SBox()

    result_s_box = [s_box[i] for i in range(s_box.finite_field.q)]

    assert result_s_box == reference_s_box


def test_inv_s_box(reference_inv_s_box):
    inv_s_box = InvSBox()

    result_inv_s_box = [inv_s_box[i] for i in range(inv_s_box.finite_field.q)]

    assert result_inv_s_box == reference_inv_s_box
