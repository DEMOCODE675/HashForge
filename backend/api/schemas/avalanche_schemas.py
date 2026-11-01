"""Pydantic schemas for statistical avalanche Monte Carlo simulations."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class TrialRecordSchema(BaseModel):
    trial: int
    bit_index: int
    byte_index: int
    hamming_distance: int
    avalanche_pct: float
    original_hex: str
    modified_hex: str
    time_ms: float


class AvalancheSimulationRequest(BaseModel):
    text: str = Field(min_length=1, description="Baseline text string for all trials")
    trials: int = Field(default=50, ge=1, le=500, description="Number of Monte Carlo trials to run")
    algorithm: Optional[str] = Field(default="sha256", description="Algorithm ('sha256' or 'sha3_256')")
    seed: Optional[int] = Field(default=None, description="Optional RNG seed")
    mode: str = Field(default="single_bit", description="'single_bit' or 'cumulative'")
    comparative: bool = Field(default=False, description="Run both SHA-256 and SHA3-256 simultaneously")


class AvalancheSimulationResponse(BaseModel):
    original_text: str
    algorithm: str
    total_input_bits: int
    trials_count: int
    mean_avalanche_pct: float
    std_avalanche_pct: float
    min_avalanche_pct: float
    max_avalanche_pct: float
    median_avalanche_pct: float
    ideal_avalanche_pct: float = 50.0
    trials: List[TrialRecordSchema]


class ComparativeSimulationResponse(BaseModel):
    original_text: str
    trials_count: int
    sha256_result: AvalancheSimulationResponse
    sha3_256_result: AvalancheSimulationResponse

