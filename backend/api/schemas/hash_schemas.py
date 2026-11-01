"""Pydantic schemas for hash generation and comparison."""

from typing import Optional
from pydantic import BaseModel, Field


class HashRequest(BaseModel):
    text: str = Field(default="", description="Input text to hash (UTF-8 encoded)")
    algorithm: str = Field(default="sha256", description="Algorithm name ('sha256' or 'sha3_256')")


class HashResponse(BaseModel):
    algorithm: str
    hex_digest: str
    binary_digest: str
    digest_bits: int
    digest_bytes: int
    input_length_bytes: int
    execution_time_ms: float
    formatted_hex: str


class AlgorithmCompareRequest(BaseModel):
    text: str = Field(default="", description="Input text to compare across SHA-256 and SHA3-256")
    benchmark_iterations: Optional[int] = Field(default=1000, ge=10, le=10000, description="Benchmark loop count")


class AlgorithmBenchmarkInfo(BaseModel):
    iterations: int
    total_time_ms: float
    average_latency_us: float


class AlgorithmCompareResponse(BaseModel):
    original_text: str
    input_bytes_count: int
    input_bits_count: int
    sha256: HashResponse
    sha3_256: HashResponse
    cross_hamming_distance: int
    cross_divergence_percentage: float
    sha256_benchmark: Optional[AlgorithmBenchmarkInfo] = None
    sha3_benchmark: Optional[AlgorithmBenchmarkInfo] = None

