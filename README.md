# Text/Code Complexity & Security Analyzer (Shannon Entropy)

A Streamlit-based application to analyze character-level Shannon entropy, calculate probability gradients, ynthetic_egov_large.csv   # created by the generator; not committed , and inspect code complexity metrics.

---

## Folder Structure

```
entropy_analyzer/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md           # Setup and usage guide
└── samples/            # Test and sample files
    └── fake_log.txt    # Sample log with dummy PII & secrets
```

---

## Setup & Running the Application

### 1. Open a Terminal / PowerShell
Navigate to the `entropy_analyzer` folder:

```bash
cd "C:\Users\Dell\.gemini\antigravity\scratch\entropy_analyzer"
```

### 2. Create and Activate a Virtual Environment
- **Windows (Command Prompt / PowerShell):**
  ```powershell
  python -m venv .venv
  .venv\Scripts\activate
  ```
  *(If on PowerShell you encounter an execution policy error, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first).*

- **macOS / Linux:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Application
```bash
streamlit run app.py
```

### 5. Access the Web UI
Open your browser and navigate to:
**http://localhost:8501**

---

## Features
- **Entropy Analysis:** Computes per-character frequency, probability $p$, Shannon entropy $H$, and qualitative band (Low / Moderate / High).
- **Calculus & Curves:** Plots contribution curve $h(p) = -p \log_2 p$, estimates central-difference gradient $\frac{dh}{dp}$, and calculates trapezoidal area.
- **Pattern & Security Scan:** Heuristically flags possible emails, phone numbers, Aadhaar numbers, passwords, API tokens, and private keys with automated masking.
- **Code Metrics:** Cyclomatic complexity (AST-based for Python, regex-based for others), line counts, and comment estimation.
- **Exporting:** Download text audit reports and character frequency CSVs.

## Limitations
- Entropy measures character distribution only. It does not prove a file is encrypted, compressed, or malicious.
- Pattern matches can be false positives (for example, a 12-digit number) or miss real secrets.
- The risk score is a heuristic for triage, not a certified security rating.
- Use synthetic or public data only. Never upload real credentials or personal identifiers.
