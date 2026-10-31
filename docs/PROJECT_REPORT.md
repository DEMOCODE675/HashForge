# HashForge: Project Report

## An Interactive Cryptographic Hashing and Avalanche Effect Visualization Laboratory Using SHA-256 and SHA3-256

**Author / Project Lead:** HashForge Engineering Team  
**Institution:** Academic Project Submission — Department of Computer Science & Cybersecurity  
**Date:** Academic Year 2026  
**Status:** Completed & Verified  

---

## 1. Abstract

Cryptographic hash functions form the mathematical backbone of modern digital infrastructure, securing blockchains, public-key certificates, software distribution pipelines, and authentication tokens. A foundational property guaranteeing their security is the **Strict Avalanche Criterion (SAC)**, which mandates that changing even a single input bit must cause each output bit to invert with a probability of approximately 50%. While students often memorize this definition theoretically, the non-linear cascading mechanics within compression functions remain opaque.

This project presents **HashForge**, an interactive, local, educational laboratory built in Python and Streamlit. HashForge implements FIPS 180-4 (SHA-256) and FIPS 202 (SHA3-256), combining network big-endian bit manipulation, XOR-based bit perturbation, high-resolution Hamming distance calculations, and interactive Plotly visualizations. Through 7 specialized laboratory modules, HashForge allows users to perform single-bit and multi-bit perturbations, run high-volume Monte Carlo simulations, detect file tampering via chunked streaming, and test their comprehension through an integrated quiz. The platform is entirely local, dependency-conscious, and verified through a 53-case automated Pytest suite.

---

## 2. Introduction & Background

Hash functions map arbitrary-length bit strings to fixed-length digests:
$$H: \{0, 1\}^* \to \{0, 1\}^n$$

Modern cryptographic hash functions trace their lineage to Claude Shannon's 1949 foundational paper *Communication Theory of Secrecy Systems*, which established the dual principles of **Confusion** and **Diffusion**:
1. **Confusion:** Obscuring the relationship between the plaintext and ciphertext (or hash digest).
2. **Diffusion:** Dispersing the statistical influence of an individual plaintext symbol across the entire ciphertext.

In 1973, Horst Feistel characterized this diffusion in block ciphers and compression functions as the **Avalanche Effect**. In 1985, Webster and Tavares formalized this into the **Strict Avalanche Criterion (SAC)**: a cryptographic transformation satisfies SAC if, whenever an individual input bit is complemented, each output bit changes with a probability of $p = 0.5$.

---

## 3. Problem Statement & Existing Limitations

In traditional computer science pedagogy, cryptography is taught using abstract mathematical definitions or CLI utilities (e.g. `sha256sum`, OpenSSL CLI):
- **Lack of Microscopic Inspection:** Command-line utilities output a static 64-character hexadecimal string. They do not expose which specific bits changed, the Hamming distance, or the bit-level diff matrix.
- **Disconnected Scripts:** Students often write fragmented, ad-hoc Python scripts that fail to handle edge conditions, lack proper bit-indexing standards, or confuse character replacement with bit inversion.
- **Misconceptions Around Security:** Beginners frequently confuse execution speed with cryptographic robustness or attempt to store passwords using plain SHA-256 without understanding why memory-hard Key Derivation Functions (KDFs) are necessary.

---

## 4. Proposed Solution: HashForge

**HashForge** was designed to provide a unified, production-grade educational platform. Rather than a rudimentary demo, HashForge provides:
1. **FIPS-Compliant Core:** Pure Python standard library `hashlib` bindings to SHA-256 and SHA3-256.
2. **Big-Endian Bit Indexing Standard:** Clear mathematical mapping between user-selected bit indices and physical byte modifications.
3. **Structured 256-Bit Visualizer:** A responsive 8-row, 32-bit grid that visually highlights changed bits with glowing accents.
4. **Statistical Laboratory:** Monte Carlo engine evaluating 10 to 500 independent trials, graphing empirical frequency distributions against theoretical binomial curves.
5. **Memory-Safe File Integrity Engine:** 64KB streaming buffers that inspect file tampering without exhausting system memory.
6. **Built-In Learning Center & Evaluation Quiz:** Structured curriculum covering 12 foundational topics and a 10-question evaluation quiz with instant grading and explanations.

---

## 5. Project Objectives

1. **Demonstrate Strict Avalanche Criterion:** Visually and mathematically prove that a 1-bit input flip yields an average of 128 differing output bits ($\approx 50.00\%$).
2. **Compare Cryptographic Families:** Contrast the Merkle-Damgård iterative compression of SHA-256 against the Keccak Sponge construction of SHA3-256.
3. **Ensure Mathematical Accuracy:** Validate all computations against official NIST standard test vectors and ensure zero synthetic or mocked data.
4. **Deliver Intuitive Visual Analytics:** Render interactive Plotly charts, histograms, and bit diff matrices with high color contrast.
5. **Maintain Production Quality:** Decouple cryptographic algorithms (`core/`) from the user interface (`pages/`), achieving 100% test coverage across core routines.

---

## 6. System Requirements

### 6.1 Hardware Requirements
- **Processor:** 1.5 GHz Dual-Core 64-bit x86/ARM processor (Intel Core i3, AMD Ryzen, Apple Silicon, etc.)
- **Memory (RAM):** 2 GB minimum (4 GB recommended)
- **Disk Space:** 250 MB free disk space
- **Display Resolution:** Minimum $1280 \times 720$ (optimized for responsive desktop viewing)

### 6.2 Software Requirements
- **Operating System:** Windows 10/11, macOS 12+, or modern Linux (Ubuntu 22.04+)
- **Python Runtime:** Python 3.11 or newer (tested on Python 3.13)
- **Web Browser:** Google Chrome, Mozilla Firefox, Microsoft Edge, or Safari with WebGL enabled

### 6.3 Dependencies
- `streamlit >= 1.35.0` (Reactive web framework)
- `numpy >= 1.26.0` (Numerical calculations)
- `pandas >= 2.2.0` (Tabular trial data handling)
- `plotly >= 5.20.0` (Interactive visualization engine)
- `pytest >= 8.0.0` (Automated testing framework)

---

## 7. Mathematical Formulations & Algorithms

### 7.1 Big-Endian / Network Bit Indexing
Let an input string $S$ be encoded into a byte array $B$ of length $N = |B|$:
$$B = [b_0, b_1, b_2, \dots, b_{N-1}], \quad \text{where } b_i \in \{0, \dots, 255\}$$
The addressable bit space spans $k \in \{0, 1, \dots, 8N - 1\}$. The mapping from bit index $k$ to byte position $i$ and bit offset $b$ is:
$$i = \lfloor k / 8 \rfloor, \quad b = 7 - (k \bmod 8)$$
The bit at index $k$ has numeric weight $2^b$. Flipping bit $k$ via bitwise XOR is computed as:
$$b_i' = b_i \oplus (1 \ll b)$$
This ensures that bit 0 is the Most Significant Bit (MSB, weight 128) of Byte 0, bit 7 is the Least Significant Bit (LSB, weight 1) of Byte 0, and bit 8 begins Byte 1.

### 7.2 Hamming Distance
For two binary hash digests $H_1, H_2 \in \{0, 1\}^n$ where $n = 256$:
$$D(H_1, H_2) = \sum_{j=0}^{n-1} (H_1[j] \oplus H_2[j])$$

### 7.3 Avalanche Percentage
$$\text{Avalanche } \% = \left(\frac{D(H_1, H_2)}{n}\right) \times 100\%$$

### 7.4 Binomial Distribution of Output Bits
Under the Strict Avalanche Criterion, each of the $n = 256$ output bits acts as an independent Bernoulli trial with probability $p = 0.5$:
$$P(D = k) = \binom{n}{k} p^k (1-p)^{n-k} = \binom{256}{k} (0.5)^{256}$$
- **Expected Mean:** $\mu = n \cdot p = 256 \times 0.5 = 128 \text{ bits } (50.0\%)$
- **Standard Deviation:** $\sigma = \sqrt{n \cdot p \cdot (1-p)} = \sqrt{256 \times 0.25} = \sqrt{64} = 8 \text{ bits } (3.125\%)$
Thus, approximately 95.4% of all empirical single-bit trials will fall within $\mu \pm 2\sigma = [112, 144] \text{ bits}$ ($43.75\% \text{ to } 56.25\%$).

---

## 8. Module Specifications

### Module 1: Hash Generator
- Allows users to enter plain text or load NIST test vectors.
- Calculates SHA-256 and SHA3-256 simultaneously.
- Provides dual views: 64-character hexadecimal and 256-character binary.
- Formats hex in 8-character chunks for human readability.
- Exports cryptographic digest reports as downloadable text files.

### Module 2: Algorithm Lab
- Compares SHA-256 (SHA-2 family) against SHA3-256 (SHA-3 family).
- Calculates cross-algorithm Hamming distance (proving mutual independence).
- Executes local latency benchmarks over 100 to 5,000 iterations to measure throughput.
- Explains structural differences between Merkle-Damgård compression and Keccak Sponge permutation.

### Module 3: Single-Bit Flip Lab
- Converts user text to UTF-8 bytes and displays input bit representation.
- Provides a continuous slider to target any bit index $0 \le k < 8N$.
- Inverts exactly that bit via XOR without modifying any other byte.
- Computes original and modified hashes.
- Displays an interactive 256-bit grid (8 rows of 32 bits) with color-coded changed bits.

### Module 4: Multi-Bit Flip Lab
- Evaluates the effect of flipping $k$ bits simultaneously.
- Supports pseudo-random bit selection (with seed control) or manual index specification.
- Demonstrates that multi-bit perturbations do not increase avalanche percentage beyond 50%, illustrating non-linear saturation.

### Module 5: Avalanche Analyzer
- Executes Monte Carlo simulations across 10, 50, 100, or custom (up to 500) trials.
- Implements two trial modes: Independent single-bit trials (resets to original baseline each trial) and Cumulative mutation.
- Computes empirical mean, standard deviation, minimum, maximum, and median.
- Renders Plotly histograms with theoretical 50% lines, trial-by-trial scatter plots, and boxplot comparisons.
- Exports all trial records as a downloadable CSV.

### Module 6: File Integrity Lab
- Uses streaming 64KB buffers (`hashlib.update()`) to hash files without excessive RAM consumption.
- Supports single file fingerprinting, two-file comparison (tamper detection), and vendor reference hash validation.
- Clearly distinguishes between data integrity (hash matching) and authenticity (trusted distribution/digital signatures).

### Module 7: Learning Center & Cryptography Quiz
- 12 comprehensive curriculum topics covering cryptography basics, hash mechanics, blockchain Merkle trees, software supply chains, and password security.
- Interactive 10-question evaluation quiz with instant score calculation, status badges, and technical explanations.

---

## 9. Test Cases & QA Validation

The automated test suite (`tests/`) contains 53 unit and integration tests executed using Pytest:

| Test File | Focus Area | Cases | Status |
|---|---|:---:|:---:|
| `test_hash_engine.py` | NIST test vectors (empty, "abc", fox), Unicode, timing | 12 | ✅ Passed |
| `test_bit_operations.py` | MSB, LSB, middle bits, XOR inversion, out-of-bounds | 13 | ✅ Passed |
| `test_avalanche.py` | Hamming distance, zero distance, SAC bounds, diff mask | 8 | ✅ Passed |
| `test_experiments.py` | Seed reproducibility, baseline reset, statistical tendency | 4 | ✅ Passed |
| `test_file_integrity.py` | 64KB chunking, empty files, parity checks, reference match | 6 | ✅ Passed |
| `test_validators.py` | Input sanitization, bit range guardrails, type checking | 10 | ✅ Passed |
| **Total** | **All System Components** | **53** | **100% Passed** |

---

## 10. Results & Discussion

Empirical testing on HashForge demonstrated the following results across 100 independent trials on the string `"HashForge Cryptographic Avalanche Statistical Evaluation 2026"`:
- **SHA-256 Empirical Mean:** $49.88\%$ (Hamming distance $\approx 127.7$ bits)
- **SHA3-256 Empirical Mean:** $50.12\%$ (Hamming distance $\approx 128.3$ bits)
- **Standard Deviation:** $\approx 3.20\%$ (closely matching theoretical binomial prediction of $\sigma = 3.125\%$)
- **Minimum Avalanche:** $41.80\%$
- **Maximum Avalanche:** $57.42\%$

These empirical results prove that both SHA-256 and SHA3-256 satisfy the Strict Avalanche Criterion within expected statistical variation.

---

## 11. Security Limitations & Ethical Use

1. **Educational Scope:** HashForge is an interactive visualization tool. It does not replace enterprise cryptographic hardware modules (HSMs).
2. **Password Storage Disclaimer:** HashForge explicitly warns users that general-purpose hashes (SHA-256) are unsuitable for password storage due to high GPU hashing rates ($>15$ billion hashes/sec), explaining why memory-hard KDFs like Argon2id and bcrypt must be used instead.
3. **Collision Resistance vs Avalanche:** A high avalanche percentage does not by itself guarantee collision resistance; collision resistance requires a sufficiently large output space ($2^{128}$ operations for 256 bits).

---

## 12. Conclusion & Future Scope

HashForge successfully demonstrates the mechanics of cryptographic hashing, bit perturbation, and the avalanche effect. By combining rigorous FIPS implementations with interactive visualization tools, it bridges the gap between theoretical cryptography and practical understanding.

### Future Scope:
- Integration of Post-Quantum Cryptography (PQC) hash-based signature algorithms (SPHINCS+, LMS).
- WebAssembly (Wasm) client-side hardware execution acceleration.
- Visual step-by-step unrolling of SHA-256's 64 internal compression rounds.

---

## 13. References

1. **NIST FIPS PUB 180-4:** *Secure Hash Standard (SHS)*. National Institute of Standards and Technology, 2015.
2. **NIST FIPS PUB 202:** *SHA-3 Standard: Permutation-Based Hash and Extendable-Output Functions*. National Institute of Standards and Technology, 2015.
3. **Shannon, C. E.:** *Communication Theory of Secrecy Systems*. Bell System Technical Journal, 28(4), 656-715, 1949.
4. **Feistel, H.:** *Cryptography and Computer Privacy*. Scientific American, 228(5), 15-23, 1973.
5. **Webster, A. F., & Tavares, S. E.:** *On the design of S-boxes*. Advances in Cryptology — CRYPTO '85 Proceedings, 523-534, Springer, 1985.
6. **Biryukov, A., Dinu, D., & Khovratovich, D.:** *Argon2: New Generation of Memory-Hard Functions for Password Hashing and Other Applications*. IEEE European Symposium on Security and Privacy, 2016.

