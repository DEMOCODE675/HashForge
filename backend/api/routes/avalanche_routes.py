"""API routes for statistical Monte Carlo avalanche simulations."""

from typing import Union
from fastapi import APIRouter, HTTPException
from backend.api.schemas.avalanche_schemas import (
    AvalancheSimulationRequest,
    AvalancheSimulationResponse,
    ComparativeSimulationResponse,
    TrialRecordSchema,
)
from core.experiments import run_avalanche_simulation, run_comparative_simulation
from core.validators import ValidationError

router = APIRouter(prefix="/experiments", tags=["Avalanche Analytics"])


def _to_sim_response(sim) -> AvalancheSimulationResponse:
    trials_schemas = [
        TrialRecordSchema(
            trial=t["trial"],
            bit_index=t["bit_index"],
            byte_index=t["byte_index"],
            hamming_distance=t["hamming_distance"],
            avalanche_pct=t["avalanche_pct"],
            original_hex=t["original_hex"],
            modified_hex=t["modified_hex"],
            time_ms=round(t["time_ms"], 4),
        )
        for t in sim.trials
    ]

    return AvalancheSimulationResponse(
        original_text=sim.original_text,
        algorithm=sim.algorithm,
        total_input_bits=sim.total_input_bits,
        trials_count=sim.trials_count,
        mean_avalanche_pct=sim.mean_avalanche_pct,
        std_avalanche_pct=sim.std_avalanche_pct,
        min_avalanche_pct=sim.min_avalanche_pct,
        max_avalanche_pct=sim.max_avalanche_pct,
        median_avalanche_pct=sim.median_avalanche_pct,
        ideal_avalanche_pct=sim.ideal_avalanche_pct,
        trials=trials_schemas,
    )


@router.post("/avalanche", response_model=Union[AvalancheSimulationResponse, ComparativeSimulationResponse])
def execute_avalanche_simulation(payload: AvalancheSimulationRequest):
    """Execute high-sample Monte Carlo avalanche simulation."""
    try:
        if payload.comparative:
            comp_result = run_comparative_simulation(
                text=payload.text,
                trials=payload.trials,
                seed=payload.seed,
            )
            return ComparativeSimulationResponse(
                original_text=comp_result.original_text,
                trials_count=comp_result.trials_count,
                sha256_result=_to_sim_response(comp_result.sha256_result),
                sha3_256_result=_to_sim_response(comp_result.sha3_256_result),
            )
        else:
            algo = payload.algorithm or "sha256"
            sim_result = run_avalanche_simulation(
                text=payload.text,
                trials=payload.trials,
                algorithm=algo,
                seed=payload.seed,
                mode=payload.mode,
            )
            return _to_sim_response(sim_result)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation failed: {str(e)}")

