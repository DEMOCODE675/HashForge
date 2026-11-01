# 🛡️ HashForge — Enterprise Cryptography Laboratory

> **An Interactive Cryptographic Hashing and Avalanche Effect Visualization Laboratory Using SHA-256 and SHA3-256**  
> *Modern Full-Stack Architecture: React 19 • TypeScript • Tailwind CSS • Lucide React • Recharts • FastAPI • Python 3.13*

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![React 19](https://img.shields.io/badge/Frontend-React%2019-61DAFB.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0%2B-3178C6.svg)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Styling-Tailwind%20CSS-38B2AC.svg)](https://tailwindcss.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python Tests: 70 Passed](https://img.shields.io/badge/Pytest-70%20Passed%20(100%25)-brightgreen.svg)](tests/)
[![Frontend Tests: 10 Passed](https://img.shields.io/badge/Vitest-10%20Passed%20(100%25)-brightgreen.svg)](frontend/)

---

## 📌 Executive Summary

**HashForge** is a modern, high-performance cybersecurity web application engineered to demonstrate the **Strict Avalanche Criterion (SAC)**, bit perturbation mechanics, and data integrity verification using **SHA-256** (FIPS 180-4) and **SHA3-256** (FIPS 202).

It replaces static command-line digests with an interactive visual laboratory inspired by developer tools like Linear, Vercel, and Raycast.

### Strict Design System Highlights:
- **Zero Emojis in UI:** Navigation, status indicators, and actions are rendered as semantic SVG components from **Lucide React**.
- **Dark-First Cybersecurity Palette:**
  - Main Canvas: `#0B0F17`
  - Sidebar: `#0D1420`
  - Content Cards: `#111827`
  - Elevated Surfaces: `#172033`
  - Subtle Borders: `#253247`
  - Accent Cyan: `#00D6C9`
  - Accent Emerald: `#10B981`
  - Warning Amber: `#F59E0B`
  - Error Rose: `#EF4444`
- **Big-Endian / Network Bit Indexing:** Strictly standardizes on network bit order ($i = \lfloor k/8 \rfloor$, $b = 7 - (k \bmod 8)$), where bit 0 is the Most Significant Bit (MSB, weight 128) of Byte 0, inverted via exact bitwise XOR (`byte ^ (1 << b)`).
- **100% Local Cryptography:** All cryptographic computations execute via standard library `hashlib` C-bindings without external network dependencies or synthetic data.

---

## 🔬 Laboratory Modules

| Module | Purpose | Key Capabilities |
|---|---|---|
| **Dashboard** | Overview & Quick Test | High-level metrics, system architecture summary, quick SHA-256 calculation widget. |
| **Module 1: Hash Generator** | Primary Hashing | Real-time dual SHA-256 & SHA3-256 computation, live byte and bit counts, chunked hex view, raw binary view, copy helper, and `.txt` file export. |
| **Module 2: Algorithm Lab** | Architecture Comparison | Merkle-Damgård vs Keccak Sponge comparison, cross-algorithm Hamming divergence, and local multi-iteration latency benchmarks (µs precision). |
| **Module 3: Single-Bit Experiment** | Diffusion Visualization | Invert exactly 1 input bit ($0 \le k < 8N$) and visualize the cascade across the **256-bit organized grid** with glowing amber highlights for flipped bits. |
| **Module 4: Multi-Bit Experiment** | Saturation Analysis | Perturb $k$ bits simultaneously using pseudo-random sampling (with reproducible seed) or manual bit specification. |
| **Module 5: Avalanche Analyzer** | Monte Carlo Lab | 10 to 500-trial statistical simulations with Recharts histograms, trial dispersion scatter lines, boxplots, and complete CSV report export. |
| **Module 6: File Integrity Lab** | Streaming Verification | Memory-safe 64KB streaming file hashing, single-byte tamper detection, and vendor reference hash validation. |
| **Module 7: Learning Center** | Curriculum & Evaluation | 12 structured curriculum topics (including why SHA-256 is not for password storage) and an interactive 10-question evaluation quiz with instant grading. |

---

## 🏗️ System Architecture

```
HashForge/
├── backend/                    # Python FastAPI REST Service
│   ├── main.py                 # FastAPI Application & CORS configuration
│   ├── requirements.txt        # Backend dependencies
│   └── api/
│       ├── schemas/            # Strict Pydantic v2 validation models
│       │   ├── hash_schemas.py
│       │   ├── experiment_schemas.py
│       │   ├── avalanche_schemas.py
│       │   └── file_schemas.py
│       └── routes/             # REST Route Handlers
│           ├── hash_routes.py
│           ├── experiment_routes.py
│           ├── avalanche_routes.py
│           ├── file_routes.py
│           └── health_routes.py
│
├── frontend/                   # Modern React 19 SPA (Vite + TypeScript)
│   ├── package.json
│   ├── vite.config.ts          # Vite & Vitest configuration with /api proxy
│   ├── tailwind.config.js      # Custom cybersecurity design tokens
│   └── src/
│       ├── types/              # TypeScript API & Domain Interfaces
│       ├── services/           # Typed API Client (fetch with error mapping)
│       ├── components/
│       │   ├── layout/         # AppShell, Sidebar, TopHeader
│       │   ├── binary/         # BitGrid256, BinaryStreamViewer
│       │   ├── charts/         # AvalancheHistogram, TrialTimelineChart, AlgorithmComparisonBox
│       │   └── shared/         # MetricCard, HashBox, StatusBadge
│       ├── pages/              # 8 Module Views (Dashboard + Modules 1–7)
│       └── test/               # Vitest & Testing Library Test Suite
│
├── core/                       # Preserved Cryptographic Core (UI-free)
│   ├── hash_engine.py          # SHA-256 & SHA3-256 wrappers
│   ├── bit_operations.py       # Big-Endian XOR manipulation
│   ├── avalanche.py            # Hamming distance & SAC formulas
│   ├── experiments.py          # Monte Carlo trial runners
│   ├── file_integrity.py       # 64KB chunked streaming file hashing
│   └── validators.py           # Bounds and type guardrails
│
├── tests/                      # Automated Pytest Suite (70 Tests)
│   ├── test_backend_api.py     # FastAPI endpoint integration tests
│   ├── test_hash_engine.py     # NIST standard test vectors
│   ├── test_bit_operations.py  # Bit boundary & XOR verification
│   ├── test_avalanche.py       # Distance formulas & SAC bounds
│   ├── test_experiments.py     # Seed reproducibility & baseline resets
│   ├── test_file_integrity.py  # Streaming chunks & tamper detection
│   └── test_validators.py      # Guardrails & exception handling
│
├── docs/                       # Academic & Technical Documentation
│   ├── PROJECT_REPORT.md       # 13-section academic project report
│   ├── ARCHITECTURE.md         # Full-stack architectural specification
│   ├── USER_GUIDE.md           # Step-by-step user manual
│   └── TESTING.md              # Quality assurance & test matrix
└── DEVELOPMENT_PROGRESS.md     # Milestone tracking log
```

---

## ⚡ Quick Start

### 1. Prerequisites
- **Python:** 3.11 or newer (tested on Python 3.13)
- **Node.js:** 18 or newer (tested on Node v24.18)

---

### 2. Start the Backend API (FastAPI)
```powershell
# In root directory:
python -m pip install -r requirements.txt
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
The REST API will be accessible at:
- **API Base:** `http://127.0.0.1:8000`
- **Interactive Swagger Docs:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

---

### 3. Start the Frontend (React + Vite)
In a new terminal window:
```powershell
cd frontend
npm install
npm run dev
```
Open **`http://localhost:5173`** in your browser.

---

## 🧪 Automated Testing

### 1. Python Backend & Core Engine (Pytest)
```powershell
python -m pytest tests/ -v
```
**70 passed in 1.95s (100% success rate)**:
- 17 FastAPI REST endpoint integration tests (`test_backend_api.py`)
- 12 NIST standard vector tests (`test_hash_engine.py`)
- 13 Bit-boundary & XOR tests (`test_bit_operations.py`)
- 8 Hamming distance & SAC tests (`test_avalanche.py`)
- 4 Monte Carlo simulation tests (`test_experiments.py`)
- 6 Streaming file integrity tests (`test_file_integrity.py`)
- 10 Input validation guardrail tests (`test_validators.py`)

### 2. Frontend Test Suite (Vitest)
```powershell
cd frontend
npm run test
```
**10 passed (100% success rate)**:
- `Navigation.test.tsx`: Route switching, zero-emoji verification, sidebar controls.
- `BitGrid256.test.tsx`: 256-bit matrix rendering, row labels, flipped vs unchanged counts.
- `HashBox.test.tsx`: Chunked view toggling, hex rendering, clipboard copying.

### 3. TypeScript Compilation & Production Build
```powershell
cd frontend
npm run typecheck
npm run build
```
Build output: `dist/index.html` (0.90 kB), `dist/assets/index.js` (built in 4.06s).

---

## 📄 License & Attribution

HashForge is open-source software licensed under the **MIT License**. See [LICENSE](LICENSE) for details.
Designed for university presentations, cybersecurity coursework, and cryptographic research demonstrations.
