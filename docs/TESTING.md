# HashForge: Quality Assurance & Testing Report

This document details the test strategy, verification matrix, and execution instructions for the HashForge test suite.

---

## 1. Test Strategy & Standards

HashForge utilizes **Pytest** for automated regression and unit testing. The testing strategy prioritizes:
1. **NIST Reference Standards:** Verification against official FIPS 180-4 and FIPS 202 test vectors.
2. **Deterministic Bit Boundaries:** Strict validation of Big-Endian network indexing at bit 0 (MSB), bit 7 (LSB), and byte boundary transitions.
3. **Statistical Reproducibility:** Verifying that Monte Carlo simulations produce identical metrics when seeded.
4. **Boundary & Error Ingestion:** Testing negative indices, out-of-bounds indices, empty inputs, and non-existent algorithms.

---

## 2. Test Matrix & Suite Breakdown

| Module | Test File | Test Cases | Description |
|---|---|:---:|---|
| **Hash Engine** | `tests/test_hash_engine.py` | 12 | Tests NIST standard vectors for empty string `""`, `"abc"`, and `"The quick brown fox jumps over the lazy dog"`. Validates Unicode, raw bytes, execution timing, and unsupported algorithm exceptions. |
| **Bit Operations** | `tests/test_bit_operations.py` | 13 | Verifies Big-Endian bit mapping, XOR inversion on bit 0 (MSB) and bit 7 (LSB), multi-bit flips, duplicate index detection, immutability of original data, and negative index rejection. |
| **Avalanche** | `tests/test_avalanche.py` | 8 | Validates zero Hamming distance on identical inputs, 100% distance on inverted bitstrings, diff mask generation, and metric boundaries. |
| **Experiments** | `tests/test_experiments.py` | 4 | Verifies deterministic seeded simulations, independent baseline resets between trials, empirical tendency near 50%, and comparative execution. |
| **File Integrity** | `tests/test_file_integrity.py` | 6 | Tests empty stream hashing, chunk-based streaming with small buffers, identical vs tampered file detection, and vendor reference hash matching. |
| **Validators** | `tests/test_validators.py` | 10 | Validates algorithm strings, text length caps, bit index bounds, duplicate rejection, and trial count limits. |

**Total Test Count:** **53 tests** (100% passing).

---

## 3. Test Execution Instructions

### Running the Full Test Suite
```powershell
python -m pytest tests/ -v
```

### Running with Code Coverage
```powershell
python -m pytest tests/ --cov=core -v
```

### Running Specific Module Tests
```powershell
python -m pytest tests/test_hash_engine.py -v
python -m pytest tests/test_bit_operations.py -v
```

---

## 4. NIST Test Vectors Verified

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

