# Contributing to HashForge

Thank you for your interest in contributing to **HashForge**! We welcome bug reports, feature enhancements, documentation improvements, and cryptographic research extensions.

---

## 1. How to Fork and Contribute (Standard Workflow)

Any GitHub user can contribute to HashForge through the open-source **Fork & Pull Request** workflow:

### Step 1: Fork the Repository on GitHub
1. Navigate to the official HashForge repository: [https://github.com/DEMOCODE675/HashForge](https://github.com/DEMOCODE675/HashForge)
2. In the top-right corner, click the **"Fork"** button.
3. Choose your personal GitHub account as the destination and click **"Create fork"**.
4. You now have your own independent copy at `https://github.com/<your-username>/HashForge`.

### Step 2: Clone Your Fork Locally
Open your terminal and clone your personal fork:
```bash
git clone https://github.com/<your-username>/HashForge.git
cd HashForge
```

### Step 3: Configure Upstream Remote
To keep your fork synchronized with the original project:
```bash
git remote add upstream https://github.com/DEMOCODE675/HashForge.git
git remote -v
```

### Step 4: Create a New Feature Branch
Always develop inside a dedicated branch rather than `main`:
```bash
git checkout -b feature/my-new-feature
```

### Step 5: Set Up the Development Environment

#### Backend (FastAPI + Python 3.12)
```bash
cd backend
python -m venv .venv

# On Windows:
.venv\Scripts\activate
# On macOS / Linux:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

#### Frontend (Vite + React 19 + TypeScript)
In a separate terminal:
```bash
cd frontend
npm install
npm run dev
```

### Step 6: Run Automated Tests
Before committing, verify that all test suites pass:

```bash
# 1. Run all 70 Python cryptographic tests
python -m pytest tests/ -q

# 2. Run TypeScript typecheck
npm --prefix frontend run typecheck

# 3. Run all 10 Vitest frontend component tests
npm --prefix frontend run test

# 4. Run Vite production build test
npm --prefix frontend run build
```

### Step 7: Commit and Push Changes to Your Fork
```bash
git add .
git commit -m "feat(module): describe your clear, concise enhancement"
git push origin feature/my-new-feature
```

### Step 8: Open a Pull Request (PR)
1. Go to your fork on GitHub: `https://github.com/<your-username>/HashForge`.
2. Click the green **"Compare & pull request"** button that appears.
3. Fill out the PR description with what you changed and how you tested it.
4. Click **"Create pull request"**.
5. The maintainers will review your code, run automated CI checks, and merge it into `main`!

---

## 2. Direct Collaborator Access (For Team Members)

If you are a core team member or partner and the repository owner wants you to push directly to the repository without forking:

1. The repository owner goes to **GitHub > DEMOCODE675/HashForge > Settings**.
2. Under **Access**, click **Collaborators**.
3. Click **"Add people"** and search for the collaborator's GitHub username or email.
4. Select the role (**Write** access allows pushing directly to branches).
5. The invitee will receive an email or GitHub notification at `https://github.com/DEMOCODE675/HashForge/invitations`.
6. Once accepted, the collaborator can clone the repository directly:
   ```bash
   git clone https://github.com/DEMOCODE675/HashForge.git
   git checkout -b feature/branch-name
   git push origin feature/branch-name
   ```

---

## 3. Engineering Guidelines & Invariants

To keep HashForge robust and cryptographically sound, all contributors must observe these rules:

1. **Zero Emojis:** Do not use emoji characters anywhere in UI text, navigation, or buttons. Use official [Lucide React](https://lucide.dev) SVG icons exclusively.
2. **Big-Endian Bit Addressing:** Maintain the established standard:
   $$\text{Byte Index } i = \lfloor k / 8 \rfloor, \quad \text{Bit Offset } b = 7 - (k \bmod 8)$$
3. **FIPS Compliance:** Do not implement proprietary or untested cryptographic algorithms. Stick to NIST standard specifications (FIPS 180-4 for SHA-2, FIPS 202 for SHA-3).
4. **Memory-Safe Streaming:** For file operations, stream data in 64KB buffers. Never load entire large files into volatile memory all at once.
5. **Mobile Responsiveness:** All UI components must remain responsive and touch-friendly on viewports down to 360px.
