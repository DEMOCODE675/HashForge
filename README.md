# 🛡️ HashForge

> **An Interactive Cryptographic Hashing and Avalanche Effect Visualization Laboratory Using SHA-256 and SHA3-256**

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red.svg)](https://streamlit.io/)
[![Cryptography: FIPS](https://img.shields.io/badge/Cryptography-FIPS%20180--4%20%2F%20FIPS%20202-green.svg)](https://csrc.nist.gov/)
[![Tests: Pytest](https://img.shields.io/badge/Tests-53%20Passed%20(100%25)-brightgreen.svg)](tests/)

---

## 📌 Executive Summary & Problem Statement

In academic computer science and cybersecurity education, students frequently master the abstract definitions of cryptographic hashing—preimage resistance, second preimage resistance, and collision resistance—yet struggle to visualize the **Strict Avalanche Criterion (SAC)**.

The core cognitive hurdle is intuitive: *How does flipping a single microscopic bit (or even 1 in 10,000 bits) in an input string cause approximately 50% of the output bits to flip in an entirely pseudo-random, uncorrelated cascade?*

**HashForge** was built to solve this problem. It provides an interactive laboratory for exploring, testing, and visualizing the cryptographic avalanche effect and data integrity behaviors of two foundational standards:
- **SHA-256** (FIPS 180-4, Merkle-Damgård iterative compression)
- **SHA3-256** (FIPS 202, Keccak Permutation-based Sponge construction)

> **Academic Disclaimer:** HashForge is an educational laboratory designed for university coursework, cybersecurity training, and research demonstrations. It uses standard FIPS implementations from Python's standard `hashlib` library and does not invent proprietary cryptographic algorithms.

---

## 🔬 Core Features & Laboratory Modules

| Module | Name | Capability |
|---|---|---|
| **Module 1** | **Hash Generator** | Live dual SHA-256 and SHA3-256 computation, live byte counters, chunked hexadecimal breakdown, raw 256-bit binary, and text export. |
| **Module 2** | **Algorithm Lab** | Side-by-side comparison of Merkle-Damgård vs Keccak Sponge architectures, cross-algorithm Hamming distance, and multi-iteration execution benchmarks. |
| **Module 3** | **Single-Bit Flip Lab** | Interactive single-bit XOR perturbation ($0 \le k < 8N$) with 256-bit color-coded visualizer showing glowing changed bits. |
| **Module 4** | **Multi-Bit Flip Lab** | Perturb $k$ distinct bit positions simultaneously via pseudo-random sampling (with reproducible seed) or manual index entry. |
| **Module 5** | **Avalanche Analyzer** | 10 to 500-trial Monte Carlo simulations with interactive Plotly histograms, trial-by-trial scatter lines, standard deviation, and CSV export. |
| **Module 6** | **File Integrity Lab** | Streaming 64KB chunk-based file hashing (up to 50MB), single-byte tamper detection, and vendor reference checksum verification. |
| **Module 7** | **Learning Center** | 12 structured curriculum modules, real-world blockchain & supply chain case studies, and an interactive 10-question evaluation quiz. |

---

## 📐 Mathematical Foundations

### 1. Big-Endian / Network Bit Indexing
HashForge strictly standardizes on network bit order:
$$\text{Byte Index } i = \lfloor k / 8 \rfloor, \quad \text{Bit Offset } b = 7 - (k \bmod 8)$$
- **Bit 0**: Most Significant Bit (MSB, $2^7 = 128$) of Byte 0.
- **Bit 7**: Least Significant Bit (LSB, $2^0 = 1$) of Byte 0.
- **Bit Inversion**: Executed via exact bitwise XOR: `byte ^ (1 << b)`.

### 2. Hamming Distance
The distance $D(H_1, H_2)$ counts differing positions between two binary sequences of equal length $n = 256$:
$$D(H_1, H_2) = \sum_{j=0}^{n-1} (H_1[j] \oplus H_2[j])$$

### 3. Avalanche Effect Percentage
$$\text{Avalanche } \% = \left(\frac{D(H_1, H_2)}{256}\right) \times 100\%$$
- **Ideal Diffusion (SAC):** $\mathbb{E}[D] = 128 \text{ bits } (50.00\%)$.

---

## 🏗️ System Architecture

```
HashForge/
├── app.py                      # Main Home Dashboard & Platform Router
├── requirements.txt            # Minimal verified dependencies
├── LICENSE                     # MIT License
├── README.md                   # Repository Guide
├── DEVELOPMENT_PROGRESS.md     # Development & Phase Milestone Log
├── .streamlit/
│   └── config.toml             # Dark cybersecurity theme configuration
├── core/                       # Cryptographic & Mathematical Engine (UI-free)
│   ├── __init__.py
│   ├── hash_engine.py          # FIPS SHA-256 and SHA3-256 wrappers & timing
│   ├── bit_operations.py       # Big-endian bit manipulation & XOR perturbation
│   ├── avalanche.py            # Hamming distance & avalanche formulas
│   ├── experiments.py          # Monte Carlo simulation & trial runners
│   ├── file_integrity.py       # 64KB chunked streaming file hashing
│   └── validators.py           # Input sanitization and bounds checking
├── components/                 # Presentation & Visualization Layer
│   ├── __init__.py
│   ├── sidebar.py              # Navigation and CSS injector
│   ├── metric_cards.py         # Visual stat cards
│   ├── bit_visualizer.py       # 256-bit grid with changed-bit highlighting
│   ├── hash_display.py         # Formatted hex & binary cards
│   ├── comparison.py           # Side-by-side diff widgets
│   └── charts.py               # Plotly interactive histograms & dispersion lines
├── pages/                      # Multi-Page Streamlit Laboratory Modules
│   ├── 1_Hash_Generator.py
│   ├── 2_Algorithm_Lab.py
│   ├── 3_Single_Bit_Experiment.py
│   ├── 4_Multi_Bit_Experiment.py
│   ├── 5_Avalanche_Analyzer.py
│   ├── 6_File_Integrity.py
│   └── 7_Learning_Center.py
├── tests/                      # Automated Pytest Suite
│   ├── test_hash_engine.py     # NIST test vectors & behavioral tests
│   ├── test_bit_operations.py  # Bit boundaries & XOR verification
│   ├── test_avalanche.py       # Distance formulas & diff masks
│   ├── test_experiments.py     # Reproducible seeded simulations
│   ├── test_file_integrity.py  # Streaming chunks & tamper detection
│   └── test_validators.py      # Input validation & boundary guardrails
├── assets/
│   ├── logo.svg                # Vector cryptographic anvil/block logo
│   └── custom.css              # Cyberpunk dark theme stylesheet
└── docs/
    ├── PROJECT_REPORT.md       # Comprehensive academic project report
    ├── ARCHITECTURE.md         # Detailed architectural specification
    ├── USER_GUIDE.md           # Step-by-step user manual
    └── TESTING.md              # QA test matrix & verification report
```

---

## ⚡ Quick Start

### 1. Prerequisites
- Python 3.11 or newer (tested on Python 3.13)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### 2. Clone & Setup Environment
```bash
git clone https://github.com/your-username/HashForge.git
cd HashForge

# Create and activate virtual environment (optional but recommended)
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies
python -m pip install -r requirements.txt
```

### 3. Launch the Application
```bash
python -m streamlit run app.py
```
Open your browser to `http://localhost:8501`.

---

## 🧪 Automated Testing

HashForge includes a rigorous 53-test automated test suite validating NIST standard test vectors, bit boundaries, and statistical distributions:

```bash
# Run full test suite with verbose output
python -m pytest tests/ -v
```

### Test Suite Summary:
```
============================= 53 passed in 0.37s ==============================
- tests/test_hash_engine.py:      12 passed (NIST vectors for "", "abc", fox)
- tests/test_bit_operations.py:   13 passed (MSB, LSB, middle, multi-flip)
- tests/test_avalanche.py:         8 passed (Hamming distance, SAC bounds)
- tests/test_experiments.py:       4 passed (Monte Carlo seed reproducibility)
- tests/test_file_integrity.py:    6 passed (Streaming chunking, tamper flags)
- tests/test_validators.py:       10 passed (Guardrails, bounds, type checks)
```

---

## 🛡️ Security & Performance Guardrails

- **Zero Remote Dependencies:** All cryptographic computations run 100% locally on your CPU. No data is sent to external APIs or cloud servers.
- **Streaming Hashing:** File uploads are hashed via streaming 64KB buffers (`hashlib.update()`), never buffering multi-gigabyte files into RAM.
- **Safe Memory Processing:** Uploaded files exist only in volatile runtime memory during hashing and are never persisted to disk.
- **Password Storage Disclaimer:** The platform explicitly teaches why high-throughput general hashes (SHA-256) are vulnerable to GPU brute-forcing and demonstrates why memory-hard KDFs (Argon2id, bcrypt, scrypt) are required for passwords.

---

## 📄 License & Attribution

This project is released under the **MIT License**. See [LICENSE](LICENSE) for details.
Built for university demonstrations, open-source education, and cryptographic experimentation.

