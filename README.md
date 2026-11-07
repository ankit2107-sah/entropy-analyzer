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

# How to Use
1. **Provide input** using one of three options:
   - Paste text into the text box.
   - Upload a TXT, LOG, PY, C, H, CPP, JAVA, JS, TS, CSV, HTML, or JSON file. Files are read as UTF-8 text and are never executed.
   - Choose a built-in sample from the dropdown and click **Use sample**.
2. Click **Analyse input**.
3. Review the result tabs:
   - **Frequency:** most common characters and the probability table.
   - **Contribution curve:** the plot of p against h(p).
   - **Calculus:** gradient statistics and trapezoidal area.
   - **Security scan:** risk score, label, and masked findings.
   - **Code metrics:** line, function, and complexity figures.
4. Download the **TXT report** and **character CSV** if you need them.
---

## Generating Large Synthetic Test Data

To test with a large file, run:

```bash
python make_synthetic_data.py 500000
```

This writes about 500,000 fake e-governance records to `samples/synthetic_egov_large.csv` (roughly 50–60 MB). The script uses a fixed random seed (42), so the output is the same on every run. All names, emails (`example.com`), and IDs are invented.

Large files can slow the browser because the whole file is loaded into the text box. If the page becomes slow, generate a smaller file, for example `python make_synthetic_data.py 100000`.

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
- 
## Safe Data Use

- Use only synthetic data, sample files, or public datasets.
- Never upload real passwords, API keys, private keys, Aadhaar numbers, or other personal identifiers.
- Review any output before sharing it.

---

## Troubleshooting

- **`python` not found:** Install Python from python.org and tick "Add python.exe to PATH".
- **`No module named streamlit`:** Activate `.venv` and run `python -m pip install -r requirements.txt` from the project folder.
- **Page does not open:** Keep the terminal running, use `http://localhost:8501`, or try `python -m streamlit run app.py --server.port 8502`.

---

## Acknowledgements

Developed as part of Project 4.2 (Text/Code Complexity & Security Vulnerability Analyzer Using Shannon Entropy), SRM Institute of Science and Technology, Ramapuram. Supervised by Mr. Johnty Rodes L.

---

## License

For academic use. Add a license file if you plan to reuse or distribute the code.
