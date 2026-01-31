import pytest

from gigarijndael.aes import AES128, AES192, AES256


@pytest.fixture()
def sample_key_128() -> bytes:
    return b"1234567890123456"  # 16 bytes


@pytest.fixture()
def sample_key_192() -> bytes:
    return b"123456789012345678901234"  # 24 bytes


@pytest.fixture()
def sample_key_256() -> bytes:
    return b"12345678901234567890123456789012"  # 32 bytes


@pytest.mark.parametrize(
    "aes_cls, key_fixture",
    [(AES128, "sample_key_128"), (AES192, "sample_key_192"), (AES256, "sample_key_256")],
)
def test_aes_roundtrip(request, sample_data, aes_cls, key_fixture):
    key = request.getfixturevalue(key_fixture)
    cipher = aes_cls()

    encrypted = cipher.encrypt(sample_data, key)
    decrypted = cipher.decrypt(encrypted, key)

    assert decrypted == sample_data


@pytest.mark.parametrize(
    "aes_cls, expected_block_size, expected_key_size",
    [(AES128, 4, 4), (AES192, 4, 6), (AES256, 4, 8)],
)
def test_aes_default_params(aes_cls, expected_block_size, expected_key_size):
    aes = aes_cls()

    assert aes._encrypter.block_size == expected_block_size
    assert aes._encrypter.key_size == expected_key_size
