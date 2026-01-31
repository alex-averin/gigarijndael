import pytest

from gigarijndael.encryption.word import GigaWord, Word


@pytest.mark.parametrize(
    ("word_cls", "value"), [(Word, 1 << Word.size_bits()), (GigaWord, 1 << GigaWord.size_bits())]
)
def test_word_init_size_validation(word_cls, value):
    with pytest.raises(ValueError, match="Word length cannot be more than"):
        word_cls(value)


@pytest.mark.parametrize("word_cls", [Word, GigaWord])
def test_word_init_default_zero(word_cls):
    word = word_cls()

    assert int(word) == 0
    assert bool(word) is False


@pytest.mark.parametrize(
    ("word_cls", "value"), [(Word, 0x12345678), (GigaWord, 0x12345678ABCDEF90)]
)
def test_word_init(word_cls, value):
    """Тест создания слова с валидными значениями."""
    word = word_cls(value)
    assert int(word) == value


@pytest.mark.parametrize(
    ("word_cls", "items", "expected_integer"),
    [
        (Word, [0x12, 0x34, 0x56, 0x78], 0x12345678),
        (
            GigaWord,
            [0x12345678, 0x9ABCDEF0, 0x11223344, 0x55667788],
            0x123456789ABCDEF01122334455667788,
        ),
    ],
)
def test_word_from_items(word_cls, items, expected_integer):
    word = word_cls.from_items(items)

    assert list(word) == items
    assert int(word) == expected_integer


@pytest.mark.parametrize("word_cls", [Word, GigaWord])
def test_word_from_items_empty(word_cls):
    word = word_cls.from_items([])

    assert int(word) == 0
    assert bool(word) is False


@pytest.mark.parametrize(
    ("shift", "expected"),
    [
        (0, 0x00112233),
        (1, 0x11223300),
        (2, 0x22330011),
        (3, 0x33001122),
        (4, 0x00112233),
        (5, 0x11223300),
    ],
)
def test_word_lshift(shift, expected):
    assert Word(0x00112233) << shift == expected


@pytest.mark.parametrize(
    ("shift", "expected"),
    [
        (0, 0x00112233),
        (1, 0x33001122),
        (2, 0x22330011),
        (3, 0x11223300),
        (4, 0x00112233),
        (5, 0x33001122),
    ],
)
def test_word_rshift(shift, expected):
    assert Word(0x00112233) >> shift == expected


def test_word_xor():
    assert Word(0x00112233) ^ Word(0x11223300) == Word(0x11331133)


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        (Word(1), Word(1), True),
        (Word(1), Word(2), False),
        (Word(1), 1, True),
        (1, Word(1), True),
        (Word(1), 2, False),
        (1, Word(2), False),
    ],
)
def test_word_eq(left, right, expected):
    assert (left == right) is expected


@pytest.mark.parametrize("word_cls", [Word, GigaWord])
@pytest.mark.parametrize(("value", "expected"), [(0, False), (1, True)])
def test_word_bool(word_cls, value, expected):
    assert bool(word_cls(value)) is expected


@pytest.mark.parametrize(
    ("index", "expected_value"),
    [(0, 0x00), (1, 0x11), (2, 0x22), (3, 0x33), (-1, 0x33), (-2, 0x22), (-3, 0x11), (-4, 0x00)],
)
def test_word_getitem_valid(index, expected_value):
    word = Word(0x00112233)

    assert word[index] == expected_value


@pytest.mark.parametrize("index", [4, 5, -5, -6])
def test_word_getitem_invalid(index):
    with pytest.raises(IndexError, match="Word index out of range"):
        Word()[index]


@pytest.mark.parametrize("index", [4, 5, -5])
def test_word_getitem_index_error(index):
    with pytest.raises(IndexError):
        Word()[index]


def test_word_setitem():
    first = Word()
    second = Word()
    first[0] = 0x00
    first[1] = 0x11
    first[2] = 0x22
    first[3] = 0x33
    second[-4] = 0x00
    second[-3] = 0x11
    second[-2] = 0x22
    second[-1] = 0x33

    assert first == second == 0x00112233


@pytest.mark.parametrize("index", [4, 5, -5, -6])
def test_word_setitem_index_error(index):
    with pytest.raises(IndexError, match="Word assignment index out of range"):
        Word()[index] = 0x1


def test_word_setitem_value_too_large():
    word = Word()
    with pytest.raises(ValueError, match="Item length cannot be more than"):
        word[0] = 0x100


def test_word_iter_forward():
    word = Word(0x00112233)

    assert list(word) == [0x00, 0x11, 0x22, 0x33]


def test_word_iter_manual():
    word = Word(0x00112233)
    expected_bytes = [0x00, 0x11, 0x22, 0x33]

    iterator = iter(word)

    for expected_byte in expected_bytes:
        assert next(iterator) == expected_byte
    with pytest.raises(StopIteration):
        next(iterator)


def test_word_reversed():
    word = Word(0x00112233)

    assert list(reversed(word)) == [0x33, 0x22, 0x11, 0x00]


def test_word_reversed_manual():
    word = Word(0x00112233)
    expected_bytes = [0x33, 0x22, 0x11, 0x00]

    rev_iterator = reversed(word)

    for expected_byte in expected_bytes:
        assert next(rev_iterator) == expected_byte
    with pytest.raises(StopIteration):
        next(rev_iterator)


@pytest.mark.parametrize("word_cls", [Word, GigaWord])
def test_word_length(word_cls):
    assert len(word_cls()) == word_cls.LENGTH


@pytest.mark.parametrize(
    ("word_cls", "expected_bytes"),
    [
        (Word, b"\x01\x02\x03\x04"),
        (GigaWord, b"\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x04"),
    ],
)
def test_word_bytes(word_cls, expected_bytes):
    items = [0x1, 0x2, 0x3, 0x4]
    word = word_cls.from_items(items)

    assert bytes(word) == expected_bytes


@pytest.mark.parametrize("word_cls", [Word, GigaWord])
def test_word_int_conversion(word_cls):
    value = 0x12345678
    word = word_cls(value)

    assert int(word) == value


@pytest.mark.parametrize(
    ("word_cls", "value", "expected_repr"),
    [
        (Word, 0x12345678, "<Word 0x12345678>"),
        (Word, 0x123, "<Word 0x00000123>"),
        (GigaWord, 0, "<GigaWord 0x00000000000000000000000000000000>"),
        (GigaWord, 0x1234, "<GigaWord 0x00000000000000000000000000001234>"),
    ],
)
def test_word_repr(word_cls, value, expected_repr):
    assert repr(word_cls(value)) == expected_repr
