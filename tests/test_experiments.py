"""Unit tests for Experiment runners and Statistical Simulations."""

import pytest
from core.experiments import (
    run_single_bit_trial,
    run_multi_bit_trial,
    run_avalanche_simulation,
    run_comparative_simulation,
)
from core.validators import ValidationError


class TestSingleAndMultiBitTrials:
    """Verifications for deterministic single and multi-bit experiments."""

    def test_single_bit_trial_basic(self):
        text = "HashForge"
        result = run_single_bit_trial(text, bit_index=0, algorithm="sha256")
        assert result.original_text == text
        assert result.bit_index == 0
        assert result.byte_index == 0
        assert result.bit_offset_in_byte == 7
        assert result.original_bit_value != result.modified_bit_value
        assert result.original_hash.hex_digest != result.modified_hash.hex_digest
        assert result.metrics.total_bits == 256
        assert 0 <= result.metrics.hamming_distance <= 256

    def test_single_bit_trial_sha3(self):
        text = "Hello World"
        result = run_single_bit_trial(text, bit_index=5, algorithm="sha3_256")
        assert result.algorithm == "sha3_256"
        assert result.metrics.hamming_distance > 50  # Cryptographic avalanche

    def test_single_bit_trial_empty_input_raises(self):
        with pytest.raises(ValidationError):
            run_single_bit_trial("", bit_index=0)

    def test_multi_bit_trial(self):
        text = "Cryptography"
        indices = [0, 8, 16]
        result = run_multi_bit_trial(text, bit_indices=indices, algorithm="sha256")
        assert result.flipped_bits_count == 3
        assert result.flipped_bit_indices == indices
        assert result.original_hash.hex_digest != result.modified_hash.hex_digest
        assert result.metrics.total_bits == 256


class TestStatisticalSimulation:
    """Verifications for multi-trial Monte Carlo avalanche simulations."""

    def test_reproducible_seeded_simulation(self):
        text = "StatisticalTestInput123"
        seed = 42
        sim_1 = run_avalanche_simulation(text, trials=20, algorithm="sha256", seed=seed)
        sim_2 = run_avalanche_simulation(text, trials=20, algorithm="sha256", seed=seed)

        assert sim_1.trials_count == 20
        assert sim_1.mean_avalanche_pct == sim_2.mean_avalanche_pct
        assert sim_1.std_avalanche_pct == sim_2.std_avalanche_pct
        assert sim_1.min_avalanche_pct == sim_2.min_avalanche_pct
        assert sim_1.max_avalanche_pct == sim_2.max_avalanche_pct
        assert [t["bit_index"] for t in sim_1.trials] == [t["bit_index"] for t in sim_2.trials]

    def test_independent_trial_baseline(self):
        # Verify that each single-bit trial resets to the original baseline
        text = "Avalanche"
        sim = run_avalanche_simulation(text, trials=10, algorithm="sha256", mode="single_bit")
        for record in sim.trials:
            # Recompute single trial to verify independence
            recomputed = run_single_bit_trial(text, bit_index=record["bit_index"], algorithm="sha256")
            assert recomputed.metrics.hamming_distance == record["hamming_distance"]

    def test_avalanche_statistical_tendency_near_50(self):
        # Over 50 random single-bit flips, mean avalanche should be reasonably near 50%
        # (typically between 45% and 55%)
        text = "The quick brown fox jumps over the lazy dog and produces cryptographic randomness"
        sim = run_avalanche_simulation(text, trials=50, algorithm="sha256", seed=12345)
        assert 40.0 <= sim.mean_avalanche_pct <= 60.0
        assert sim.min_avalanche_pct > 20.0
        assert sim.max_avalanche_pct < 80.0
        assert sim.std_avalanche_pct >= 0.0

    def test_comparative_simulation(self):
        text = "ComparativeBenchmark"
        comp = run_comparative_simulation(text, trials=15, seed=999)
        assert comp.trials_count == 15
        assert comp.sha256_result.trials_count == 15
        assert comp.sha3_256_result.trials_count == 15
        # Bit indices used must be identical
        sha256_bits = [t["bit_index"] for t in comp.sha256_result.trials]
        sha3_bits = [t["bit_index"] for t in comp.sha3_256_result.trials]
        assert sha256_bits == sha3_bits

