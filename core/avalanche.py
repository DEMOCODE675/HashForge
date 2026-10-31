"""Avalanche Effect and Hamming Distance mathematical operations."""

from dataclasses import dataclass
from typing import List, Tuple
from core.validators import ValidationError


@dataclass(frozen=True)
class AvalancheMetrics:
    """Metrics quantifying the difference between two cryptographic hash outputs."""
    hamming_distance: int
    total_bits: int
    avalanche_percentage: float
    changed_indices: Tuple[int, ...]
    unchanged_count: int

    @property
    def changed_count(self) -> int:
        return self.hamming_distance

    @property
    def distance_from_ideal(self) -> float:
        """Absolute distance from theoretical ideal avalanche of 50.0%."""
        return abs(self.avalanche_percentage - 50.0)


def hamming_distance(bin_a: str, bin_b: str) -> int:
    """Calculate the Hamming distance (number of differing bit positions) between two binary strings.

    Args:
        bin_a: First binary string.
        bin_b: Second binary string.

    Returns:
        Integer count of differing bit positions.

    Raises:
        ValidationError: If strings have unequal lengths or contain non-binary characters.
    """
    if len(bin_a) != len(bin_b):
        raise ValidationError(
            f"Cannot calculate Hamming distance for mismatched lengths ({len(bin_a)} vs {len(bin_b)} bits)."
        )

    dist = 0
    for a, b in zip(bin_a, bin_b):
        if a not in ("0", "1") or b not in ("0", "1"):
            raise ValidationError("Binary strings must contain only '0' and '1' characters.")
        if a != b:
            dist += 1
    return dist


def avalanche_percentage(hamming_dist: int, total_bits: int) -> float:
    """Calculate avalanche effect percentage: (Hamming Distance / Total Bits) * 100.

    Args:
        hamming_dist: Number of flipped output bits.
        total_bits: Total bit length of the hash digest (e.g., 256).

    Returns:
        Float percentage in range [0.0, 100.0].

    Raises:
        ValidationError: If total_bits <= 0 or hamming_dist is out of range.
    """
    if total_bits <= 0:
        raise ValidationError("Total bits must be strictly positive.")
    if hamming_dist < 0 or hamming_dist > total_bits:
        raise ValidationError(
            f"Hamming distance ({hamming_dist}) cannot exceed total bits ({total_bits}) or be negative."
        )

    return (hamming_dist / total_bits) * 100.0


def get_diff_mask(bin_a: str, bin_b: str) -> List[bool]:
    """Generate a boolean difference mask comparing two binary strings.

    Args:
        bin_a: First binary string.
        bin_b: Second binary string.

    Returns:
        List of booleans, where True indicates that the bit at that position changed.
    """
    if len(bin_a) != len(bin_b):
        raise ValidationError(
            f"Binary lengths must match to compute diff mask ({len(bin_a)} vs {len(bin_b)})."
        )

    return [a != b for a, b in zip(bin_a, bin_b)]


def compute_avalanche_metrics(bin_a: str, bin_b: str) -> AvalancheMetrics:
    """Compute comprehensive avalanche metrics for two binary hash digests.

    Args:
        bin_a: Original binary hash digest.
        bin_b: Perturbed binary hash digest.

    Returns:
        AvalancheMetrics instance.
    """
    dist = hamming_distance(bin_a, bin_b)
    total_bits = len(bin_a)
    pct = avalanche_percentage(dist, total_bits)

    changed_indices = tuple(i for i, (a, b) in enumerate(zip(bin_a, bin_b)) if a != b)
    unchanged_count = total_bits - dist

    return AvalancheMetrics(
        hamming_distance=dist,
        total_bits=total_bits,
        avalanche_percentage=pct,
        changed_indices=changed_indices,
        unchanged_count=unchanged_count,
    )

