"""File integrity verification and chunk-based streaming hashing."""

import hashlib
import time
from dataclasses import dataclass
from typing import BinaryIO, Dict, Optional, Tuple, Union


@dataclass(frozen=True)
class FileIntegrityReport:
    """Fingerprint report for a single file."""
    file_name: str
    file_size_bytes: int
    formatted_size: str
    sha256_hex: str
    sha3_256_hex: str
    chunks_processed: int
    hashing_duration_ms: float


@dataclass(frozen=True)
class FileComparisonReport:
    """Comparison report between two files or a file and a reference hash."""
    file_a: FileIntegrityReport
    file_b: Optional[FileIntegrityReport]
    reference_hash: Optional[str]
    is_identical: bool
    sha256_match: bool
    sha3_256_match: bool
    size_match: bool
    details: str


def format_file_size(size_bytes: int) -> str:
    """Format byte count into human-readable unit (B, KB, MB, GB).

    Args:
        size_bytes: Non-negative integer size in bytes.

    Returns:
        Formatted string (e.g., '12.45 KB').
    """
    if size_bytes < 0:
        return "0 B"
    if size_bytes == 0:
        return "0 B"

    units = ["B", "KB", "MB", "GB", "TB"]
    unit_index = 0
    size = float(size_bytes)

    while size >= 1024.0 and unit_index < len(units) - 1:
        size /= 1024.0
        unit_index += 1

    if unit_index == 0:
        return f"{int(size)} {units[unit_index]}"
    return f"{size:.2f} {units[unit_index]}"


def hash_file_stream(
    file_obj: BinaryIO,
    file_name: str = "uploaded_file",
    chunk_size: int = 65536,
) -> FileIntegrityReport:
    """Compute SHA-256 and SHA3-256 fingerprints in a single streaming pass.

    Reads data in chunks to prevent excessive memory consumption.

    Args:
        file_obj: Readable binary stream (io.BytesIO or file-like object).
        file_name: Human-readable file name.
        chunk_size: Read buffer size in bytes (default 64KB).

    Returns:
        FileIntegrityReport with both digests and metadata.
    """
    hasher_sha256 = hashlib.sha256()
    hasher_sha3 = hashlib.sha3_256()

    total_bytes = 0
    chunk_count = 0

    # Ensure stream position is at start if seekable
    if hasattr(file_obj, "seek"):
        try:
            file_obj.seek(0)
        except Exception:
            pass

    t0 = time.perf_counter_ns()
    while True:
        chunk = file_obj.read(chunk_size)
        if not chunk:
            break
        total_bytes += len(chunk)
        chunk_count += 1
        hasher_sha256.update(chunk)
        hasher_sha3.update(chunk)

    t1 = time.perf_counter_ns()
    duration_ms = (t1 - t0) / 1_000_000.0

    # Reset stream pointer for any downstream consumer
    if hasattr(file_obj, "seek"):
        try:
            file_obj.seek(0)
        except Exception:
            pass

    return FileIntegrityReport(
        file_name=file_name,
        file_size_bytes=total_bytes,
        formatted_size=format_file_size(total_bytes),
        sha256_hex=hasher_sha256.hexdigest(),
        sha3_256_hex=hasher_sha3.hexdigest(),
        chunks_processed=chunk_count,
        hashing_duration_ms=duration_ms,
    )


def compare_file_hashes(
    report_a: FileIntegrityReport,
    report_b: Optional[FileIntegrityReport] = None,
    reference_hash: Optional[str] = None,
) -> FileComparisonReport:
    """Compare a file report against a second file report or a reference hash string.

    Args:
        report_a: Integrity report of the primary file.
        report_b: Optional integrity report of the second file.
        reference_hash: Optional reference hash string provided by a trusted distributor.

    Returns:
        FileComparisonReport with match status and analytical details.
    """
    if report_b is not None:
        sha256_match = report_a.sha256_hex.lower() == report_b.sha256_hex.lower()
        sha3_match = report_a.sha3_256_hex.lower() == report_b.sha3_256_hex.lower()
        size_match = report_a.file_size_bytes == report_b.file_size_bytes
        is_identical = sha256_match and sha3_match and size_match

        if is_identical:
            details = (
                f"Files '{report_a.file_name}' and '{report_b.file_name}' have identical "
                "cryptographic fingerprints across SHA-256 and SHA3-256. Their content is bit-for-bit identical."
            )
        else:
            details = (
                f"Files '{report_a.file_name}' and '{report_b.file_name}' differ in cryptographic fingerprints. "
                "The files have different content or have been modified."
            )

        return FileComparisonReport(
            file_a=report_a,
            file_b=report_b,
            reference_hash=None,
            is_identical=is_identical,
            sha256_match=sha256_match,
            sha3_256_match=sha3_match,
            size_match=size_match,
            details=details,
        )

    elif reference_hash is not None:
        ref_clean = reference_hash.strip().lower()
        sha256_match = report_a.sha256_hex.lower() == ref_clean
        sha3_match = report_a.sha3_256_hex.lower() == ref_clean
        is_identical = sha256_match or sha3_match

        if is_identical:
            matched_algo = "SHA-256" if sha256_match else "SHA3-256"
            details = (
                f"File '{report_a.file_name}' perfectly matches the provided reference hash via {matched_algo}. "
                "File integrity verified."
            )
        else:
            details = (
                f"File '{report_a.file_name}' DOES NOT match the provided reference hash. "
                "The file may be corrupted, truncated, or tampered with."
            )

        return FileComparisonReport(
            file_a=report_a,
            file_b=None,
            reference_hash=ref_clean,
            is_identical=is_identical,
            sha256_match=sha256_match,
            sha3_256_match=sha3_match,
            size_match=True,
            details=details,
        )
    else:
        return FileComparisonReport(
            file_a=report_a,
            file_b=None,
            reference_hash=None,
            is_identical=True,
            sha256_match=True,
            sha3_256_match=True,
            size_match=True,
            details="Single file report generated.",
        )

