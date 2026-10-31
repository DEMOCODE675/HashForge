"""Unit tests for Validators and Constraint Checking."""

import pytest
from core.validators import (
    validate_algorithm,
    validate_text_input,
    validate_bit_index,
    validate_bit_indices,
    validate_trial_count,
    ValidationError,
)


class TestValidators:
    """Verifications for input validation guardrails."""

    def test_validate_algorithm_valid(self):
        assert validate_algorithm("sha256") == "sha256"
        assert validate_algorithm("SHA256") == "sha256"
        assert validate_algorithm("sha3_256") == "sha3_256"
        assert validate_algorithm(" SHA3_256 ") == "sha3_256"

    def test_validate_algorithm_invalid(self):
        with pytest.raises(ValidationError):
            validate_algorithm("md5")
        with pytest.raises(ValidationError):
            validate_algorithm(123)  # type: ignore

    def test_validate_text_input(self):
        assert validate_text_input("hello") == "hello"
        assert validate_text_input("", allow_empty=True) == ""

        with pytest.raises(ValidationError):
            validate_text_input("", allow_empty=False)

        with pytest.raises(ValidationError):
            validate_text_input(None)  # type: ignore

        with pytest.raises(ValidationError):
            validate_text_input("a" * 101, max_length=100)

    def test_validate_bit_index(self):
        assert validate_bit_index(0, 8) == 0
        assert validate_bit_index(7, 8) == 7

        with pytest.raises(ValidationError):
            validate_bit_index(-1, 8)

        with pytest.raises(ValidationError):
            validate_bit_index(8, 8)

        with pytest.raises(ValidationError):
            validate_bit_index(True, 8)  # bool rejected

        with pytest.raises(ValidationError):
            validate_bit_index(0, 0)  # total_bits <= 0

    def test_validate_bit_indices(self):
        assert validate_bit_indices([0, 5, 2], total_bits=16) == [0, 2, 5]

        # Duplicate detection
        with pytest.raises(ValidationError):
            validate_bit_indices([1, 2, 1], total_bits=16)

        # Empty sequence
        with pytest.raises(ValidationError):
            validate_bit_indices([], total_bits=16)

        # Out of bounds
        with pytest.raises(ValidationError):
            validate_bit_indices([0, 16], total_bits=16)

    def test_validate_trial_count(self):
        assert validate_trial_count(50) == 50
        assert validate_trial_count(1, min_trials=1, max_trials=100) == 1
        assert validate_trial_count(100, min_trials=1, max_trials=100) == 100

        with pytest.raises(ValidationError):
            validate_trial_count(0, min_trials=1)

        with pytest.raises(ValidationError):
            validate_trial_count(101, max_trials=100)

        with pytest.raises(ValidationError):
            validate_trial_count("50")  # type: ignore

