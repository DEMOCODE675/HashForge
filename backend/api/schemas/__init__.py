"""Schemas export package."""

try:
    from backend.api.schemas.hash_schemas import (
        HashRequest,
        HashResponse,
        AlgorithmCompareRequest,
        AlgorithmCompareResponse,
        AlgorithmBenchmarkInfo,
    )
    from backend.api.schemas.experiment_schemas import (
        SingleBitRequest,
        SingleBitResponse,
        MultiBitRequest,
        MultiBitRandomRequest,
        MultiBitResponse,
        AvalancheMetricsSchema,
    )
    from backend.api.schemas.avalanche_schemas import (
        AvalancheSimulationRequest,
        AvalancheSimulationResponse,
        ComparativeSimulationResponse,
        TrialRecordSchema,
    )
    from backend.api.schemas.file_schemas import (
        FileHashResponse,
        FileCompareResponse,
    )
except ImportError:
    from api.schemas.hash_schemas import (
        HashRequest,
        HashResponse,
        AlgorithmCompareRequest,
        AlgorithmCompareResponse,
        AlgorithmBenchmarkInfo,
    )
    from api.schemas.experiment_schemas import (
        SingleBitRequest,
        SingleBitResponse,
        MultiBitRequest,
        MultiBitRandomRequest,
        MultiBitResponse,
        AvalancheMetricsSchema,
    )
    from api.schemas.avalanche_schemas import (
        AvalancheSimulationRequest,
        AvalancheSimulationResponse,
        ComparativeSimulationResponse,
        TrialRecordSchema,
    )
    from api.schemas.file_schemas import (
        FileHashResponse,
        FileCompareResponse,
    )

__all__ = [
    "HashRequest",
    "HashResponse",
    "AlgorithmCompareRequest",
    "AlgorithmCompareResponse",
    "AlgorithmBenchmarkInfo",
    "SingleBitRequest",
    "SingleBitResponse",
    "MultiBitRequest",
    "MultiBitRandomRequest",
    "MultiBitResponse",
    "AvalancheMetricsSchema",
    "AvalancheSimulationRequest",
    "AvalancheSimulationResponse",
    "ComparativeSimulationResponse",
    "TrialRecordSchema",
    "FileHashResponse",
    "FileCompareResponse",
]

