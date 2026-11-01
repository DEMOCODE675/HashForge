"""API routes for bit-level perturbation experiments."""

import random
from fastapi import APIRouter, HTTPException
from backend.api.schemas.experiment_schemas import (
    SingleBitRequest,
    SingleBitResponse,
    MultiBitRequest,
    MultiBitRandomRequest,
    MultiBitResponse,
    AvalancheMetricsSchema,
)
from backend.api.schemas.hash_schemas import HashResponse
from core.experiments import run_single_bit_trial, run_multi_bit_trial
from core.bit_operations import text_to_bytes, bytes_to_bits
from core.validators import ValidationError

router = APIRouter(prefix="/experiments", tags=["Bit Experiments"])


def _to_hash_response(hr) -> HashResponse:
    return HashResponse(
        algorithm=hr.algorithm,
        hex_digest=hr.hex_digest,
        binary_digest=hr.binary_digest,
        digest_bits=hr.digest_bits,
        digest_bytes=hr.digest_bytes,
        input_length_bytes=hr.input_length_bytes,
        execution_time_ms=round(hr.execution_time_ms, 5),
        formatted_hex=hr.formatted_hex,
    )


def _to_metrics_schema(m) -> AvalancheMetricsSchema:
    return AvalancheMetricsSchema(
        hamming_distance=m.hamming_distance,
        total_bits=m.total_bits,
        avalanche_percentage=round(m.avalanche_percentage, 2),
        changed_indices=list(m.changed_indices),
        unchanged_count=m.unchanged_count,
        distance_from_ideal=round(m.distance_from_ideal, 2),
    )


@router.post("/single-bit", response_model=SingleBitResponse)
def execute_single_bit_experiment(payload: SingleBitRequest):
    """Execute a single-bit XOR perturbation experiment."""
    try:
        trial = run_single_bit_trial(
            text=payload.text,
            bit_index=payload.bit_index,
            algorithm=payload.algorithm,
        )

        diff_mask = [i in trial.metrics.changed_indices for i in range(256)]

        return SingleBitResponse(
            original_text=trial.original_text,
            total_input_bits=trial.total_input_bits,
            bit_index=trial.bit_index,
            byte_index=trial.byte_index,
            bit_offset_in_byte=trial.bit_offset_in_byte,
            original_bit_value=trial.original_bit_value,
            modified_bit_value=trial.modified_bit_value,
            original_bytes_hex=trial.original_bytes.hex(),
            modified_bytes_hex=trial.modified_bytes.hex(),
            original_binary_input=bytes_to_bits(trial.original_bytes),
            modified_binary_input=bytes_to_bits(trial.modified_bytes),
            algorithm=trial.algorithm,
            original_hash=_to_hash_response(trial.original_hash),
            modified_hash=_to_hash_response(trial.modified_hash),
            metrics=_to_metrics_schema(trial.metrics),
            diff_mask=diff_mask,
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Experiment failed: {str(e)}")


@router.post("/multi-bit", response_model=MultiBitResponse)
def execute_multi_bit_experiment(payload: MultiBitRequest):
    """Execute a multi-bit XOR perturbation experiment with explicit bit indices."""
    try:
        trial = run_multi_bit_trial(
            text=payload.text,
            bit_indices=payload.bit_indices,
            algorithm=payload.algorithm,
        )

        diff_mask = [i in trial.metrics.changed_indices for i in range(256)]

        return MultiBitResponse(
            original_text=trial.original_text,
            total_input_bits=trial.total_input_bits,
            flipped_bit_indices=trial.flipped_bit_indices,
            flipped_bits_count=trial.flipped_bits_count,
            original_bytes_hex=trial.original_bytes.hex(),
            modified_bytes_hex=trial.modified_bytes.hex(),
            algorithm=trial.algorithm,
            original_hash=_to_hash_response(trial.original_hash),
            modified_hash=_to_hash_response(trial.modified_hash),
            metrics=_to_metrics_schema(trial.metrics),
            diff_mask=diff_mask,
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Multi-bit experiment failed: {str(e)}")


@router.post("/multi-bit/random", response_model=MultiBitResponse)
def execute_multi_bit_random_experiment(payload: MultiBitRandomRequest):
    """Sample k distinct bits randomly and execute multi-bit perturbation."""
    try:
        raw_bytes = text_to_bytes(payload.text)
        total_bits = len(raw_bytes) * 8

        if payload.k_bits > total_bits:
            raise ValidationError(
                f"Requested {payload.k_bits} bit flips, but input only contains {total_bits} bits."
            )

        rng = random.Random(payload.seed)
        sampled_indices = sorted(rng.sample(range(total_bits), payload.k_bits))

        trial = run_multi_bit_trial(
            text=payload.text,
            bit_indices=sampled_indices,
            algorithm=payload.algorithm,
        )

        diff_mask = [i in trial.metrics.changed_indices for i in range(256)]

        return MultiBitResponse(
            original_text=trial.original_text,
            total_input_bits=trial.total_input_bits,
            flipped_bit_indices=trial.flipped_bit_indices,
            flipped_bits_count=trial.flipped_bits_count,
            original_bytes_hex=trial.original_bytes.hex(),
            modified_bytes_hex=trial.modified_bytes.hex(),
            algorithm=trial.algorithm,
            original_hash=_to_hash_response(trial.original_hash),
            modified_hash=_to_hash_response(trial.modified_hash),
            metrics=_to_metrics_schema(trial.metrics),
            diff_mask=diff_mask,
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Random multi-bit experiment failed: {str(e)}")

