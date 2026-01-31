import typing

from gigarijndael.encryption.word import Word

Block: typing.TypeAlias = tuple[int, ...]
State: typing.TypeAlias = list[Word]
