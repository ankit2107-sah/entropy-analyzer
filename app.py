import ast
import math
import re
from collections import Counter

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

EPS = 1e-7

SAMPLES = {
    "Repeated character": "AAAAAAAAAA",
    "Worked example (AAB)": "AAB",
    "E-governance log": (
        "INFO login ok user=test01 email=citizen@example.com\n"
        "WARN password=Secr3tPass99\n"
        "INFO upload complete"
    ),
    "Random-looking string": "q7Zx9LmP2vKd8RtB4nWc6HsY1aJ0eF3u",
}

# name: (regex, severity, points)
PATTERNS = {
    "Email address": (r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "Medium", 10),
    "Phone-like number (India)": (r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)", "Medium", 10),
    "Aadhaar-like number": (r"(?<!\d)\d{4}\s?\d{4}\s?\d{4}(?!\d)", "High", 20),
    "Password/secret assignment": (r"(?i)\b(?:password|pwd|secret)\s*[=:]\s*\S+", "High", 20),
    "API/access token": (r"(?i)\b(?:api_key|access_token|token)\s*[=:]\s*[A-Za-z0-9_\-]{8,}", "High", 20),
    "Private-key header": (r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", "Critical", 35),
    "Long hex/Base64-like run": (r"[A-Za-z0-9+/=]{32,}", "Review", 8),
}
SEVERITY_POINTS = {"Medium": 10, "High": 20, "Critical": 35, "Review": 8}


def h(p):
    """Contribution h(p) = -p log2 p."""
    return 0.0 if p <= 0 else -p * math.log2(p)


def dh_dp(p):
    """Central-difference estimate of dh/dp."""
    p = min(max(p, 1e-6), 1 - 1e-6)
    return (h(p + EPS) - h(p - EPS)) / (2 * EPS)


def band(H):
    if H < 3:
        return "Low entropy"
    if H < 5:
        return "Moderate entropy"
    return "High entropy"


def analyse_entropy(text):
    n = len(text)
    counts = Counter(text)
    rows = []
    for ch, f in counts.most_common():
        rows.append({"char": repr(ch)[1:-1], "count": f, "p": f / n})
    df = pd.DataFrame(rows)

    probs = df["p"].to_numpy()
    H = sum(h(p) for p in probs)

    grads = [dh_dp(p) for p in probs]
    order = np.sort(probs)
    ys = [h(p) for p in order]
    area = sum(
        (ys[i] + ys[i + 1]) / 2 * (order[i + 1] - order[i])
        for i in range(len(order) - 1)
    )
    return {
        "n": n,
        "unique": len(counts),
        "H": H,
        "table": df,
        "grad_mean": float(np.mean(grads)),
        "grad_min": float(np.min(grads)),
        "grad_max": float(np.max(grads)),
        "area": area,
        "curve_x": order,
        "curve_y": np.array(ys),
    }


def scan_patterns(text):
    findings = []
    for name, (regex, sev, pts) in PATTERNS.items():
        for m in re.finditer(regex, text):
            value = m.group(0)
            masked = value[:3] + "*" * max(len(value) - 6, 3) + value[-3:] if len(value) > 8 else "***"
            findings.append({"indicator": name, "severity": sev, "points": pts, "masked": masked})
    return findings


def risk_score(findings):
    score = min(100, sum(f["points"] for f in findings))
    if score == 0:
        label = "No pattern detected"
    elif score < 25:
        label = "Low - review flagged items"
    elif score < 60:
        label = "Moderate - review findings"
    else:
        label = "High - investigate"
    return score, label


def code_metrics(text, filename=""):
    lines = text.splitlines()
    non_empty = [l for l in lines if l.strip()]
    comments = [l for l in lines if l.strip().startswith(("#", "//", "/*", "*", "<!--"))]
    result = {
        "Total lines": len(lines),
        "Non-empty lines": len(non_empty),
        "Comment lines (approx.)": len(comments),
    }
    if filename.lower().endswith(".py"):
        try:
            tree = ast.parse(text)
            funcs = sum(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) for n in ast.walk(tree))
            D = 0
            for node in ast.walk(tree):
                if isinstance(node, (ast.If, ast.For, ast.While, ast.IfExp, ast.ExceptHandler, ast.comprehension)):
                    D += 1
                elif isinstance(node, ast.BoolOp):
                    D += len(node.values) - 1
            result.update({"Functions": funcs, "Decision points (D)": D,
                           "Cyclomatic complexity (M = D+1)": D + 1, "Method": "AST"})
            return result
        except SyntaxError:
            pass
    D = len(re.findall(r"\b(?:if|for|while|catch|case|elif|else if)\b|&&|\|\|", text))
    funcs = len(re.findall(r"\bdef\s+\w+|\bfunction\s+\w+|\b\w+\s*\([^)]*\)\s*\{", text))
    result.update({"Functions": funcs, "Decision points (D)": D,
                   "Cyclomatic complexity (M = D+1)": D + 1, "Method": "regex (approximate)"})
    return result


def build_report(text, stats, findings, score, label, metrics):
    lines = [
        "TEXT/CODE ENTROPY & SECURITY AUDIT REPORT",
        "=" * 44,
        f"Characters: {stats['n']}",
        f"Unique characters: {stats['unique']}",
        f"Entropy: {stats['H']:.4f} bits/char ({band(stats['H'])})",
        f"Risk score: {score}/100 - {label}",
        "",
        "Findings (masked):",
    ]
    lines += [f"  - {f['indicator']} [{f['severity']}]: {f['masked']}" for f in findings] or ["  None"]
    lines += ["", "Code metrics:"] + [f"  {k}: {v}" for k, v in metrics.items()]
    lines += ["", "Note: heuristic educational triage, not a security audit."]
    return "\n".join(lines)


# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="Shannon Entropy & Security Analyzer", layout="wide")
st.title("Text/Code Complexity & Security Analyzer (Shannon Entropy)")

if "text" not in st.session_state:
    st.session_state.text = ""

col1, col2 = st.columns([2, 1])
with col2:
    sample = st.selectbox("Load a sample", ["(none)"] + list(SAMPLES))
    if sample != "(none)" and st.button("Use sample"):
        st.session_state.text = SAMPLES[sample]
        st.session_state.filename = ""
    uploaded = st.file_uploader(
        "Upload a file",
        type=["txt", "log", "py", "c", "h", "cpp", "java", "js", "ts", "csv", "html", "json"],
    )
    if uploaded is not None:
        st.session_state.text = uploaded.getvalue().decode("utf-8", errors="ignore")
        st.session_state.filename = uploaded.name

with col1:
    text = st.text_area("Paste text or code", value=st.session_state.text, height=220)

filename = st.session_state.get("filename", "")

if st.button("Analyse input", type="primary") and text.strip():
    stats = analyse_entropy(text)
    findings = scan_patterns(text)
    score, label = risk_score(findings)
    metrics = code_metrics(text, filename)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Characters", stats["n"])
    c2.metric("Unique characters", stats["unique"])
    c3.metric("Entropy (bits/char)", f"{stats['H']:.4f}")
    c4.metric("Band", band(stats["H"]))

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Frequency", "Contribution curve", "Calculus", "Security scan", "Code metrics"]
    )

    with tab1:
        top = stats["table"].head(20)
        fig, ax = plt.subplots()
        ax.bar(top["char"], top["count"])
        ax.set_xlabel("Character")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)
        st.dataframe(stats["table"], use_container_width=True)

    with tab2:
        fig, ax = plt.subplots()
        ax.plot(stats["curve_x"], stats["curve_y"], "o-")
        ax.set_xlabel("Probability p")
        ax.set_ylabel("Contribution h(p) = -p log2 p")
        st.pyplot(fig)

    with tab3:
        st.write(f"Gradient dh/dp (central difference, eps={EPS}): "
                 f"mean {stats['grad_mean']:.4f}, min {stats['grad_min']:.4f}, max {stats['grad_max']:.4f}")
        st.write(f"Trapezoidal area under sorted curve: {stats['area']:.4f}")
        st.caption("The area is not the Shannon entropy and is not a security metric.")

    with tab4:
        st.write(f"**Risk score: {score}/100 - {label}**")
        if findings:
            st.dataframe(pd.DataFrame(findings), use_container_width=True)
        else:
            st.success("No sensitive-looking patterns found.")
        st.caption("Pattern matching has false positives and false negatives. Review manually.")

    with tab5:
        st.table(pd.Series(metrics, name="Value"))

    report = build_report(text, stats, findings, score, label, metrics)
    d1, d2 = st.columns(2)
    d1.download_button("Download TXT report", report, "audit_report.txt")
    csv = stats["table"].to_csv(index=False)
    d2.download_button("Download character CSV", csv, "character_frequency.csv")
elif st.button("Analyse input") and not text.strip():
    st.warning("Please paste text, upload a file, or load a sample.")
