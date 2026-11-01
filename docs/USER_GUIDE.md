# HashForge: User Guide & Laboratory Manual

Welcome to **HashForge**, an interactive educational laboratory for cryptographic hashing and avalanche effect analysis. This guide covers setup, navigation, and practical exercises across the full-stack React and FastAPI platform.

---

## 1. Quick Setup & Launch

### 1.1 Prerequisites
- **Python 3.11+** (tested with Python 3.13)
- **Node.js 18+** with `npm` (tested with Node.js 20+)
- Modern web browser (Chrome, Firefox, Edge, Safari)

### 1.2 Running the Application

The application consists of a FastAPI backend and a React 19 Single Page Application.

#### Step 1: Start the FastAPI Backend
Open a terminal in the project root:
```powershell
cd c:\Users\priyanshu\PROJECTS\HASHFORGE
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
The backend API server will start at `http://127.0.0.1:8000`. You can inspect interactive OpenAPI documentation at `http://127.0.0.1:8000/docs`.

#### Step 2: Start the React Frontend
Open a second terminal window:
```powershell
cd c:\Users\priyanshu\PROJECTS\HASHFORGE\frontend
npm run dev
```
The Vite development server will start at `http://localhost:5173`. Open this URL in your web browser.

---

## 2. Laboratory Modules Walkthrough

### Module 1: Hash Generator
- **Objective:** Compute hashes of text, examine hexadecimal vs binary digests, and export reports.
- **How to Use:**
  1. Navigate to **Hash Generator** in the sidebar.
  2. Enter plain text into the input field or click **Sample NIST Vector** to load a standardized test string.
  3. Observe the live byte and bit counter update in real time.
  4. Switch between the **SHA-256** and **SHA3-256** tabs.
  5. Expand the **Formatted Hex & Raw Binary Digest** accordion to view chunked outputs with 8-character groupings.
  6. Click **Copy** to copy the hex or binary string to your clipboard.
  7. Click **Export Report** to download the cryptographic digest summary as a text file.

---

### Module 2: Algorithm Lab (SHA-256 vs SHA3-256)
- **Objective:** Compare the Merkle-Damgård iterative compression of SHA-256 against the Keccak Sponge permutation of SHA3-256.
- **How to Use:**
  1. Open **Algorithm Lab**.
  2. Enter input text to generate side-by-side SHA-256 and SHA3-256 digests.
  3. Examine the **Cross-Algorithm Divergence Metric**: even for identical inputs, the two algorithms exhibit independent hash output with ~50% bit divergence.
  4. Select a benchmark iteration count (100, 500, 1,000, or 5,000 iterations).
  5. Click **Run Latency Benchmark** to measure microsecond-level CPU throughput and compare execution speeds.
  6. Review the comparative architecture table detailing block sizes, internal states, and collision resistance bounds.

---

### Module 3: Single-Bit Flip Experiment
- **Objective:** Invert exactly one input bit and observe the cascading avalanche effect across the 256 output bits.
- **How to Use:**
  1. Open **Single-Bit Experiment**.
  2. Enter baseline text (e.g., `HashForge Cryptography Lab`).
  3. Select the target hash algorithm (`SHA-256` or `SHA3-256`).
  4. Adjust the **Bit Index Slider** to target any bit $k \in [0, 8N - 1]$. Note that bit 0 represents the Most Significant Bit (MSB) of Byte 0.
  5. Inspect the **Input Byte & Bit Inspection** panel to view the exact byte index, bit offset, and modified ASCII character.
  6. Review the resulting **Hamming Distance** and **Avalanche Percentage**.
  7. In the **256-Bit Output Diffusion Visualizer**, examine the 8-row by 32-bit grid:
     - Unchanged bits are rendered in subtle dark gray.
     - Changed bits glow in amber with clear visual contrast.
     - Hover over any bit cell to inspect its bit position (0 to 255), original value, modified value, and flip state.

---

### Module 4: Multi-Bit Flip Experiment
- **Objective:** Perturb multiple distinct input bits simultaneously and investigate non-linear saturation.
- **How to Use:**
  1. Open **Multi-Bit Experiment**.
  2. Choose either **Random Bit Sampling** or **Manual Bit Specification**:
     - In **Random Mode**, choose the number of bits to flip ($k$) and optionally set an RNG seed for reproducible experiments.
     - In **Manual Mode**, enter a comma-separated list of bit indices (e.g., `0, 8, 16, 24`).
  3. Click **Execute Multi-Bit Experiment**.
  4. Compare the baseline hash against the perturbed hash.
  5. Note the key pedagogical takeaway: flipping 10 or 20 bits does not double the avalanche percentage; the output remains statistically centered near 50%, demonstrating rapid cryptographic saturation.

---

### Module 5: Avalanche Analyzer (Monte Carlo Lab)
- **Objective:** Execute statistical simulations to verify the empirical binomial distribution around 50% ($128$ bits).
- **How to Use:**
  1. Open **Avalanche Analyzer**.
  2. Select a trial count: 10, 50, 100, or custom (up to 500 trials).
  3. Select a trial mode:
     - **Independent Flips (Strict Avalanche Criterion):** Each trial flips a random bit in the original baseline text.
     - **Cumulative Mutation:** Each trial mutates the text from the previous trial sequentially.
  4. Click **Run Monte Carlo Simulation**.
  5. Inspect statistical summary metrics:
     - **Mean Avalanche Percentage:** Typically $49.5\% - 50.5\%$.
     - **Standard Deviation:** Approximately $3.1\%$, closely matching theoretical prediction $\sigma = \sqrt{256 \times 0.25} / 256 \approx 3.125\%$.
     - **Minimum & Maximum Avalanche:** Observed extremes across the trial run.
  6. Analyze interactive Recharts visualizations:
     - **Frequency Histogram:** Shows empirical trial distribution against the theoretical 50% normal curve.
     - **Trial Timeline Scatter Plot:** Displays individual trial data points and deviation from the mean.
  7. Click **Export CSV** to download the complete trial dataset for further analysis in spreadsheet or data science tools.

---

### Module 6: File Integrity Lab
- **Objective:** Detect single-byte tampering in files and verify vendor checksums using memory-efficient streaming hashing.
- **Workflows:**
  - **Single File Fingerprinting:** Upload any file to compute its SHA-256 and SHA3-256 fingerprints in 64KB streaming chunks.
  - **Two-File Comparison:** Upload an original file and a suspect file. HashForge performs a byte-by-byte comparison, flags any parity mismatches, and displays the differing hashes.
  - **Vendor Reference Checksum Validation:** Paste an official SHA-256 checksum from a software publisher and upload a downloaded file to verify cryptographic authenticity.

---

### Module 7: Learning Center & Knowledge Evaluation
- **Objective:** Study cryptographic theory and test comprehension through an interactive quiz.
- **Features:**
  1. **Curriculum Modules:** Read through 12 structured topics covering hash fundamentals, the Strict Avalanche Criterion, Merkle-Damgård vs Sponge constructions, pre-image resistance, collision resistance, blockchain Merkle trees, software supply chain security, and why general-purpose hashes must not be used for password hashing.
  2. **Evaluation Quiz:** Take the 10-question evaluation quiz covering practical and theoretical concepts. Click **Submit Quiz** to receive an immediate grade, status badges, and detailed answer explanations.

---

## 3. Running Automated Tests

### 3.1 Backend Tests (Pytest)
```powershell
cd c:\Users\priyanshu\PROJECTS\HASHFORGE
python -m pytest tests/ -v
```
Verifies all 70 Python test cases across the core cryptographic engine and the FastAPI REST routes.

### 3.2 Frontend Tests (Vitest)
```powershell
cd c:\Users\priyanshu\PROJECTS\HASHFORGE\frontend
npm run test
```
Executes all 10 React component tests, verifying bit grid rendering, hash formatting, and zero-emoji compliance.

### 3.3 Production Frontend Build
```powershell
cd c:\Users\priyanshu\PROJECTS\HASHFORGE\frontend
npm run build
```
Typechecks TypeScript and builds optimized production assets in `frontend/dist/`.
