# HashForge: User Guide & Laboratory Manual

Welcome to **HashForge**. This user guide walks you through every module in the laboratory to help you explore cryptographic hashing and the avalanche effect.

---

## 🚀 Quick Setup & Launch

1. Open PowerShell, Terminal, or Command Prompt inside the project directory:
   ```bash
   cd c:\Users\priyanshu\PROJECTS\HASHFORGE
   ```
2. Install requirements:
   ```bash
   python -m pip install -r requirements.txt
   ```
3. Run HashForge:
   ```bash
   python -m streamlit run app.py
   ```
4. HashForge will open in your default browser at `http://localhost:8501`.

---

## 📖 Laboratory Modules Walkthrough

### Module 1: Hash Generator
- **Goal:** Compute hashes of text, examine hexadecimal vs binary digests, and export reports.
- **Steps:**
  1. Navigate to **1_Hash_Generator** in the sidebar.
  2. Type any text into the text area or click **Sample NIST Vector**.
  3. Observe the live byte and bit counter.
  4. Switch between the **SHA-256** and **SHA3-256** tabs.
  5. Expand **View Formatted Hex & Raw Binary Digest** to view chunked outputs.
  6. Click **Download Cryptographic Digests** to save the results to a `.txt` file.

---

### Module 2: Algorithm Lab (SHA-256 vs SHA3-256)
- **Goal:** Compare Merkle-Damgård vs Sponge architectures and benchmark execution times.
- **Steps:**
  1. Open **2_Algorithm_Lab**.
  2. Enter a plaintext string.
  3. Compare the side-by-side SHA-256 and SHA3-256 cards.
  4. Notice the **Cross-Algorithm Divergence**: even for identical inputs, the two functions share ~50% bit divergence.
  5. Select benchmark iterations (e.g., 1,000) and click **Run Local Latency Benchmark** to measure microsecond-level CPU throughput.

---

### Module 3: Single-Bit Flip Experiment
- **Goal:** Invert exactly one input bit and visualize how ~50% of output bits flip.
- **Steps:**
  1. Open **3_Single_Bit_Experiment**.
  2. Enter baseline text (e.g., `HashForge`).
  3. Choose the algorithm (`SHA-256` or `SHA3-256`).
  4. Move the bit slider to pick an index (e.g. `0` for the MSB of Byte 0).
  5. Inspect the **Input Byte & Bit Inspection** panels to see the inverted bit.
  6. Review the **Hamming Distance** and **Avalanche Percentage**.
  7. In the **256-Bit Output Diffusion Visualizer**, hover over the **glowing amber bits** to inspect which bits changed.

---

### Module 4: Multi-Bit Flip Experiment
- **Goal:** Perturb multiple distinct input bits simultaneously.
- **Steps:**
  1. Open **4_Multi_Bit_Experiment**.
  2. Choose **Random Bit Sampling** or **Manual Bit Specification**.
  3. If random, choose $k$ bits to flip and toggle deterministic RNG seed.
  4. If manual, enter comma-separated indices (e.g. `0, 8, 16`).
  5. Examine whether flipping 10 bits produces a higher avalanche than flipping 1 bit (answer: diffusion remains centered near 50%).

---

### Module 5: Avalanche Analyzer (Monte Carlo Lab)
- **Goal:** Run statistical simulations to verify the binomial distribution around 50%.
- **Steps:**
  1. Open **5_Avalanche_Analyzer**.
  2. Choose a sample size: 10, 50, 100, or custom trials (up to 500).
  3. Choose **Independent Flips (Standard SAC)** or **Cumulative Mutation**.
  4. Click **Run Monte Carlo Avalanche Simulation**.
  5. Inspect the **Mean Avalanche**, **Standard Deviation**, and **Min/Max**.
  6. View the interactive **Histogram**, **Trial Timeline**, and **Boxplot**.
  7. Download the complete dataset as a CSV file.

---

### Module 6: File Integrity Lab
- **Goal:** Detect single-byte tampering in files and verify vendor checksums.
- **Scenarios:**
  - **Single File Fingerprinting:** Upload any file up to 50MB to view its SHA-256 and SHA3-256 checksums.
  - **Two-File Comparison:** Upload two versions of a document to check for bit alterations.
  - **Vendor Reference Hash:** Paste an expected checksum (e.g., from an ISO or release manifest) and upload a file to confirm authenticity.

---

### Module 7: Learning Center & Cryptography Quiz
- **Goal:** Master core cryptography concepts and evaluate your knowledge.
- **Steps:**
  1. Open **7_Learning_Center**.
  2. Read through the 12 curriculum expanders (including why SHA-256 is not suitable for passwords).
  3. Switch to the **Interactive Knowledge Check Quiz** tab.
  4. Answer all 10 questions and click **Submit Quiz & Calculate Score** to view detailed explanations and your grade.

