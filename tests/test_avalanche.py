"""Unit tests for Hamming Distance and Avalanche Effect calculations."""

import pytest
from core.avalanche import (
    hamming_distance,
    avalanche_percentage,
    get_diff_mask,
    compute_avalanche_metrics,
)
from core.validators import ValidationError


class TestAvalancheCalculations:
    """Verifications for distance metrics and percentage evaluations."""

    def test_identical_hashes_zero_distance(self):
        bits = "0" * 256
        dist = hamming_distance(bits, bits)
        assert dist == 0
        pct = avalanche_percentage(dist, 256)
        assert pct == 0.0

    def test_completely_different_hashes_full_distance(self):
        bits_a = "0" * 256
        bits_b = "1" * 256
        dist = hamming_distance(bits_a, bits_b)
        assert dist == 256
        pct = avalanche_percentage(dist, 256)
        assert pct == 100.0

    def test_known_pattern_distance(self):
        # 128 matching bits, 128 differing bits -> exactly 50%
        bits_a = ("0" * 128) + ("1" * 128)
        bits_b = ("0" * 128) + ("0" * 128)
        dist = hamming_distance(bits_a, bits_b)
        assert dist == 128
        pct = avalanche_percentage(dist, 256)
        assert pct == 50.0

    def test_unequal_length_raises(self):
        bits_a = "0" * 256
        bits_b = "1" * 255
        with pytest.raises(ValidationError):
            hamming_distance(bits_a, bits_b)

        with pytest.raises(ValidationError):
            get_diff_mask(bits_a, bits_b)

    def test_invalid_characters_raises(self):
        with pytest.raises(ValidationError):
            hamming_distance("0101", "0123")

    def test_diff_mask(self):
        a = "0100"
        b = "1101"
        mask = get_diff_mask(a, b)
        assert mask == [True, False, False, True]

    def test_compute_avalanche_metrics(self):
        a = "00000000"
        b = "10000001"
        metrics = compute_avalanche_metrics(a, b)
        assert metrics.hamming_distance == 2
        assert metrics.total_bits == 8
        assert metrics.avalanche_percentage == 25.0
        assert metrics.changed_indices == (0, 7)
        assert metrics.unchanged_count == 6
        assert metrics.distance_from_ideal == 25.0

    def test_avalanche_percentage_bounds(self):
        with pytest.raises(ValidationError):
            avalanche_percentage(300, 256)
        with pytest.raises(ValidationError):
            avalanche_percentage(-1, 256)
        with pytest.raises(ValidationError):
            avalanche_percentage(10, 0)

