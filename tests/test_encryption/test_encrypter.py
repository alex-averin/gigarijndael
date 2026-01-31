import pytest

from gigarijndael.encryption.encrypter import RijndaelEncrypter
from gigarijndael.encryption.word import Word


@pytest.mark.parametrize(
    ("block_size", "key_size", "expected_rounds_number"),
    [
        (4, 4, 10),
        (4, 6, 12),
        (4, 8, 14),
        (6, 4, 12),
        (6, 6, 12),
        (6, 8, 14),
        (8, 4, 14),
        (8, 6, 14),
        (8, 8, 14),
    ],
)
def test_rounds_number(block_size, key_size, expected_rounds_number):
    encrypter = RijndaelEncrypter(block_size=block_size, key_size=key_size)

    assert encrypter.rounds_number == expected_rounds_number


@pytest.mark.parametrize(
    ("block_size", "key_size", "expected"),
    [
        (
            4,
            4,
            (
                0x01000000,
                0x02000000,
                0x04000000,
                0x08000000,
                0x10000000,
                0x20000000,
                0x40000000,
                0x80000000,
                0x1B000000,
                0x36000000,
            ),
        )
    ],
)
def test_round_constants(block_size, key_size, expected):
    encrypter = RijndaelEncrypter(block_size=block_size, key_size=key_size)

    round_constants = encrypter.round_constants

    assert round_constants == expected


@pytest.mark.parametrize("key_size", [4, 6, 8])
@pytest.mark.parametrize(
    ("block_size", "expected"), [(4, (0, 1, 2, 3)), (6, (0, 1, 2, 3)), (8, (0, 1, 3, 4))]
)
def test_shift_row_sizes(block_size, key_size, expected):
    encrypter = RijndaelEncrypter(block_size=block_size, key_size=key_size)

    assert encrypter.shift_row_sizes == expected


@pytest.mark.parametrize("key_size", [4, 6, 8])
def test__key_expansion_length(key_size):
    key = [Word(0x00000000)] * key_size
    encrypter = RijndaelEncrypter(block_size=key_size, key_size=key_size)

    key_schedule = encrypter._key_expansion(key)

    assert len(key_schedule) == (encrypter.rounds_number + 1) * key_size


def test_sub_word():
    encrypter = RijndaelEncrypter(block_size=4, key_size=4)
    word = Word(0x00010203)
    # SBox[0x00]=0x63, SBox[0x01]=0x7C, SBox[0x02]=0x77, SBox[0x03]=0x7B
    expected = Word(0x637C777B)
    assert encrypter.sub_word(word) == expected


def test_add_round_key():
    encrypter = RijndaelEncrypter(block_size=4, key_size=4)
    state = [Word(0), Word(0), Word(1), Word(1)]
    round_key = [Word(1), Word(0), Word(1), Word(0)]
    expected_result = [Word(1), Word(0), Word(0), Word(1)]

    assert encrypter._add_round_key(state, round_key) == expected_result


def test_sub_elements():
    encrypter = RijndaelEncrypter(block_size=4, key_size=4)
    state = [Word(0x00000101), Word(0x03030707), Word(0x0F0F1F1F), Word(0x3F3F7F7F)]
    expected_state = [Word(0x63637C7C), Word(0x7B7BC5C5), Word(0x7676C0C0), Word(0x7575D2D2)]

    assert encrypter._sub_elements(state=state) == expected_state


def test_inv_sub_elements():
    encrypter = RijndaelEncrypter(block_size=4, key_size=4)
    state = [Word(0x63637C7C), Word(0x7B7BC5C5), Word(0x7676C0C0), Word(0x7575D2D2)]
    expected_state = [Word(0x00000101), Word(0x03030707), Word(0x0F0F1F1F), Word(0x3F3F7F7F)]

    assert encrypter._inv_sub_elements(state=state) == expected_state


def test_shift_rows():
    encrypter = RijndaelEncrypter(block_size=4, key_size=4)
    state = [Word(0x63637C7C), Word(0x7B7BC5C5), Word(0x7676C0C0), Word(0x7575D2D2)]
    expected_state = [Word(0x637BC0D2), Word(0x7B76D27C), Word(0x76757CC5), Word(0x7563C5C0)]

    assert encrypter._shift_rows(state) == expected_state


def test_inv_shift_rows():
    encrypter = RijndaelEncrypter(block_size=4, key_size=4)
    state = [Word(0x637BC0D2), Word(0x7B76D27C), Word(0x76757CC5), Word(0x7563C5C0)]
    expected_state = [Word(0x63637C7C), Word(0x7B7BC5C5), Word(0x7676C0C0), Word(0x7575D2D2)]

    assert encrypter._inv_shift_rows(state) == expected_state


def test_mix_columns():
    encrypter = RijndaelEncrypter(block_size=4, key_size=4)
    state = [Word(0x637BC0D2), Word(0x7B76D27C), Word(0x76757CC5), Word(0x7563C5C0)]
    expected_state = [Word(0x591CEEA1), Word(0xC28636D1), Word(0xCADDAF02), Word(0x4A27DCA2)]

    assert encrypter._mix_columns(state) == expected_state


def test_inv_mix_columns():
    encrypter = RijndaelEncrypter(block_size=4, key_size=4)
    state = [Word(0x591CEEA1), Word(0xC28636D1), Word(0xCADDAF02), Word(0x4A27DCA2)]
    expected_state = [Word(0x637BC0D2), Word(0x7B76D27C), Word(0x76757CC5), Word(0x7563C5C0)]

    assert encrypter._inv_mix_columns(state) == expected_state


def test_round_encrypt():
    encrypter = RijndaelEncrypter(block_size=4, key_size=4)
    key = [Word(0x00000000), Word(0x00000000), Word(0x00000000), Word(0x00000000)]
    state = [Word(0x00000101), Word(0x03030707), Word(0x0F0F1F1F), Word(0x3F3F7F7F)]
    key_schedule = encrypter._key_expansion(key)
    expected_result = [Word(0x3B7F8DC2), Word(0xA0E555B2), Word(0xA8BECC61), Word(0x2844BFC1)]

    result = encrypter._round(state=state, round_key=key_schedule[4:8])

    assert result == expected_result


def test_state_encrypt():
    encrypter = RijndaelEncrypter(block_size=4, key_size=4)
    key = [Word(0x00000000), Word(0x00000000), Word(0x00000000), Word(0x00000000)]
    state = [Word(0x00000101), Word(0x03030707), Word(0x0F0F1F1F), Word(0x3F3F7F7F)]
    key_schedule = encrypter._key_expansion(key)

    # Init AddRoundKey
    state = encrypter._add_round_key(state, key_schedule[0:4])
    # Rounds 1-9
    for i in range(1, 10):
        state = encrypter._round(state, key_schedule[i * 4 : (i + 1) * 4])
    # Final round
    state = encrypter._round(state, key_schedule[40:44], is_final=True)

    expected_state = [Word(0xC7D12419), Word(0x489E3B62), Word(0x33A2C5A7), Word(0xF4563172)]
    assert state == expected_state


def test_state_decrypt():
    encrypter = RijndaelEncrypter(block_size=4, key_size=4)
    key = [Word(0x00000000), Word(0x00000000), Word(0x00000000), Word(0x00000000)]
    state = [Word(0xC7D12419), Word(0x489E3B62), Word(0x33A2C5A7), Word(0xF4563172)]
    key_schedule = encrypter._key_expansion(key)

    init_key, round_keys = encrypter._round_keys(key_schedule, decrypt=True)
    state = encrypter._add_round_key(state, init_key)
    for i in range(encrypter.rounds_number - 1):
        state = encrypter._inverse_round(state, round_keys[i])
    state = encrypter._inverse_round(state, round_keys[encrypter.rounds_number - 1], is_final=True)

    expected_state = [Word(0x00000101), Word(0x03030707), Word(0x0F0F1F1F), Word(0x3F3F7F7F)]
    assert state == expected_state


def test_encrypt():
    encrypter = RijndaelEncrypter(block_size=4, key_size=4)
    key = [Word(0x00000000), Word(0x00000000), Word(0x00000000), Word(0x00000000)]
    blocks = [
        (
            0x00,
            0x00,
            0x01,
            0x01,
            0x03,
            0x03,
            0x07,
            0x07,
            0x0F,
            0x0F,
            0x1F,
            0x1F,
            0x3F,
            0x3F,
            0x7F,
            0x7F,
        )
    ]
    expected_cipher_blocks = [
        (
            0xC7,
            0xD1,
            0x24,
            0x19,
            0x48,
            0x9E,
            0x3B,
            0x62,
            0x33,
            0xA2,
            0xC5,
            0xA7,
            0xF4,
            0x56,
            0x31,
            0x72,
        )
    ]

    assert encrypter.encrypt(blocks=blocks, key=key, decrypt=False) == expected_cipher_blocks


def test_decrypt():
    encrypter = RijndaelEncrypter(block_size=4, key_size=4)
    key = [Word(0x00000000), Word(0x00000000), Word(0x00000000), Word(0x00000000)]
    blocks = [
        (
            0xC7,
            0xD1,
            0x24,
            0x19,
            0x48,
            0x9E,
            0x3B,
            0x62,
            0x33,
            0xA2,
            0xC5,
            0xA7,
            0xF4,
            0x56,
            0x31,
            0x72,
        )
    ]
    expected_blocks = [
        (
            0x00,
            0x00,
            0x01,
            0x01,
            0x03,
            0x03,
            0x07,
            0x07,
            0x0F,
            0x0F,
            0x1F,
            0x1F,
            0x3F,
            0x3F,
            0x7F,
            0x7F,
        )
    ]

    assert encrypter.encrypt(blocks=blocks, key=key, decrypt=True) == expected_blocks
