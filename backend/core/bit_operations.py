"""Bit-level operations, XOR perturbation, and binary formatting for HashForge.

Indexing Convention:
    HashForge standardizes on Big-Endian (Network Order) bit indexing:
    For an input byte array of length N (total bits = 8 * N):
    - Byte index:      i = bit_index // 8
    - Bit offset:      b = 7 - (bit_index % 8)
    - Bit mask:        1 << b

    - Bit 0 is the Most Significant Bit (MSB, 2^7 = 128) of byte 0.
    - Bit 7 is the Least Significant Bit (LSB, 2^0 = 1) of byte 0.
    - Bit 8 is the MSB of byte 1.
    - Bit (8*N - 1) is the LSB of the final byte (N - 1).

    Flipping a bit uses exact bitwise XOR: byte ^ (1 << b).
"""

from typing import Sequence, List
from core.validators import validate_bit_index, validate_bit_indices, ValidationError

BIT_INDEXING_EXPLANATION = (
    "Big-Endian / Network Bit Indexing: For any input byte array, bit 0 represents "
    "the Most Significant Bit (MSB, 2^7) of Byte 0, bit 7 is the Least Significant Bit "
    "(LSB, 2^0) of Byte 0, and bit 8 begins Byte 1. Bit flipping is performed via exact "
    "XOR inversion (byte ^ (1 << (7 - (k % 8))))."
)


def text_to_bytes(text: str, encoding: str = "utf-8") -> bytes:
    """Convert input string to bytes using specified encoding.

    Args:
        text: Input string.
        encoding: Character encoding (default 'utf-8').

    Returns:
        Encoded bytes.
    """
    return text.encode(encoding)


def bytes_to_bits(data: bytes) -> str:
    """Convert bytes to a continuous string of '0' and '1' characters."""
    return "".join(f"{b:08b}" for b in data)


def get_bit_at(data: bytes, bit_index: int) -> int:
    """Retrieve the bit value (0 or 1) at a given bit index.

    Args:
        data: Target byte sequence.
        bit_index: Zero-based bit position in Big-Endian order.

    Returns:
        0 or 1.
    """
    total_bits = len(data) * 8
    validate_bit_index(bit_index, total_bits)

    byte_idx = bit_index // 8
    bit_offset = 7 - (bit_index % 8)
    target_byte = data[byte_idx]

    return (target_byte >> bit_offset) & 1


def flip_bit(data: bytes, bit_index: int) -> bytes:
    """Flip exactly one bit in a byte array using XOR inversion.

    Args:
        data: Input bytes (must not be empty).
        bit_index: Zero-based index of bit to flip (0 <= bit_index < 8 * len(data)).

    Returns:
        A new immutable bytes object with the single bit inverted.

    Raises:
        ValidationError: If bit_index is out of range or data is empty.
    """
    total_bits = len(data) * 8
    validate_bit_index(bit_index, total_bits)

    byte_idx = bit_index // 8
    bit_offset = 7 - (bit_index % 8)
    mask = 1 << bit_offset

    byte_array = bytearray(data)
    byte_array[byte_idx] ^= mask

    return bytes(byte_array)


def flip_multiple_bits(data: bytes, bit_indices: Sequence[int]) -> bytes:
    """Flip multiple distinct bits in a byte array using XOR inversion.

    Args:
        data: Input bytes.
        bit_indices: Sequence of unique zero-based bit indices.

    Returns:
        A new immutable bytes object with all specified bits inverted.

    Raises:
        ValidationError: If indices are invalid, out of range, or duplicate.
    """
    total_bits = len(data) * 8
    validated_indices = validate_bit_indices(bit_indices, total_bits)

    byte_array = bytearray(data)
    for bit_index in validated_indices:
        byte_idx = bit_index // 8
        bit_offset = 7 - (bit_index % 8)
        mask = 1 << bit_offset
        byte_array[byte_idx] ^= mask

    return bytes(byte_array)


def format_binary_grouped(bit_string: str, group_size: int = 8, line_size: int = 64) -> List[str]:
    """Group a binary bit string into byte-sized blocks and multi-byte lines for readable display.

    Args:
        bit_string: Sequence of '0' and '1'.
        group_size: Bits per block (default 8 bits = 1 byte).
        line_size: Bits per display line (default 64 bits = 8 bytes).

    Returns:
        List of formatted string lines.
    """
    if not bit_string:
        return []

    lines = []
    for line_start in range(0, len(bit_string), line_size):
        chunk = bit_string[line_start : line_start + line_size]
        groups = [chunk[i : i + group_size] for i in range(0, len(chunk), group_size)]
        lines.append(" ".join(groups))

    return lines

