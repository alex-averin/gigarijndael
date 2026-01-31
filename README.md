# GigaRijndael
**GigaRijndael** is an experimental research project that explores extensions of the Rijndael (AES) algorithm using Galois fields **GF(2³²)**.

## Features
- Implementation of the Rijndael algorithm with variable block and key sizes (128, 192, 256 bits).
- AES-128, AES-192, AES-256 predefined classes.
- Support for GF(2³), GF(2⁴), GF(2⁵), GF(2⁷), GF(2), GF(2⁸), GF(2³²).
- Support for non-standard block and key parameters based on extended arithmetic in GF(2³²).

## Installation
```bash
pip install git+https://github.com/alex-averin/gigarijndael.git
```

## Usage

### Simple AES Encryption
```python
from gigarijndael import AES128

cipher = AES128()
key = b"very-secret-key!" # 16 bytes for AES-128
data = b"Hello, World!"

encrypted = cipher.encrypt(data, key)
decrypted = cipher.decrypt(encrypted, key)

print(decrypted) # b'Hello, World!'
```

### Flexible Rijndael
```python
from gigarijndael import Rijndael

# Block size 256 bits (8 words), Key size 192 bits (6 words)
cipher = Rijndael(block_size=8, key_size=6)
key = b"another-secret-key-123456"
data = b"Extended Rijndael testing"

encrypted = cipher.encrypt(data, key)
decrypted = cipher.decrypt(encrypted, key)
```

### Experimental "Giga" Mode (GF(2³²))
This mode extends each element from 8 bits to 32 bits, using a larger Galois field for research purposes.
```python
from gigarijndael import Rijndael

# Use experimental=True to enable Giga mode
cipher = Rijndael(block_size=4, key_size=4, experimental=True)
key = b"very-long-secret-key"
data = b"Research data for GF(2^32)"

encrypted = cipher.encrypt(data, key)
decrypted = cipher.decrypt(encrypted, key)
```
