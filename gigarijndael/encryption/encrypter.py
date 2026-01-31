import functools
import itertools
import typing

from more_itertools import grouper, padded

from gigarijndael.encryption.block import Block, State
from gigarijndael.encryption.matrix import left_shift, right_shift
from gigarijndael.encryption.sbox import GigaInvSBox, GigaSBox, InvSBox, SBox
from gigarijndael.encryption.word import GigaWord, Word
from gigarijndael.finite_fields.field import FiniteField


class RijndaelEncrypter:
    ROUNDS_NUMBER_REFERENCE_VALUE = 6  # Used to dynamically determine the number of rounds
    AVAILABLE_SIZES = {4, 6, 8}

    def __init__(self, block_size: int, key_size: int, experimental: bool = False):
        if block_size not in self.AVAILABLE_SIZES:
            raise ValueError(f"Invalid block size: {block_size}")
        if key_size not in self.AVAILABLE_SIZES:
            raise ValueError(f"Invalid key size: {key_size}")

        self.block_size: int = block_size
        self.key_size: int = key_size

        if not experimental:
            self.word_cls = Word
            self.finite_field: FiniteField = FiniteField(8)
            self.s_box = SBox()
            self.inv_s_box = InvSBox()
        else:
            self.word_cls = GigaWord
            self.s_box = GigaSBox()
            self.inv_s_box = GigaInvSBox()
            self.finite_field = self.s_box.finite_field

    @functools.cached_property
    def rounds_number(self) -> int:
        return max(self.key_size, self.block_size) + self.ROUNDS_NUMBER_REFERENCE_VALUE

    @functools.cached_property
    def round_constants(self) -> tuple[Word, ...]:
        """Generate round constants."""

        num_round_constants = (self.total_words - 1) // self.key_size

        def high_element_generator():
            round_constant = 1
            yield round_constant
            for _ in range(num_round_constants - 1):
                round_constant <<= 1
                if round_constant.bit_length() > self.word_cls.item_size_bits():
                    round_constant ^= self.finite_field.general_polynomial
                yield round_constant

        return tuple(self.word_cls.from_items([element]) for element in high_element_generator())

    @functools.cached_property
    def shift_row_sizes(self) -> tuple[int, ...]:
        second_row_shift = 2 if self.block_size < 8 else 3
        return 0, 1, second_row_shift, second_row_shift + 1

    @property
    def total_words(self) -> int:
        """Total number of words in the key schedule."""
        return self.block_size * (self.rounds_number + 1)

    def encrypt(
        self, blocks: typing.Iterable[Block], key: list[Word], decrypt: bool
    ) -> list[Block]:
        """
        Encrypt or decrypt multiple blocks.

        Args:
            blocks: Iterable of blocks to process.
            key: Expanded or original key words.
            decrypt: If True, perform decryption.

        Returns:
            List of processed blocks.
        """
        key_schedule = self._key_expansion(key[: self.key_size])
        return [self._block_encrypt(block, key_schedule, decrypt=decrypt) for block in blocks]

    def _block_encrypt(self, block: Block, key_schedule: list[Word], decrypt: bool) -> Block:
        """Process a single block."""
        state = self._init_state(block=block)
        init_key, round_keys = self._round_keys(key_schedule=key_schedule, decrypt=decrypt)
        round_func = self._inverse_round if decrypt else self._round

        state = self._add_round_key(state, init_key)
        for i in range(self.rounds_number - 1):
            state = round_func(state, round_keys[i])
        state = round_func(state, round_keys[self.rounds_number - 1], is_final=True)

        return tuple(itertools.chain.from_iterable(state))

    def _round(
        self, state: State, round_key: typing.Iterable[Word], is_final: bool = False
    ) -> State:
        """Standard Rijndael round."""
        state = self._sub_elements(state)
        state = self._shift_rows(state)
        if not is_final:
            state = self._mix_columns(state)
        state = self._add_round_key(state, round_key)
        return state

    def _inverse_round(
        self, state: State, round_key: typing.Iterable[Word], is_final: bool = False
    ) -> State:
        """Inverse Rijndael round."""
        state = self._inv_shift_rows(state)
        state = self._inv_sub_elements(state)
        state = self._add_round_key(state, round_key)
        if not is_final:
            state = self._inv_mix_columns(state)
        return state

    def _add_round_key(self, state: State, round_key: typing.Iterable[Word]) -> State:
        """XOR state with round key."""
        return [s ^ k for s, k in zip(state, round_key, strict=True)]

    def _sub_elements(self, state: State) -> State:
        """Apply S-Box to each element of each word in the state."""
        return [self.sub_word(word) for word in state]

    def _inv_sub_elements(self, state: State) -> State:
        """Apply inverse S-Box to each element of each word in the state."""
        return [
            self.word_cls.from_items(self.inv_s_box[element] for element in word) for word in state
        ]

    def _shift_rows(self, state: State) -> State:
        """Cyclic shift of rows in the state."""
        element_rows = []
        for i in range(self.word_cls.LENGTH):
            shift_size = self.shift_row_sizes[i]
            # Extract row (actually elements with same index across words)
            row = [state[j][i] for j in range(self.block_size)]
            element_rows.append(left_shift(row, shift_size))

        # Transpose back: Reconstruct words from shifted rows
        new_state = []
        for word_idx in range(self.block_size):
            word_items = [
                element_rows[row_idx][word_idx] for row_idx in range(self.word_cls.LENGTH)
            ]
            new_state.append(self.word_cls.from_items(word_items))
        return new_state

    def _inv_shift_rows(self, state: State) -> State:
        """Inverse cyclic shift of rows in the state."""
        element_rows = []
        for i in range(self.word_cls.LENGTH):
            shift_size = self.shift_row_sizes[i]
            row = [state[j][i] for j in range(self.block_size)]
            element_rows.append(right_shift(row, shift_size))

        new_state = []
        for word_idx in range(self.block_size):
            word_items = [
                element_rows[row_idx][word_idx] for row_idx in range(self.word_cls.LENGTH)
            ]
            new_state.append(self.word_cls.from_items(word_items))
        return new_state

    def _mix_columns(self, state: State) -> State:
        """Mix columns in the state."""
        column_polynomial = [0x02, 0x03, 0x01, 0x01]
        new_state = []
        for word in state:
            column_elements = [
                self.finite_field.add(
                    *(
                        self.finite_field.multiply(coef, element)
                        for coef, element in zip(right_shift(column_polynomial, i), word)
                    )
                )
                for i in range(len(word))
            ]
            new_state.append(self.word_cls.from_items(column_elements))
        return new_state

    def _inv_mix_columns(self, state: State) -> State:
        """Inverse mix columns in the state."""
        column_polynomial = [0x0E, 0x0B, 0x0D, 0x09]
        new_state = []
        for word in state:
            column_elements = [
                self.finite_field.add(
                    *(
                        self.finite_field.multiply(coef, element)
                        for coef, element in zip(right_shift(column_polynomial, i), word)
                    )
                )
                for i in range(len(word))
            ]
            new_state.append(self.word_cls.from_items(column_elements))
        return new_state

    def _round_keys(
        self, key_schedule: list[Word], decrypt: bool
    ) -> tuple[tuple[Word, ...], list[tuple[Word, ...]]]:
        """Split key schedule into round keys."""
        round_keys = list(itertools.batched(key_schedule, self.block_size))
        if decrypt:
            round_keys.reverse()
        return round_keys[0], round_keys[1:]

    def _init_state(self, block: Block) -> State:
        """Initialize state from block."""
        return [
            self.word_cls.from_items(word_items)
            for word_items in itertools.batched(block, self.word_cls.LENGTH)
        ]

    def sub_word(self, word: Word) -> Word:
        """Substitute word elements with S-Box values."""
        return self.word_cls.from_items(self.s_box[element] for element in word)

    def _key_expansion(self, key: list[Word]) -> list[Word]:
        """
        Expand the key into a key schedule.

        Args:
            key: Original key as a list of words.

        Returns:
            Key schedule as a list of words.
        """
        if len(key) != self.key_size:
            raise ValueError(f"Invalid key size: {len(key)}, expected: {self.key_size}")

        expanded_key = list(key)
        for i in range(self.key_size, self.total_words):
            expanded_key.append(self._round_key_expansion(index=i, key_expansion=expanded_key))
        return expanded_key

    def _round_key_expansion(self, *, index: int, key_expansion: list[Word]) -> Word:
        """Helper for key expansion."""
        key_length = self.key_size  # length in words
        temp_key = key_expansion[-1]
        if index % key_length == 0:
            rcon = self.round_constants[index // key_length - 1]
            temp_key = self.sub_word(temp_key << 1) ^ rcon
        elif key_length > 6 and index % key_length == 4:
            temp_key = self.sub_word(temp_key)
        return key_expansion[-key_length] ^ temp_key
