# Contributing to HashForge

Thank you for your interest in contributing to **HashForge**!

## Code of Conduct
Please ensure all interactions are constructive, professional, and respectful.

## Getting Started
1. Fork the repository and clone your fork locally:
   ```bash
   git clone https://github.com/your-username/HashForge.git
   cd HashForge
   ```
2. Create a clean virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
3. Create a feature branch:
   ```bash
   git checkout -b feature/my-enhancement
   ```

## Development Guidelines
- **Core Engine Separation:** Never import Streamlit or UI elements into `core/`. Keep cryptographic algorithms pure and testable.
- **Bit Indexing Convention:** Maintain Big-Endian network order for bit indexing.
- **Automated Tests:** Add unit tests to `tests/` for any new mathematical or cryptographic features. Run tests before submitting:
  ```bash
  python -m pytest tests/ -v
  ```
- **FIPS Compliance:** Do not invent proprietary hash algorithms. Use standard library implementations.

## Submitting Pull Requests
- Ensure all 53 automated tests pass.
- Write clear, concise commit messages.
- Fill out the PR template describing your changes and verification steps.

