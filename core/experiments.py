"""Experiment execution runners for single-bit, multi-bit, and statistical simulations."""

import math
import random
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence

from core.avalanche import AvalancheMetrics, compute_avalanche_metrics
from core.bit_operations import flip_bit, flip_multiple_bits, get_bit_at, text_to_bytes
from core.hash_engine import HashResult, compute_hash
from core.validators import validate_algorithm, validate_text_input, validate_trial_count


@dataclass(frozen=True)
class SingleBitTrialResult:
    """Detailed result of a single-bit perturbation experiment."""
    original_text: str
    original_bytes: bytes
    total_input_bits: int
    bit_index: int
    byte_index: int
    bit_offset_in_byte: int
    original_bit_value: int
    modified_bit_value: int
    modified_bytes: bytes
    algorithm: str
    original_hash: HashResult
    modified_hash: HashResult
    metrics: AvalancheMetrics


@dataclass(frozen=True)
class MultiBitTrialResult:
    """Detailed result of a multi-bit perturbation experiment."""
    original_text: str
    original_bytes: bytes
    total_input_bits: int
    flipped_bit_indices: List[int]
    flipped_bits_count: int
    modified_bytes: bytes
    algorithm: str
    original_hash: HashResult
    modified_hash: HashResult
    metrics: AvalancheMetrics


@dataclass(frozen=True)
class AvalancheSimulationResult:
    """Aggregate statistical results of an N-trial avalanche experiment."""
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
    trials: List[Dict[str, Any]] = None  # type: ignore


@dataclass(frozen=True)
class ComparativeSimulationResult:
    """Comparative simulation executing SHA-256 and SHA3-256 on identical perturbations."""
    original_text: str
    trials_count: int
    sha256_result: AvalancheSimulationResult
    sha3_256_result: AvalancheSimulationResult


def run_single_bit_trial(
    text: str,
    bit_index: int,
    algorithm: str = "sha256",
) -> SingleBitTrialResult:
    """Execute a single-bit flip trial and evaluate cryptographic avalanche effect.

    Args:
        text: Input string (must have at least 1 character).
        bit_index: Target bit index in Big-Endian order.
        algorithm: 'sha256' or 'sha3_256'.

    Returns:
        SingleBitTrialResult with complete before-and-after hashes and metrics.
    """
    valid_text = validate_text_input(text, allow_empty=False)
    algo = validate_algorithm(algorithm)

    raw_bytes = text_to_bytes(valid_text)
    total_bits = len(raw_bytes) * 8

    # Calculate bit address
    byte_idx = bit_index // 8
    bit_offset = 7 - (bit_index % 8)
    original_val = get_bit_at(raw_bytes, bit_index)
    modified_val = 1 - original_val

    # Perturb
    modified_bytes = flip_bit(raw_bytes, bit_index)

    # Hash both
    orig_hash = compute_hash(raw_bytes, algorithm=algo)
    mod_hash = compute_hash(modified_bytes, algorithm=algo)

    # Compute avalanche metrics
    metrics = compute_avalanche_metrics(orig_hash.binary_digest, mod_hash.binary_digest)

    return SingleBitTrialResult(
        original_text=valid_text,
        original_bytes=raw_bytes,
        total_input_bits=total_bits,
        bit_index=bit_index,
        byte_index=byte_idx,
        bit_offset_in_byte=bit_offset,
        original_bit_value=original_val,
        modified_bit_value=modified_val,
        modified_bytes=modified_bytes,
        algorithm=algo,
        original_hash=orig_hash,
        modified_hash=mod_hash,
        metrics=metrics,
    )


def run_multi_bit_trial(
    text: str,
    bit_indices: Sequence[int],
    algorithm: str = "sha256",
) -> MultiBitTrialResult:
    """Execute a multi-bit flip trial and evaluate cryptographic avalanche effect.

    Args:
        text: Input string (must have at least 1 character).
        bit_indices: Sequence of bit indices to flip.
        algorithm: 'sha256' or 'sha3_256'.

    Returns:
        MultiBitTrialResult containing hashes and metrics.
    """
    valid_text = validate_text_input(text, allow_empty=False)
    algo = validate_algorithm(algorithm)

    raw_bytes = text_to_bytes(valid_text)
    total_bits = len(raw_bytes) * 8

    modified_bytes = flip_multiple_bits(raw_bytes, bit_indices)

    orig_hash = compute_hash(raw_bytes, algorithm=algo)
    mod_hash = compute_hash(modified_bytes, algorithm=algo)

    metrics = compute_avalanche_metrics(orig_hash.binary_digest, mod_hash.binary_digest)

    return MultiBitTrialResult(
        original_text=valid_text,
        original_bytes=raw_bytes,
        total_input_bits=total_bits,
        flipped_bit_indices=sorted(list(bit_indices)),
        flipped_bits_count=len(bit_indices),
        modified_bytes=modified_bytes,
        algorithm=algo,
        original_hash=orig_hash,
        modified_hash=mod_hash,
        metrics=metrics,
    )


def run_avalanche_simulation(
    text: str,
    trials: int = 50,
    algorithm: str = "sha256",
    seed: Optional[int] = None,
    mode: str = "single_bit",
    specified_bits: Optional[List[int]] = None,
) -> AvalancheSimulationResult:
    """Run an automated statistical simulation of N trials.

    Methodology:
        Each single-bit trial starts strictly from the SAME original input text/bytes.
        One input bit is independently selected and flipped, then the modified hash is compared
        to the original hash.

    Args:
        text: Baseline input string.
        trials: Number of trials to execute (1 <= trials <= 1000).
        algorithm: 'sha256' or 'sha3_256'.
        seed: Optional RNG seed for deterministic reproduction.
        mode: 'single_bit' (independent single-bit trials) or 'cumulative' (cumulative random perturbation).
        specified_bits: Optional explicit sequence of bit indices to use for trials.

    Returns:
        AvalancheSimulationResult with summary statistics and per-trial details.
    """
    valid_text = validate_text_input(text, allow_empty=False)
    algo = validate_algorithm(algorithm)
    valid_trials = validate_trial_count(trials)

    raw_bytes = text_to_bytes(valid_text)
    total_input_bits = len(raw_bytes) * 8

    rng = random.Random(seed)

    orig_hash = compute_hash(raw_bytes, algorithm=algo)
    orig_bin = orig_hash.binary_digest

    trial_records: List[Dict[str, Any]] = []
    avalanche_percentages: List[float] = []

    cumulative_bytes = bytearray(raw_bytes)

    # Determine bit sequence
    if specified_bits is not None and len(specified_bits) >= valid_trials:
        chosen_bits = list(specified_bits[:valid_trials])
    else:
        # If trials <= total_input_bits, we can sample without replacement if possible,
        # otherwise sample with replacement across the whole bit address space
        if valid_trials <= total_input_bits:
            chosen_bits = rng.sample(range(total_input_bits), valid_trials)
        else:
            chosen_bits = [rng.randrange(0, total_input_bits) for _ in range(valid_trials)]

    for trial_idx in range(valid_trials):
        bit_idx = chosen_bits[trial_idx]

        if mode == "cumulative":
            # Flip bit cumulatively on the mutating array
            byte_i = bit_idx // 8
            bit_b = 7 - (bit_idx % 8)
            cumulative_bytes[byte_i] ^= (1 << bit_b)
            trial_modified_bytes = bytes(cumulative_bytes)
        else:
            # Independent single-bit trial from baseline
            trial_modified_bytes = flip_bit(raw_bytes, bit_idx)

        t_mod_hash = compute_hash(trial_modified_bytes, algorithm=algo)
        metrics = compute_avalanche_metrics(orig_bin, t_mod_hash.binary_digest)

        avalanche_percentages.append(metrics.avalanche_percentage)
        trial_records.append({
            "trial": trial_idx + 1,
            "bit_index": bit_idx,
            "byte_index": bit_idx // 8,
            "hamming_distance": metrics.hamming_distance,
            "avalanche_pct": round(metrics.avalanche_percentage, 4),
            "original_hex": orig_hash.hex_digest,
            "modified_hex": t_mod_hash.hex_digest,
            "time_ms": t_mod_hash.execution_time_ms,
        })

    # Statistical aggregations
    n = len(avalanche_percentages)
    mean_val = sum(avalanche_percentages) / n
    min_val = min(avalanche_percentages)
    max_val = max(avalanche_percentages)

    sorted_vals = sorted(avalanche_percentages)
    if n % 2 == 1:
        median_val = sorted_vals[n // 2]
    else:
        median_val = (sorted_vals[n // 2 - 1] + sorted_vals[n // 2]) / 2.0

    # Sample standard deviation
    if n > 1:
        variance = sum((x - mean_val) ** 2 for x in avalanche_percentages) / (n - 1)
        std_val = math.sqrt(variance)
    else:
        std_val = 0.0

    return AvalancheSimulationResult(
        original_text=valid_text,
        algorithm=algo,
        total_input_bits=total_input_bits,
        trials_count=valid_trials,
        mean_avalanche_pct=round(mean_val, 3),
        std_avalanche_pct=round(std_val, 3),
        min_avalanche_pct=round(min_val, 3),
        max_avalanche_pct=round(max_val, 3),
        median_avalanche_pct=round(median_val, 3),
        ideal_avalanche_pct=50.0,
        trials=trial_records,
    )


def run_comparative_simulation(
    text: str,
    trials: int = 50,
    seed: Optional[int] = None,
) -> ComparativeSimulationResult:
    """Run simultaneous SHA-256 and SHA3-256 simulations on the identical bit flips.

    Ensures mathematical fairness in algorithmic comparison.
    """
    valid_text = validate_text_input(text, allow_empty=False)
    valid_trials = validate_trial_count(trials)
    raw_bytes = text_to_bytes(valid_text)
    total_bits = len(raw_bytes) * 8

    rng = random.Random(seed)
    if valid_trials <= total_bits:
        chosen_bits = rng.sample(range(total_bits), valid_trials)
    else:
        chosen_bits = [rng.randrange(0, total_bits) for _ in range(valid_trials)]

    res_sha256 = run_avalanche_simulation(
        text=valid_text,
        trials=valid_trials,
        algorithm="sha256",
        seed=seed,
        specified_bits=chosen_bits,
    )

    res_sha3 = run_avalanche_simulation(
        text=valid_text,
        trials=valid_trials,
        algorithm="sha3_256",
        seed=seed,
        specified_bits=chosen_bits,
    )

    return ComparativeSimulationResult(
        original_text=valid_text,
        trials_count=valid_trials,
        sha256_result=res_sha256,
        sha3_256_result=res_sha3,
    )

