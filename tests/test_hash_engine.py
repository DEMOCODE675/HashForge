"""Unit tests for HashForge Cryptographic Engine and standard test vectors."""

import pytest
from core.hash_engine import (
    compute_hash,
    bytes_to_binary_string,
    hex_to_binary_string,
    HashResult,
)
from core.validators import ValidationError


class TestHashEngineKnownVectors:
    """NIST standard test vector verifications for SHA-256 and SHA3-256."""

    def test_sha256_empty_string(self):
        result = compute_hash("", algorithm="sha256")
        expected = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        assert result.hex_digest == expected
        assert result.digest_bits == 256
        assert result.digest_bytes == 32
        assert len(result.hex_digest) == 64
        assert len(result.binary_digest) == 256

    def test_sha256_abc(self):
        result = compute_hash("abc", algorithm="sha256")
        expected = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
        assert result.hex_digest == expected
        assert result.input_length_bytes == 3

    def test_sha256_quick_brown_fox(self):
        msg = "The quick brown fox jumps over the lazy dog"
        result = compute_hash(msg, algorithm="sha256")
        expected = "d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592"
        assert result.hex_digest == expected

    def test_sha3_256_empty_string(self):
        result = compute_hash("", algorithm="sha3_256")
        expected = "a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a"
        assert result.hex_digest == expected
        assert result.digest_bits == 256
        assert result.digest_bytes == 32
        assert len(result.hex_digest) == 64
        assert len(result.binary_digest) == 256

    def test_sha3_256_abc(self):
        result = compute_hash("abc", algorithm="sha3_256")
        expected = "3a985da74fe225b2045c172d6bd390bd855f086e3e9d525b46bfe24511431532"
        assert result.hex_digest == expected
        assert result.input_length_bytes == 3

    def test_sha3_256_quick_brown_fox(self):
        msg = "The quick brown fox jumps over the lazy dog"
        result = compute_hash(msg, algorithm="sha3_256")
        expected = "69070dda01975c8c120c3aada1b282394e7f032fa9cf32f4cb2259a0897dfc04"
        assert result.hex_digest == expected


class TestHashEngineBehaviors:
    """Testing edge cases, unicode, raw bytes, and errors."""

    def test_unicode_input(self):
        msg = "Cryptography 🔐 & HashForge"
        res_sha256 = compute_hash(msg, "sha256")
        res_sha3 = compute_hash(msg, "sha3_256")
        assert len(res_sha256.hex_digest) == 64
        assert len(res_sha3.hex_digest) == 64
        assert res_sha256.input_length_bytes == len(msg.encode("utf-8"))

    def test_raw_bytes_input(self):
        raw = b"\x00\xff\x7f\x80"
        res = compute_hash(raw, "sha256")
        assert res.input_length_bytes == 4
        assert res.input_bytes == raw

    def test_unsupported_algorithm_raises(self):
        with pytest.raises(ValidationError):
            compute_hash("hello", algorithm="md5")

        with pytest.raises(ValidationError):
            compute_hash("hello", algorithm="sha1")

    def test_invalid_type_raises(self):
        with pytest.raises(TypeError):
            compute_hash(12345, algorithm="sha256")  # type: ignore

    def test_execution_time_is_positive(self):
        res = compute_hash("benchmark test", "sha256")
        assert isinstance(res.execution_time_ms, float)
        assert res.execution_time_ms >= 0.0

    def test_binary_and_hex_conversions(self):
        raw = b"\x0f\xf0"
        bin_str = bytes_to_binary_string(raw)
        assert bin_str == "0000111111110000"

        hex_str = "0ff0"
        bin_from_hex = hex_to_binary_string(hex_str)
        assert bin_from_hex == "0000111111110000"
