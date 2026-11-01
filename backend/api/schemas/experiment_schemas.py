"""Pydantic schemas for single-bit and multi-bit perturbation experiments."""

from typing import List, Optional
from pydantic import BaseModel, Field
from backend.api.schemas.hash_schemas import HashResponse


class AvalancheMetricsSchema(BaseModel):
    hamming_distance: int
    total_bits: int
    avalanche_percentage: float
    changed_indices: List[int]
    unchanged_count: int
    distance_from_ideal: float


class SingleBitRequest(BaseModel):
    text: str = Field(min_length=1, description="Input string (minimum 1 char)")
    bit_index: int = Field(ge=0, description="Target bit index to invert (0 is MSB of Byte 0)")
    algorithm: str = Field(default="sha256", description="Algorithm name ('sha256' or 'sha3_256')")


class SingleBitResponse(BaseModel):
    original_text: str
    total_input_bits: int
    bit_index: int
    byte_index: int
    bit_offset_in_byte: int
    original_bit_value: int
    modified_bit_value: int
    original_bytes_hex: str
    modified_bytes_hex: str
    original_binary_input: str
    modified_binary_input: str
    algorithm: str
    original_hash: HashResponse
    modified_hash: HashResponse
    metrics: AvalancheMetricsSchema
    diff_mask: List[bool]


class MultiBitRequest(BaseModel):
    text: str = Field(min_length=1, description="Input string")
    bit_indices: List[int] = Field(min_length=1, description="List of unique bit indices to flip")
    algorithm: str = Field(default="sha256", description="Algorithm name ('sha256' or 'sha3_256')")


class MultiBitRandomRequest(BaseModel):
    text: str = Field(min_length=1, description="Input string")
    k_bits: int = Field(ge=1, description="Number of unique bits to randomly invert")
    seed: Optional[int] = Field(default=None, description="Optional RNG seed for deterministic reproduction")
    algorithm: str = Field(default="sha256", description="Algorithm name ('sha256' or 'sha3_256')")


class MultiBitResponse(BaseModel):
    original_text: str
    total_input_bits: int
    flipped_bit_indices: List[int]
    flipped_bits_count: int
    original_bytes_hex: str
    modified_bytes_hex: str
    algorithm: str
    original_hash: HashResponse
    modified_hash: HashResponse
    metrics: AvalancheMetricsSchema
    diff_mask: List[bool]

