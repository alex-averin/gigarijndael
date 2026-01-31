import pytest

from gigarijndael.rijndael import Rijndael


@pytest.mark.parametrize("experimental", [True, False])
@pytest.mark.parametrize("block_size", [4, 6, 8])
@pytest.mark.parametrize("key_size", [4, 6, 8])
def test_rijndael_encrypt(sample_data, experimental, block_size, key_size):
    key = b"secret-key"
    rijndael = Rijndael(block_size=block_size, key_size=key_size, experimental=experimental)

    cipher_text = rijndael.encrypt(data=sample_data, key=key)
    plain_text = rijndael.decrypt(data=cipher_text, key=key)

    assert plain_text == sample_data


@pytest.mark.parametrize("experimental", [True, False])
@pytest.mark.parametrize("block_size", [4, 6, 8])
@pytest.mark.parametrize("key_size", [4, 6, 8])
def test_rijndael_decrypt(sample_data, experimental, block_size, key_size):
    key = b"secret-key"
    rijndael = Rijndael(block_size=block_size, key_size=key_size, experimental=experimental)

    plain_text = rijndael.decrypt(data=sample_data, key=key)
    cipher_text = rijndael.encrypt(data=plain_text, key=key)

    assert cipher_text == sample_data
