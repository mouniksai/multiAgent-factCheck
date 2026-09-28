# 🎬 Document 4: Live Demo Script & Step-by-Step Presentation Guide — Aletheia AI

**Course:** Foundations of Artificial Intelligence (FAI)  
**Rubric Focus:** Review 2 — Demo Quality & Testing Scenarios (3 Marks)  
**Goal:** Deliver a flawless, high-impact presentation and live demo with zero fumbles, zero lag, and 100% confidence.

---

## 1. Pre-Demo Setup & Verification (Do This Before Presenting)

Open your terminal in the project directory:
```bash
cd /Users/mouniksai/Documents/multiAgent-factCheck
```

Verify that all dependencies and automated tests pass cleanly:
```bash
pytest tests/test_graph.py
```
*(Expected output: `6 passed in ~16s` with 0 failures and 0 warnings).*

---

## 2. Launching the Interactive Presentation Environment

### Step A: Open the Presentation Deck
Open the generated presentation in PowerPoint or Keynote:
- File location: `Aletheia_Dialectical_Fact_Checking.pptx` (or in `/Users/mouniksai/Downloads/Aletheia_Dialectical_Fact_Checking.pptx`).
- Walk through Slides 1 through 7 during your conceptual presentation (PEAS, Environment, Algorithmic Modeling, Tooling).

### Step B: Launch the Live Streamlit Dashboard
In your terminal, execute:
```bash
streamlit run app/streamlit_app.py
```
The browser will automatically open at `http://localhost:8501`.

---

## 3. The 5-Minute Live Demo Script (Step-by-Step Walkthrough)

Follow this sequence to cover all rubric requirements and impress the evaluators:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        LIVE DEMO TIMELINE                              │
├───────────────┬───────────────────────────────┬────────────────────────┤
│ Minute 01     │ The Genuinely Ambiguous Claim │ Tab 1: Coffee & CVD    │
│ Minute 02     │ The Empirical Refutation      │ Tab 1: Great Wall Myth │
│ Minute 03     │ Cross-Examiner & Guardrail    │ Fallacies & [Ex] tags  │
│ Minute 04     │ Algorithmic Search Benchmark  │ Tab 3: BM25 vs FAISS   │
│ Minute 05     │ Automated Benchmark Harness   │ Tab 4: 5/5 Test Suite  │
└───────────────┴───────────────────────────────┴────────────────────────┘
```

---

### Step 1: The Genuinely Ambiguous Claim (Showcases Epistemic Calibration)
*Why this first? Evaluators hate seeing naive AI say "True" or "False" to nuanced medical/scientific claims. Showing calibration immediately proves your project is advanced.*

1. In **Tab 1: Fact-Check Arena**, go to the **Quick Benchmark Preset** dropdown on the left sidebar.
2. Select: **`3. Genuinely Ambiguous (Caffeine)`**:
   > *"Moderate coffee consumption increases the risk of heart disease."*
3. Set **Debate Rounds** to `1 Round (Fast ~2s)`.
4. Click **`🚀 Verify Claim`**.
5. **What to Say to Evaluators:**
   > *"Notice how the system decomposes the claim into atomic sub-claims. In parallel, our PRO agent retrieves cardiology studies from Harvard indicating cardiovascular safety, while our CON agent retrieves trials on arrhythmia risks in slow caffeine metabolizers.*
   >
   > *Instead of forcing a binary True/False verdict like vanilla ChatGPT, our Supreme Judge correctly recognizes the empirical contradiction: it renders an **UNVERIFIABLE** verdict, calibrates confidence to **55%**, and provides an explicit **Uncertainty Note** highlighting dosage and genetic polymorphisms."*

---

### Step 2: The Empirical Refutation (Showcases Counter-Evidence Power)

1. In the sidebar dropdown, select: **`1. Clear False (Space Myth)`**:
   > *"The Great Wall of China is visible from space with the naked eye."*
2. Click **`🚀 Verify Claim`**.
3. **What to Say to Evaluators:**
   > *"Here, the PRO agent cites the monumental physical dimensions of the wall, but the CON agent retrieves satellite photography and optical physics from NASA and Scientific American. The Cross-Examiner identifies that unaided human eye resolution cannot resolve narrow structures from orbit. The Supreme Judge delivers an authoritative **FALSE** verdict with **95% confidence**."*

---

### Step 3: Showcase the Dialectical Cross-Examiner & Citation Guardrail

1. Scroll down to Section 3: **`⚖️ 3. Cross-Examiner Dialectical Audit & Synthesis`**.
2. Point out:
   - **Consensus Points:** Shared baseline facts agreed upon by both sides.
   - **Contention Points:** Core points of scientific disagreement.
   - **Detected Fallacies:** Highlights where debaters committed *Correlation vs. Causation* or *Hasty Generalization*.
3. Scroll down to the **Supreme Judicial Verdict Card**:
   - Point out the **Citation Guardrail Status: Clean (100% Grounded)**.
   - Point out the **Epistemic Source Credibility** score.
   - Click the **`📥 Download Fact-Check Audit Dossier (JSON)`** button to show that the system produces complete compliance audit trails.

---

### Step 4: Live Algorithmic Search Benchmark (Rubric 1: 3 Marks)

1. Click on **Tab 3: 🔬 Algorithmic Search Benchmark**.
2. Click **`⚡ Run Retrieval Benchmark`**.
3. Show the three side-by-side columns:
   - **BM25 Okapi (Sparse Lexical):** Latency `< 1ms`, exact keyword matching.
   - **FAISS Dense (Semantic Vector):** Captures conceptual synonyms like arterial plaque and cardiac arrest.
   - **Hybrid Reciprocal Rank Fusion (RRF $c=60$):** Combines the ranks to give the ultimate reranked evidence pool.
4. **What to Say to Evaluators:**
   > *"This directly satisfies Review 1: Algorithmic Modeling. We implemented both sparse BM25 and dense semantic search, and fused them via Reciprocal Rank Fusion using smoothing constant c=60 to eliminate lexical and semantic blind spots."*

---

### Step 5: Automated 5-Scenario Benchmark Test Suite (Rubric 2: 3 Marks)

1. Click on **Tab 4: 🧪 Automated Benchmark Suite**.
2. Click **`▶️ Execute 5-Scenario Benchmark Test`**.
3. Watch the progress bar execute and render the full table:
   - Clear False (Great Wall) ➔ `FALSE` (95%) ➔ **PASS**
   - Clear True (Exercise) ➔ `TRUE` (92%) ➔ **PASS**
   - Genuinely Ambiguous (Coffee) ➔ `UNVERIFIABLE` (55%) ➔ **PASS**
   - Misleading Context (1.5C Climate) ➔ `FALSE` (94%) ➔ **PASS**
   - Time-Sensitive (Lithium Battery) ➔ `UNVERIFIABLE` (62%) ➔ **PASS**
4. **What to Say to Evaluators:**
   > *"All 5 benchmark scenarios pass ground-truth verification and strict calibration thresholds, proving our system's robustness across diverse scientific, historical, and economic domains."*

---

## 4. Alternative CLI Demonstration (If Evaluators Ask to See Code / Terminal)

If an examiner asks: *"Can this run without the web UI?"* or *"Show me the terminal output."*

Run this single command:
```bash
python fact_check_cli.py --claim "Moderate coffee consumption increases the risk of heart disease." --rounds 1
```
It will print the formatted headers, atomic sub-claims, retrieved evidence pool with credibility tiers, the Cross-Examiner synthesis, and the Supreme Judge calibrated verdict directly in the terminal!

To display the formal PEAS formulation on CLI:
```bash
python fact_check_cli.py --peas
```
