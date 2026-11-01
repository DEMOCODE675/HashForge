# HashForge: Quality Assurance & Testing Report

This document details the automated testing strategy, verification matrices, and execution commands for the HashForge platform across both backend and frontend tiers.

---

## 1. Testing Strategy & Quality Standards

HashForge enforces a comprehensive dual-tier automated testing strategy:
1. **NIST Reference Standards:** Verification against official FIPS 180-4 (SHA-256) and FIPS 202 (SHA3-256) test vectors.
2. **Deterministic Bit Boundaries:** Strict validation of Big-Endian network indexing ($i = \lfloor k/8 \rfloor$, $b = 7 - (k \bmod 8)$) at bit 0 (MSB), bit 7 (LSB), and byte boundary transitions.
3. **Statistical Reproducibility:** Validation that Monte Carlo simulations produce identical metrics when seeded with fixed RNG states.
4. **FastAPI Contract Validation:** Verification of HTTP status codes, JSON payload schemas, boundary checks, and multipart streaming file uploads via `httpx.AsyncClient` / `TestClient`.
5. **Component Render Verification:** React component testing via Vitest and `@testing-library/react` ensuring exact bit grid cell counts, glowing class assignments, clipboard interactions, and strict zero-emoji navigation enforcement.

---

## 2. Backend Test Matrix (Pytest)

The backend test suite is located in `tests/` and contains **70 automated tests** (100% passing).

| Test Module | File | Cases | Description |
|---|---|:---:|---|
| **Hash Engine** | `tests/test_hash_engine.py` | 12 | Tests NIST standard vectors for empty string `""`, `"abc"`, and `"The quick brown fox jumps over the lazy dog"`. Validates Unicode, raw bytes, execution timing, and unsupported algorithm exceptions. |
| **Bit Operations** | `tests/test_bit_operations.py` | 13 | Verifies Big-Endian bit mapping, XOR inversion on bit 0 (MSB) and bit 7 (LSB), multi-bit flips, duplicate index detection, immutability of original data, and negative index rejection. |
| **Avalanche** | `tests/test_avalanche.py` | 8 | Validates zero Hamming distance on identical inputs, 100% distance on inverted bitstrings, diff mask generation, and metric boundaries. |
| **Experiments** | `tests/test_experiments.py` | 4 | Verifies deterministic seeded simulations, independent baseline resets between trials, empirical tendency near 50%, and comparative execution. |
| **File Integrity** | `tests/test_file_integrity.py` | 6 | Tests empty stream hashing, chunk-based streaming with 64KB buffers, identical vs tampered file detection, and vendor reference hash matching. |
| **Validators** | `tests/test_validators.py` | 10 | Validates algorithm strings, text length caps, bit index bounds, duplicate rejection, and trial count limits. |
| **Backend REST API** | `tests/test_backend_api.py` | 17 | Tests FastAPI endpoints (`/api/health`, `/api/hash/compute`, `/api/hash/dual`, `/api/hash/benchmark`, `/api/experiment/single-bit`, `/api/experiment/multi-bit`, `/api/avalanche/simulate`, `/api/file/hash`, `/api/file/compare`), error handling, and 422 validation errors. |
| **Pytest Total** | | **70** | **All 70 tests passed in 1.95s.** |

---

## 3. Frontend Component Test Matrix (Vitest)

The frontend test suite is located in `frontend/src/test/` and contains **10 automated tests** (100% passing).

| Test Module | File | Cases | Description |
|---|---|:---:|---|
| **BitGrid256** | `frontend/src/test/BitGrid256.test.tsx` | 3 | Verifies rendering of all 256 bits, amber glow class application on flipped bits, and bit tooltip contents on hover. |
| **HashBox** | `frontend/src/test/HashBox.test.tsx` | 4 | Verifies rendering of hex and binary digests, chunked byte grouping, and clipboard copy action handling. |
| **Navigation** | `frontend/src/test/Navigation.test.tsx` | 3 | Verifies sidebar route rendering, active link state transitions, and asserts that zero emojis exist in the navigation UI. |
| **Vitest Total** | | **10** | **All 10 tests passed in 13.88s.** |

**Grand Total Automated Tests:** **80 test cases** across backend and frontend.

---

## 4. Test Execution Instructions

### 4.1 Running Backend Pytest Tests
```powershell
cd c:\Users\priyanshu\PROJECTS\HASHFORGE
python -m pytest tests/ -v
```

To run with coverage reporting:
```powershell
python -m pytest tests/ --cov=core --cov=backend.api -v
```

### 4.2 Running Frontend Vitest Tests
```powershell
cd c:\Users\priyanshu\PROJECTS\HASHFORGE\frontend
npm run test
```

### 4.3 Running TypeScript Verification & Production Build
```powershell
cd c:\Users\priyanshu\PROJECTS\HASHFORGE\frontend
npm run typecheck
npm run build
```

---

## 5. NIST Test Vectors Verified

### SHA-256 (FIPS 180-4)
- **Empty String `""`:**
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- **`"abc"`:**
  `ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad`
- **`"The quick brown fox jumps over the lazy dog"`:**
  `d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592`

### SHA3-256 (FIPS 202)
- **Empty String `""`:**
  `a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a`
- **`"abc"`:**
  `3a985da74fe225b2045c172d6bd390bd855f086e3e9d525b46bfe24511431532`
- **`"The quick brown fox jumps over the lazy dog"`:**
  `69070dda01975c8c120c3aada1b282394e7f032fa9cf32f4cb2259a0897dfc04`
