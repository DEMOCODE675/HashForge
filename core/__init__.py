"""HashForge Core Cryptographic & Analytics Engine."""

from core.hash_engine import HashResult, compute_hash, bytes_to_binary_string, hex_to_binary_string
from core.bit_operations import (
    text_to_bytes,
    flip_bit,
    flip_multiple_bits,
    get_bit_at,
    bytes_to_bits,
    format_binary_grouped,
    BIT_INDEXING_EXPLANATION,
)
from core.avalanche import (
    hamming_distance,
    avalanche_percentage,
    get_diff_mask,
    AvalancheMetrics,
    compute_avalanche_metrics,
)
from core.validators import (
    validate_text_input,
    validate_bit_index,
    validate_bit_indices,
    validate_algorithm,
    validate_trial_count,
    ValidationError,
)
from core.experiments import (
    SingleBitTrialResult,
    MultiBitTrialResult,
    AvalancheSimulationResult,
    run_single_bit_trial,
    run_multi_bit_trial,
    run_avalanche_simulation,
)
from core.file_integrity import (
    hash_file_stream,
    compare_file_hashes,
    FileIntegrityReport,
    format_file_size,
)

__all__ = [
    "HashResult",
    "compute_hash",
    "bytes_to_binary_string",
    "hex_to_binary_string",
    "text_to_bytes",
    "flip_bit",
    "flip_multiple_bits",
    "get_bit_at",
    "bytes_to_bits",
    "format_binary_grouped",
    "BIT_INDEXING_EXPLANATION",
    "hamming_distance",
    "avalanche_percentage",
    "get_diff_mask",
    "AvalancheMetrics",
    "compute_avalanche_metrics",
    "validate_text_input",
    "validate_bit_index",
    "validate_bit_indices",
    "validate_algorithm",
    "validate_trial_count",
    "ValidationError",
    "SingleBitTrialResult",
    "MultiBitTrialResult",
    "AvalancheSimulationResult",
    "run_single_bit_trial",
    "run_multi_bit_trial",
    "run_avalanche_simulation",
    "hash_file_stream",
    "compare_file_hashes",
    "FileIntegrityReport",
    "format_file_size",
]

