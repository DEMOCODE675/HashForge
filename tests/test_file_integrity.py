"""Unit tests for File Integrity and Streaming Hashing."""

import io
import pytest
from core.file_integrity import (
    hash_file_stream,
    compare_file_hashes,
    format_file_size,
)


class TestFileIntegrity:
    """Verifications for chunked streaming hashing and tamper detection."""

    def test_format_file_size(self):
        assert format_file_size(0) == "0 B"
        assert format_file_size(500) == "500 B"
        assert format_file_size(1024) == "1.00 KB"
        assert format_file_size(1024 * 1024) == "1.00 MB"
        assert format_file_size(1024 * 1024 * 1024) == "1.00 GB"

    def test_empty_file_stream(self):
        empty_stream = io.BytesIO(b"")
        report = hash_file_stream(empty_stream, file_name="empty.txt")
        assert report.file_size_bytes == 0
        assert report.formatted_size == "0 B"
        assert report.chunks_processed == 0
        # Check standard empty hash digests
        assert report.sha256_hex == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        assert report.sha3_256_hex == "a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a"

    def test_identical_files_comparison(self):
        data = b"HashForge secure verification test payload"
        stream_a = io.BytesIO(data)
        stream_b = io.BytesIO(data)

        report_a = hash_file_stream(stream_a, file_name="file_a.bin")
        report_b = hash_file_stream(stream_b, file_name="file_b.bin")

        comparison = compare_file_hashes(report_a, report_b)
        assert comparison.is_identical is True
        assert comparison.sha256_match is True
        assert comparison.sha3_256_match is True
        assert comparison.size_match is True

    def test_different_files_comparison(self):
        stream_a = io.BytesIO(b"Authentic Firmware v1.0.0")
        stream_b = io.BytesIO(b"Tampered Firmware v1.0.0")

        report_a = hash_file_stream(stream_a, file_name="fw_original.bin")
        report_b = hash_file_stream(stream_b, file_name="fw_modified.bin")

        comparison = compare_file_hashes(report_a, report_b)
        assert comparison.is_identical is False
        assert comparison.sha256_match is False
        assert comparison.sha3_256_match is False

    def test_chunking_with_small_buffer(self):
        # 100 KB payload processed with 16 KB chunks -> 7 chunks
        payload = b"X" * (100 * 1024)
        stream = io.BytesIO(payload)
        report = hash_file_stream(stream, file_name="large_payload.bin", chunk_size=16384)
        assert report.file_size_bytes == 100 * 1024
        assert report.chunks_processed == 7
        assert len(report.sha256_hex) == 64
        assert len(report.sha3_256_hex) == 64

    def test_reference_hash_matching(self):
        stream = io.BytesIO(b"HashForge Reference Test")
        report = hash_file_stream(stream, file_name="doc.pdf")

        # Correct match
        comp_ok = compare_file_hashes(report, reference_hash=report.sha256_hex)
        assert comp_ok.is_identical is True
        assert comp_ok.sha256_match is True

        # Tampered / incorrect reference hash
        tampered_ref = "0000000000000000000000000000000000000000000000000000000000000000"
        comp_fail = compare_file_hashes(report, reference_hash=tampered_ref)
        assert comp_fail.is_identical is False
        assert comp_fail.sha256_match is False

