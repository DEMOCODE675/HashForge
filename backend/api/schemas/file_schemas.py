"""Pydantic schemas for file integrity and fingerprinting endpoints."""

from typing import Optional
from pydantic import BaseModel


class FileHashResponse(BaseModel):
    file_name: str
    file_size_bytes: int
    formatted_size: str
    sha256_hex: str
    sha3_256_hex: str
    chunks_processed: int
    hashing_duration_ms: float


class FileCompareResponse(BaseModel):
    file_a: FileHashResponse
    file_b: Optional[FileHashResponse] = None
    reference_hash: Optional[str] = None
    is_identical: bool
    sha256_match: bool
    sha3_256_match: bool
    size_match: bool
    details: str

