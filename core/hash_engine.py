"""Cryptographic Hashing Engine supporting SHA-256 and SHA3-256."""

import hashlib
import time
from dataclasses import dataclass
from typing import Union

from core.validators import validate_algorithm


@dataclass(frozen=True)
class HashResult:
    """Immutable result container for a cryptographic hash computation."""
    algorithm: str
    input_bytes: bytes
    input_length_bytes: int
    hex_digest: str
    binary_digest: str
    digest_bits: int
    digest_bytes: int
    execution_time_ms: float

    @property
    def formatted_hex(self) -> str:
        """Return formatted hex digest with spacing every 8 chars for legibility."""
        return " ".join(self.hex_digest[i : i + 8] for i in range(0, len(self.hex_digest), 8))


def bytes_to_binary_string(data: bytes) -> str:
    """Convert raw bytes to an unspaced binary bit string ('0' and '1').

    Each byte is converted to an 8-bit representation with leading zeros preserved (big-endian).

    Args:
        data: Raw byte string.

    Returns:
        String of 0s and 1s representing all bits.
    """
    return "".join(f"{b:08b}" for b in data)


def hex_to_binary_string(hex_str: str) -> str:
    """Convert a hexadecimal digest string to a 256-bit binary string.

    Args:
        hex_str: Hexadecimal string (e.g. 64 chars for 256 bits).

    Returns:
        Binary representation with exactly 4 bits per hex character.
    """
    clean_hex = hex_str.strip().lower()
    return "".join(f"{int(c, 16):04b}" for c in clean_hex)


def compute_hash(data: Union[str, bytes], algorithm: str = "sha256") -> HashResult:
    """Compute the cryptographic hash of input data using hashlib.

    Args:
        data: Input string or raw bytes. If string, it is encoded to UTF-8 bytes.
        algorithm: 'sha256' or 'sha3_256'.

    Returns:
        HashResult dataclass populated with digest, binary representation, and timing.

    Raises:
        ValidationError: If algorithm is not recognized.
    """
    algo = validate_algorithm(algorithm)

    if isinstance(data, str):
        byte_data = data.encode("utf-8")
    elif isinstance(data, (bytes, bytearray)):
        byte_data = bytes(data)
    else:
        raise TypeError(f"Data must be str or bytes, got {type(data).__name__}.")

    # High-precision timer
    t0 = time.perf_counter_ns()

    if algo == "sha256":
        hasher = hashlib.sha256(byte_data)
        digest_bytes_len = 32
    elif algo == "sha3_256":
        hasher = hashlib.sha3_256(byte_data)
        digest_bytes_len = 32
    else:
        raise ValueError(f"Unhandled algorithm: {algo}")

    raw_digest = hasher.digest()
    t1 = time.perf_counter_ns()

    hex_digest = raw_digest.hex()
    bin_digest = bytes_to_binary_string(raw_digest)
    execution_time_ms = (t1 - t0) / 1_000_000.0

    return HashResult(
        algorithm=algo,
        input_bytes=byte_data,
        input_length_bytes=len(byte_data),
        hex_digest=hex_digest,
        binary_digest=bin_digest,
        digest_bits=digest_bytes_len * 8,
        digest_bytes=digest_bytes_len,
        execution_time_ms=execution_time_ms,
    )

