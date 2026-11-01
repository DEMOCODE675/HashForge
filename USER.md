# HashForge: User Guide & Laboratory Manual

Welcome to **HashForge**, an interactive cryptographic laboratory designed to explore, benchmark, and visualize the inner workings of modern cryptographic hash functions and the **Avalanche Effect** (Strict Avalanche Criterion - SAC).

Whether you are a computer science student, security researcher, software engineer, or curious developer, this guide provides complete instructions on how to run HashForge, navigate every laboratory module, interpret scientific outcomes, and use the platform on desktop or mobile devices.

---

## Table of Contents
1. [Overview & Core Philosophy](#1-overview--core-philosophy)
2. [Quick Start: How to Run HashForge](#2-quick-start-how-to-run-hashforge)
   - [Option A: Running Locally (Development Mode)](#option-a-running-locally-development-mode)
   - [Option B: Using Docker](#option-b-using-docker)
   - [Option C: Live Cloud Deployment](#option-c-live-cloud-deployment)
3. [Laboratory Modules Walkthrough & Expected Outcomes](#3-laboratory-modules-walkthrough--expected-outcomes)
   - [Module 1: Hash Generator Laboratory](#module-1-hash-generator-laboratory)
   - [Module 2: Algorithm Comparison Lab](#module-2-algorithm-comparison-lab)
   - [Module 3: Single-Bit Inversion Experiment](#module-3-single-bit-inversion-experiment)
   - [Module 4: Multi-Bit Perturbation Experiment](#module-4-multi-bit-perturbation-experiment)
   - [Module 5: Avalanche Statistical Analyzer](#module-5-avalanche-statistical-analyzer)
   - [Module 6: File Integrity Laboratory](#module-6-file-integrity-laboratory)
   - [Module 7: Learning Center & Evaluation Quiz](#module-7-learning-center--evaluation-quiz)
4. [Scientific Metrics Glossary & How to Interpret Results](#4-scientific-metrics-glossary--how-to-interpret-results)
5. [Mobile & Tablet Navigation Guide](#5-mobile--tablet-navigation-guide)
6. [Troubleshooting & FAQ](#6-troubleshooting--faq)

---

## 1. Overview & Core Philosophy

### What is HashForge?
A cryptographic hash function takes arbitrary-length input data (such as a string, code file, or document) and deterministically condenses it into a fixed-length string of bits (in our case, **256 bits** / 32 bytes / 64 hexadecimal characters).

### The Strict Avalanche Criterion (SAC)
In secure cryptographic hash algorithms:
$$\text{If a single input bit is flipped, each output bit must change with a probability of exactly } p = 0.5 \text{ (50\%)}$$

If flipping a bit changes only 2% or 95% of the output, an attacker could deduce relationships between plaintexts and ciphertext digests. Achieving approximately **50% diffusion** makes mathematical inversion computationally infeasible.

HashForge lets you witness, measure, and verify this mathematical phenomenon in real time across two NIST cryptographic standards:
- **SHA-256** (FIPS PUB 180-4, Merkle-Damgård iterative compression)
- **SHA3-256** (FIPS PUB 202, Keccak permutation-based sponge)

---

## 2. Quick Start: How to Run HashForge

### Option A: Running Locally (Development Mode)

#### Prerequisites
- **Python 3.11 or 3.12** installed
- **Node.js (v18+)** and **npm** installed
- **Git**

#### Step 1: Clone the Repository
```bash
git clone https://github.com/DEMOCODE675/HashForge.git
cd HashForge
```

#### Step 2: Start the FastAPI Backend
Open a terminal window:
```bash
# 1. Navigate to backend directory
cd backend

# 2. (Optional) Create a virtual environment
python -m venv .venv

# On Windows:
.venv\Scripts\activate
# On Linux / macOS:
source .venv/bin/activate

# 3. Install backend dependencies
pip install -r requirements.txt

# 4. Start the FastAPI server
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
- Verify the backend is live at: `http://127.0.0.1:8000/docs` (Interactive Swagger API documentation)
- Health check endpoint: `http://127.0.0.1:8000/api/health`

#### Step 3: Start the Vite + React Frontend
Open a second terminal window:
```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Start development server
npm run dev
```
- Open your browser to: `http://localhost:5173`

---

### Option B: Using Docker
If you have Docker and Docker Compose installed:
```bash
docker-compose up --build
```
- Web Application: `http://localhost:3000`
- API Backend: `http://localhost:8000`

---

### Option C: Live Cloud Deployment
If hosted on Vercel:
- Visit your live URL (e.g., `https://hashcrypto.vercel.app` or custom domain).
- The frontend and backend run together under Vercel Services routing.

---

## 3. Laboratory Modules Walkthrough & Expected Outcomes

### Module 1: Hash Generator Laboratory
- **What it does:** Calculates cryptographic digests for any plaintext in real time.
- **How to test:**
  1. Type or paste text into the input field (or click **"NIST Fox Vector"** to test `"The quick brown fox jumps over the lazy dog"`).
  2. Switch between **SHA-256** and **SHA3-256** tabs.
  3. Toggle format views between **Hex**, **Chunked (8-character blocks)**, and **Binary (256 individual bits)**.
  4. Click **Copy** or **Export** to save the generated digest.
- **Expected Outcome:**
  - Standard SHA-256 digest length: 64 hexadecimal characters (256 bits).
  - Empty string test: Computes valid FIPS hash vector `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
  - Byte and bit counters update dynamically as you type.

---

### Module 2: Algorithm Comparison Lab
- **What it does:** Performs architectural and performance comparisons between Merkle-Damgård (SHA-2) and Keccak Sponge (SHA-3).
- **How to test:**
  1. Enter a baseline plaintext string.
  2. Select benchmark iteration sample size (100, 500, 1,000, or 5,000 runs).
  3. Click **"Execute Comparison & Benchmark"**.
- **Expected Outcome:**
  - **Cross-Divergence:** Compares SHA-256 vs SHA3-256 digests on identical plaintext. You will see approximately **50% Hamming distance divergence** ($\approx 128$ differing bits), proving the two algorithms produce completely unrelated outputs.
  - **Microsecond Latency:** Shows execution time in microseconds ($\mu\text{s}$) per digest calculation.
  - **Architectural Specs:** Side-by-side breakdown of internal block size (512-bit Merkle-Damgård vs 1600-bit Keccak state matrix).

---

### Module 3: Single-Bit Inversion Experiment
- **What it does:** The core demonstration of the Avalanche Effect. Inverts exactly **one bit** in your input using bitwise XOR, then visualizes which output bits changed.
- **How to test:**
  1. Enter an input word (e.g., `"HashForge"`).
  2. Use the slider to pick which bit index to flip (e.g., Bit #0, which is the Most Significant Bit of Byte 0).
  3. Click **"Run Single-Bit Inversion"**.
  4. Look at the **Input Bitstream Viewer**: Notice the highlighted byte showing the exact single bit modified.
  5. Inspect the **256-Bit Cryptographic Output Grid**:
     - Glowing amber cells represent **Flipped Bits**.
     - Dark slate cells represent **Unchanged Bits**.
     - Tap or hover any cell to inspect its bit address, byte address, and flip status.
- **Expected Outcome:**
  - **Avalanche Percentage:** Typically ranges between **43% and 57%** (clustering tightly around **50.00%**).
  - **Hamming Distance:** Approximately **120 to 136 bits** out of 256 are inverted.
  - Changing just one microscopic bit produces a radically different, unrecognizable hash!

---

### Module 4: Multi-Bit Perturbation Experiment
- **What it does:** Perturbs multiple distinct bits simultaneously to examine whether multiple input flips cause "over-diffusion" or cancel each other out.
- **How to test:**
  - **Random Mode:** Choose $k$ bits (e.g., 4 or 8 bits) and set a deterministic seed (e.g., `42`), then click **"Run Multi-Bit Perturbation"**.
  - **Manual Mode:** Enter comma-separated bit indices (e.g., `0, 8, 16, 24`) to flip specific bits across multiple bytes.
- **Expected Outcome:**
  - Whether you flip 1 bit, 4 bits, or 16 bits, the output avalanche percentage remains stable around **50.00%**.
  - Proves that cryptographic hash diffusion reaches mathematical saturation instantaneously.

---

### Module 5: Avalanche Statistical Analyzer
- **What it does:** Executes automated Monte Carlo simulations (10, 50, 100, or 200 trials) to statistically evaluate diffusion across random single-bit perturbations.
- **How to test:**
  1. Set your baseline plaintext.
  2. Choose trial count (e.g., `50 Trials`).
  3. Select **"Compare SHA-2 & SHA-3"**.
  4. Click **"Execute Monte Carlo Simulation"**.
  5. Inspect the resulting:
     - **Statistical KPI Cards:** Mean Avalanche %, Standard Deviation ($\sigma$), Median, Min, and Max.
     - **Comparative Bar Charts:** Side-by-side metric comparison between SHA-256 and SHA3-256.
     - **Avalanche Histogram:** Gaussian bell curve centered at 50%.
     - **Trial Timeline Scatter Plot:** Fluctuation of each trial around the theoretical 50% dashed reference line.
     - **Trial Records Table:** Sortable log with an **"Export CSV"** button.
- **Expected Outcome:**
  - As trial count increases ($N \ge 50$), the mean avalanche percentage converges closer to **50.00%**, and standard deviation shrinks, demonstrating the **Central Limit Theorem** in action.

---

### Module 6: File Integrity Laboratory
- **What it does:** Demonstrates file tampering detection and vendor checksum verification using streaming 64KB buffers.
- **How to test:**
  - **Single File Fingerprint:** Drag and drop any document or image. View its SHA-256 and SHA3-256 checksums, chunk count, and processing duration.
  - **Two-File Parity Comparison:** Select File A (original) and File B (modified). Even changing a single character in a text file results in a bold red **"TAMPERING DETECTED"** banner. If files are identical, a green **"INTEGRITY VERIFIED"** banner appears.
  - **Vendor Reference Hash:** Select a downloaded file and paste an official vendor checksum (e.g., from Ubuntu, Python, or Apache) to verify file authenticity.
- **Expected Outcome:**
  - Validates zero-byte corruption resistance.
  - Files are streamed chunk-by-chunk in volatile memory without leaking memory or storing user files to disk.

---

### Module 7: Learning Center & Evaluation Quiz
- **What it does:** Comprehensive educational curriculum and self-evaluation tool.
- **Curriculum:** 12 interactive topics covering:
  1. Cryptographic Hash Foundations
  2. The Strict Avalanche Criterion (SAC)
  3. Merkle-Damgård Iterative Construction
  4. Keccak Permutation & Sponge Engine
  5. Collision Resistance & Birthday Paradox
  6. Pre-Image & Second Pre-Image Resistance
  7. Hamming Distance in Cryptanalysis
  8. Cryptographic Pseudorandomness
  9. File Integrity & Digital Signatures
  10. Blockchain Merkle Trees & State Roots
  11. Quantum Computing Impact (Grover's Algorithm)
  12. Password Hashing (Why Argon2/bcrypt is used instead of raw SHA-256)
- **Knowledge Quiz:** 10 scenario-based questions with instant grading, score calculation, and detailed technical answer explanations.

---

## 4. Scientific Metrics Glossary & How to Interpret Results

| Metric | Scientific Definition | Ideal Cryptographic Target | Meaning if Divergent |
| :--- | :--- | :--- | :--- |
| **Hamming Distance** | Count of bit positions in which two binary sequences differ: $d_H(x, y) = \sum (x_i \oplus y_i)$ | **128 Bits** (out of 256) | $< 100$ or $> 156$ indicates non-uniform diffusion in an individual trial. |
| **Avalanche Percentage** | $\frac{\text{Hamming Distance}}{256} \times 100\%$ | **50.00%** | Average over multiple trials should cluster at 50%. |
| **Standard Deviation ($\sigma$)** | Measure of dispersion of avalanche percentages around the mean across $N$ trials. | **$\approx 2.5\% - 3.5\%$** | Very low dispersion confirms predictable binomial distribution. |
| **Cross-Divergence** | Hamming distance between SHA-256 and SHA3-256 digests of the same plaintext. | **$\approx 50.00\%$** | Confirms independence of Merkle-Damgård and Keccak algorithms. |
| **Latency ($\mu\text{s}$)** | Mean computation time per hash in microseconds. | **Platform dependent** | Variations reflect CPU hardware instructions (e.g. SHA extensions vs ALU operations). |

---

## 5. Mobile & Tablet Navigation Guide

HashForge is engineered with a mobile-first, responsive interface:
- **Mobile Drawer:** On phone screens ($< 1024\text{px}$), tap the top-left **Hamburger Menu Icon** to open the navigation drawer. Tap any module to jump directly to it; the drawer will close automatically. Tap the dark backdrop or the close button (**X**) to dismiss.
- **256-Bit Grid on Mobile:** An 8-row by 32-column grid requires horizontal space. On mobile, the grid features **smooth touch scrolling (`touch-pan-x`)** with **sticky row headers** (`Bits 000–031`), ensuring you never lose your row context while swiping left and right.
- **Tap to Inspect:** Tap any individual bit on touch screens to inspect its exact bit index, byte address, and flip status in the live detail banner below the grid.
- **Touch-Friendly Controls:** All buttons, dropdowns, and quiz options provide a minimum **44px touch target** to prevent accidental mis-taps.

---

## 6. Troubleshooting & FAQ

#### Q: Why does the top header show "API Offline"?
- Ensure the backend FastAPI server is running (`http://127.0.0.1:8000/api/health`).
- If running on Vercel, verify that your Vercel deployment completed successfully and that Python 3.12 runtime is selected in `.python-version`.

#### Q: Why did flipping one bit change 131 bits instead of exactly 128?
- Each bit flip behaves like an independent fair coin toss ($p = 0.5$). For 256 independent trials, the binomial distribution has a standard deviation of $\sigma = \sqrt{256 \times 0.5 \times 0.5} = 8$ bits. Therefore, Hamming distances between **120 and 136 bits** are normal and expected!

#### Q: Can I use raw SHA-256 for storing user passwords?
- **No.** As explained in Module 7, SHA-256 is designed to be extremely fast. Attackers can test billions of SHA-256 guesses per second using GPUs. Always use **Argon2id**, **bcrypt**, or **scrypt** for passwords.
