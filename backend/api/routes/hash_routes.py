"""API routes for hashing operations and algorithm comparisons."""

import time
from fastapi import APIRouter, HTTPException
from backend.api.schemas.hash_schemas import (
    HashRequest,
    HashResponse,
    AlgorithmCompareRequest,
    AlgorithmCompareResponse,
    AlgorithmBenchmarkInfo,
)
from core.hash_engine import compute_hash, HashResult
from core.bit_operations import text_to_bytes
from core.avalanche import hamming_distance, avalanche_percentage
from core.validators import ValidationError

router = APIRouter(prefix="/hash", tags=["Hashing"])


def _to_hash_response(hr: HashResult) -> HashResponse:
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


@router.post("/generate", response_model=HashResponse)
def generate_hash(payload: HashRequest):
    """Compute SHA-256 or SHA3-256 hash digest for input text."""
    try:
        hr = compute_hash(payload.text, algorithm=payload.algorithm)
        return _to_hash_response(hr)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hash computation failed: {str(e)}")


@router.post("/compare", response_model=AlgorithmCompareResponse)
def compare_algorithms(payload: AlgorithmCompareRequest):
    """Compare SHA-256 and SHA3-256 on identical input and run local benchmarks."""
    try:
        raw_bytes = text_to_bytes(payload.text)
        total_bits = len(raw_bytes) * 8

        res_sha2 = compute_hash(payload.text, algorithm="sha256")
        res_sha3 = compute_hash(payload.text, algorithm="sha3_256")

        dist = hamming_distance(res_sha2.binary_digest, res_sha3.binary_digest)
        div_pct = avalanche_percentage(dist, 256)

        bench_sha2 = None
        bench_sha3 = None
        iters = payload.benchmark_iterations or 1000

        if iters > 0:
            # Benchmark SHA-256
            t0 = time.perf_counter_ns()
            for _ in range(iters):
                compute_hash(raw_bytes, "sha256")
            t1 = time.perf_counter_ns()
            tot_sha2_ms = (t1 - t0) / 1_000_000.0
            avg_sha2_us = (tot_sha2_ms / iters) * 1000.0
            bench_sha2 = AlgorithmBenchmarkInfo(
                iterations=iters,
                total_time_ms=round(tot_sha2_ms, 3),
                average_latency_us=round(avg_sha2_us, 3),
            )

            # Benchmark SHA3-256
            t0 = time.perf_counter_ns()
            for _ in range(iters):
                compute_hash(raw_bytes, "sha3_256")
            t1 = time.perf_counter_ns()
            tot_sha3_ms = (t1 - t0) / 1_000_000.0
            avg_sha3_us = (tot_sha3_ms / iters) * 1000.0
            bench_sha3 = AlgorithmBenchmarkInfo(
                iterations=iters,
                total_time_ms=round(tot_sha3_ms, 3),
                average_latency_us=round(avg_sha3_us, 3),
            )

        return AlgorithmCompareResponse(
            original_text=payload.text,
            input_bytes_count=len(raw_bytes),
            input_bits_count=total_bits,
            sha256=_to_hash_response(res_sha2),
            sha3_256=_to_hash_response(res_sha3),
            cross_hamming_distance=dist,
            cross_divergence_percentage=round(div_pct, 2),
            sha256_benchmark=bench_sha2,
            sha3_benchmark=bench_sha3,
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")

