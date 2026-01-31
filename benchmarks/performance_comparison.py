import os
import sys
import timeit
import typing
from pathlib import Path

from gigarijndael.aes import AES128, AES192, AES256
from gigarijndael.rijndael import Rijndael


def benchmark_cipher(name: str, cipher: Rijndael, data: bytes, key: bytes, iterations: int = 10):
    timer_enc = timeit.Timer(lambda: cipher.encrypt(data, key))
    time_enc = timer_enc.timeit(number=iterations)

    data_size = len(data)
    print(
        f"| {name:<30} | {data_size:>10} | {iterations:<10} | {time_enc:>10.4f}s | {time_enc/iterations:>12.6f}s |"
    )


def main():
    data_sizes = [
        16,  # 1 block for AES
        256,
        1024,  # 1 KB
        1024 * 10,  # 10 KiB
        # 1024 * 1024,  # 1 MiB
    ]

    key_128 = os.urandom(16)
    key_192 = os.urandom(24)
    key_256 = os.urandom(32)

    print("-" * 90)
    print(
        f"| {'Cipher':<30} | {'Data Size':>10} | {'Iterations':<10} | {'Total Time':<10} | {'Time/Iter':<12} |"
    )
    print("-" * 90)

    for size in data_sizes:
        data = os.urandom(size)

        # AES standard
        benchmark_cipher("AES128", AES128(), data, key_128)
        benchmark_cipher("AES192", AES192(), data, key_192)
        benchmark_cipher("AES256", AES256(), data, key_256)

        # Rijndael with different block sizes
        benchmark_cipher("Rijndael (B:6, K:6)", Rijndael(block_size=6, key_size=6), data, key_192)
        benchmark_cipher("Rijndael (B:8, K:8)", Rijndael(block_size=8, key_size=8), data, key_256)

        # Experimental Giga mode
        benchmark_cipher(
            "GigaRijndael (B:4, K:4)",
            Rijndael(block_size=4, key_size=4, experimental=True),
            data,
            key_128,
        )
        benchmark_cipher(
            "GigaRijndael (B:8, K:8)",
            Rijndael(block_size=8, key_size=8, experimental=True),
            data,
            key_256,
        )
        benchmark_cipher(
            "GigaRijndael (B:8, K:4)",
            Rijndael(block_size=8, key_size=4, experimental=True),
            data,
            key_128,
        )
        print("-" * 90)


if __name__ == "__main__":
    main()
