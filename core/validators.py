"""Validation utilities for HashForge input parameters and constraints."""

from typing import Iterable, Sequence


class ValidationError(ValueError):
    """Raised when an input or parameter fails cryptographic/operational validation."""
    pass


SUPPORTED_ALGORITHMS = ("sha256", "sha3_256")


def validate_algorithm(algorithm: str) -> str:
    """Validate that the requested hashing algorithm is supported.

    Args:
        algorithm: String name of algorithm (e.g., 'sha256', 'sha3_256').

    Returns:
        Normalized lower-case algorithm name.

    Raises:
        ValidationError: If algorithm is not supported.
    """
    if not isinstance(algorithm, str):
        raise ValidationError(f"Algorithm name must be a string, got {type(algorithm).__name__}.")

    algo_norm = algorithm.strip().lower()
    if algo_norm not in SUPPORTED_ALGORITHMS:
        raise ValidationError(
            f"Unsupported algorithm '{algorithm}'. Supported algorithms: {', '.join(SUPPORTED_ALGORITHMS)}."
        )
    return algo_norm


def validate_text_input(text: str, allow_empty: bool = True, max_length: int = 100_000) -> str:
    """Validate string input for hashing or bit experimentation.

    Args:
        text: Input string.
        allow_empty: Whether empty string is permitted (standard hashing permits empty).
        max_length: Maximum allowed character length to avoid memory denial.

    Returns:
        The validated text.

    Raises:
        ValidationError: If text violates constraints.
    """
    if not isinstance(text, str):
        raise ValidationError(f"Input must be a string, got {type(text).__name__}.")

    if not allow_empty and len(text) == 0:
        raise ValidationError("Input text cannot be empty for bit-flipping experiments.")

    if len(text) > max_length:
        raise ValidationError(
            f"Input text length ({len(text):,} chars) exceeds maximum allowable limit of {max_length:,} characters."
        )

    return text


def validate_bit_index(bit_index: int, total_bits: int) -> int:
    """Validate that a single bit index is an integer within valid range [0, total_bits - 1].

    Args:
        bit_index: Zero-based bit position.
        total_bits: Total number of bits in the target byte array.

    Returns:
        The validated integer bit index.

    Raises:
        ValidationError: If index is non-integer, negative, or out of bounds.
    """
    if not isinstance(bit_index, int) or isinstance(bit_index, bool):
        raise ValidationError(f"Bit index must be an integer, got {type(bit_index).__name__}.")

    if total_bits <= 0:
        raise ValidationError("Cannot index bits in an empty byte array (total_bits <= 0).")

    if bit_index < 0 or bit_index >= total_bits:
        raise ValidationError(
            f"Bit index {bit_index} is out of bounds for an input of {total_bits} bits (valid range: 0 to {total_bits - 1})."
        )

    return bit_index


def validate_bit_indices(bit_indices: Sequence[int], total_bits: int) -> list[int]:
    """Validate a sequence of bit indices for multi-bit flips.

    Args:
        bit_indices: Sequence of bit indices to flip.
        total_bits: Total number of bits in target byte array.

    Returns:
        A sorted list of unique validated bit indices.

    Raises:
        ValidationError: If any index is invalid, duplicate, or out of range.
    """
    if not isinstance(bit_indices, (list, tuple, set)):
        raise ValidationError("Bit indices must be provided as a sequence or collection.")

    if len(bit_indices) == 0:
        raise ValidationError("At least one bit index must be specified for multi-bit flip.")

    indices_list = list(bit_indices)
    for idx in indices_list:
        validate_bit_index(idx, total_bits)

    unique_indices = sorted(set(indices_list))
    if len(unique_indices) != len(indices_list):
        raise ValidationError("Duplicate bit indices detected. All flipped positions must be distinct.")

    if len(unique_indices) > total_bits:
        raise ValidationError(
            f"Requested {len(unique_indices)} bit flips, but input only has {total_bits} total bits."
        )

    return unique_indices


def validate_trial_count(trials: int, min_trials: int = 1, max_trials: int = 1000) -> int:
    """Validate statistical trial count.

    Args:
        trials: Number of experiments to run.
        min_trials: Minimum allowable trials.
        max_trials: Maximum allowable trials.

    Returns:
        Validated integer trial count.

    Raises:
        ValidationError: If trials count is outside acceptable bounds.
    """
    if not isinstance(trials, int) or isinstance(trials, bool):
        raise ValidationError(f"Trial count must be an integer, got {type(trials).__name__}.")

    if trials < min_trials or trials > max_trials:
        raise ValidationError(
            f"Trial count {trials} is outside allowable bounds [{min_trials}, {max_trials}]."
        )

    return trials

