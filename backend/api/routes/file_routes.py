"""API routes for streaming file fingerprinting and integrity verification."""

from typing import Optional
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from backend.api.schemas.file_schemas import FileHashResponse, FileCompareResponse
from core.file_integrity import hash_file_stream, compare_file_hashes

router = APIRouter(prefix="/files", tags=["File Integrity"])

# Max allowed upload: 50MB (52,428,800 bytes)
MAX_FILE_BYTES = 50 * 1024 * 1024


def _to_file_hash_response(rep) -> FileHashResponse:
    return FileHashResponse(
        file_name=rep.file_name,
        file_size_bytes=rep.file_size_bytes,
        formatted_size=rep.formatted_size,
        sha256_hex=rep.sha256_hex,
        sha3_256_hex=rep.sha3_256_hex,
        chunks_processed=rep.chunks_processed,
        hashing_duration_ms=round(rep.hashing_duration_ms, 2),
    )


@router.post("/hash", response_model=FileHashResponse)
async def hash_file(file: UploadFile = File(...)):
    """Compute SHA-256 and SHA3-256 fingerprints in 64KB streaming chunks."""
    try:
        report = hash_file_stream(file.file, file_name=file.filename or "uploaded_file")
        if report.file_size_bytes > MAX_FILE_BYTES:
            raise HTTPException(
                status_code=413,
                detail=f"File exceeds maximum allowed size of 50 MB ({report.formatted_size}).",
            )
        return _to_file_hash_response(report)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File hashing failed: {str(e)}")


@router.post("/compare", response_model=FileCompareResponse)
async def compare_files(
    file_a: UploadFile = File(...),
    file_b: Optional[UploadFile] = File(None),
    reference_hash: Optional[str] = Form(None),
):
    """Compare two files or a file against an expected reference hash."""
    try:
        report_a = hash_file_stream(file_a.file, file_name=file_a.filename or "file_a")
        if report_a.file_size_bytes > MAX_FILE_BYTES:
            raise HTTPException(
                status_code=413,
                detail=f"File A exceeds maximum allowed size of 50 MB ({report_a.formatted_size}).",
            )

        report_b = None
        if file_b is not None:
            report_b = hash_file_stream(file_b.file, file_name=file_b.filename or "file_b")
            if report_b.file_size_bytes > MAX_FILE_BYTES:
                raise HTTPException(
                    status_code=413,
                    detail=f"File B exceeds maximum allowed size of 50 MB ({report_b.formatted_size}).",
                )

        comp = compare_file_hashes(
            report_a=report_a,
            report_b=report_b,
            reference_hash=reference_hash,
        )

        return FileCompareResponse(
            file_a=_to_file_hash_response(comp.file_a),
            file_b=_to_file_hash_response(comp.file_b) if comp.file_b else None,
            reference_hash=comp.reference_hash,
            is_identical=comp.is_identical,
            sha256_match=comp.sha256_match,
            sha3_256_match=comp.sha3_256_match,
            size_match=comp.size_match,
            details=comp.details,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File comparison failed: {str(e)}")

