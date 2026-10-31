"""Unit tests for Bit Operations and XOR Perturbation Engine."""

import pytest
from core.bit_operations import (
    text_to_bytes,
    bytes_to_bits,
    get_bit_at,
    flip_bit,
    flip_multiple_bits,
    format_binary_grouped,
)
from core.validators import ValidationError


class TestBitOperations:
    """Verifications for bit retrieval, XOR manipulation, and network endianness."""

    def test_text_to_bytes_and_bits(self):
        b = text_to_bytes("A")
        assert b == b"\x41"  # ASCII 65 = 0b01000001
        bits = bytes_to_bits(b)
        assert bits == "01000001"

    def test_get_bit_at_big_endian(self):
        # 'A' = 0x41 = 0b01000001
        data = b"\x41"
        assert get_bit_at(data, 0) == 0  # MSB
        assert get_bit_at(data, 1) == 1
        assert get_bit_at(data, 2) == 0
        assert get_bit_at(data, 3) == 0
        assert get_bit_at(data, 4) == 0
        assert get_bit_at(data, 5) == 0
        assert get_bit_at(data, 6) == 0
        assert get_bit_at(data, 7) == 1  # LSB

    def test_flip_first_valid_bit(self):
        # 'A' = 0b01000001 (65)
        # Inverting bit 0 (MSB: mask 0x80 = 128) -> 65 + 128 = 193 = 0b11000001
        data = b"\x41"
        flipped = flip_bit(data, 0)
        assert flipped == bytes([0b11000001])
        assert get_bit_at(flipped, 0) == 1

    def test_flip_last_valid_bit(self):
        # Two bytes: "AB" = [0x41, 0x42]
        # Total bits = 16. Last bit index is 15 (LSB of byte 1).
        # 'B' = 0x42 = 0b01000010
        # Inverting bit 15 (LSB of byte 1: mask 0x01) -> 0b01000011 = 'C' (0x43)
        data = b"\x41\x42"
        flipped = flip_bit(data, 15)
        assert flipped == b"\x41\x43"
        assert get_bit_at(flipped, 15) == 1

    def test_flip_middle_bit(self):
        # 'A' = 0b01000001. Flip bit 1 (mask 0x40 = 64) -> 0b00000001
        data = b"\x41"
        flipped = flip_bit(data, 1)
        assert flipped == bytes([0b00000001])

    def test_original_data_immutability(self):
        original = b"\x41"
        flipped = flip_bit(original, 0)
        assert original == b"\x41"
        assert flipped != original

    def test_flip_empty_bytes_raises(self):
        with pytest.raises(ValidationError):
            flip_bit(b"", 0)

    def test_negative_bit_index_raises(self):
        with pytest.raises(ValidationError):
            flip_bit(b"\x41", -1)

    def test_out_of_range_bit_index_raises(self):
        data = b"\x41"  # 8 bits (indices 0 to 7)
        with pytest.raises(ValidationError):
            flip_bit(data, 8)

        with pytest.raises(ValidationError):
            flip_bit(data, 100)

    def test_flip_multiple_bits(self):
        data = b"\x00"  # 0b00000000
        # Flip bits 0 (MSB) and 7 (LSB) -> 0b10000001 = 0x81
        flipped = flip_multiple_bits(data, [0, 7])
        assert flipped == bytes([0x81])

    def test_flip_multiple_duplicate_raises(self):
        with pytest.raises(ValidationError):
            flip_multiple_bits(b"\x00", [1, 1])

    def test_flip_multiple_empty_indices_raises(self):
        with pytest.raises(ValidationError):
            flip_multiple_bits(b"\x00", [])

    def test_format_binary_grouped(self):
        bit_string = "0100000101000010"  # 16 bits
        grouped = format_binary_grouped(bit_string, group_size=8, line_size=16)
        assert len(grouped) == 1
        assert grouped[0] == "01000001 01000010"

        empty_grouped = format_binary_grouped("")
        assert empty_grouped == []

