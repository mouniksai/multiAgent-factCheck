# 📘 Document 1: Project Overview & Vision — Aletheia AI

**Course:** Foundations of Artificial Intelligence (FAI)  
**Project Title:** Aletheia AI — Dialectical Multi-Agent Fact-Checking & Epistemic Audit Framework  
**Theoretical Paradigm:** Multi-Agent Systems, Adversarial Search, Russell & Norvig PEAS Formulation, Game-Theoretic Dialectic, Epistemic Uncertainty Calibration  

---

## 1. Executive Summary & Problem Statement

### The Problem with Modern AI Fact-Checking
When a user asks standard Large Language Models (e.g., vanilla GPT-4, Claude, or Gemini) to verify a factual claim, the system frequently fails due to five well-documented epistemic vulnerabilities:
1. **Confirmation & Sycophancy Bias:** LLMs tend to agree with the premise of the user's prompt rather than aggressively stress-testing it.
2. **Hallucinated Citations:** Generating authoritative-sounding academic citations or URLs that do not exist.
3. **Flat Epistemic Weighting:** Treating an unvetted forum comment (e.g., Reddit) with the same epistemic weight as a peer-reviewed systematic meta-analysis in *The Lancet* or data from the *World Health Organization*.
4. **Forced Binary Fallacy:** Forcing nuanced, contested, or evolving scientific claims into a crude "True" or "False" verdict, concealing genuine empirical ambiguity.
5. **Temporal Blindness:** Static model weights lack real-time access to the rapidly mutating open web.

### What We Are Trying to Do (The Vision)
We set out to build **Aletheia AI**: an autonomous, dialectical multi-agent architecture rooted in classical jurisprudence and the Foundations of Artificial Intelligence. Instead of relying on a single fallible prompt, Aletheia orchestrates an **adversarial court of specialized agents**:
- A **Claim Normalizer** decomposes complex user claims into testable atomic elements.
- An adversarial debate arena pits a **PRO Debater** (arguing for the claim) against a **CON Debater** (arguing against the claim), each equipped with live web retrieval.
- A **Cross-Examiner Agent** audits both sides for rhetorical fallacies (**Correlation vs. Causation, Hasty Generalization, False Dichotomy**) and isolates points of consensus vs. empirical contention.
- An **Epistemic Source Authority Scorer** weights evidence based on institutional rigor (Tier-1 Journals, Government portals vs. unvetted blogs).
- A **Citation Integrity Guardrail** deterministically verifies that every cited fact corresponds 100% to real evidence.
- An impartial **Supreme Judge** renders a calibrated verdict (`TRUE`, `FALSE`, or `UNVERIFIABLE`), complete with an explicit **Confidence Score** and an **Uncertainty Advisory Note**.

---

## 2. Foundations of Artificial Intelligence (Curriculum Connections)

This project is an end-to-end implementation of foundational AI concepts from the standard **Russell & Norvig** curriculum:

```
                          ┌────────────────────────┐
                          │   Foundations of AI    │
                          └───────────┬────────────┘
         ┌────────────────────────────┼───────────────────────────┐
         ▼                            ▼                           ▼
┌──────────────────┐       ┌────────────────────┐      ┌─────────────────────┐
│  Agent Theory &  │       │ Adversarial Search │      │ Information Theory  │
│  PEAS Taxonomy   │       │ & Game Dialectic   │      │ & Calibration       │
├──────────────────┤       ├────────────────────┤      ├─────────────────────┤
│ 6 Agent Roles    │       │ Non-zero-sum game  │      │ Epistemic entropy   │
│ 7 Env Dimensions │       │ Minimax tension    │      │ Hybrid RRF fusion   │
│ Stateful Graph   │       │ Dialectical Triad  │      │ Guardrail filtering │
└──────────────────┘       └────────────────────┘      └─────────────────────┘
```

1. **Russell & Norvig PEAS Formulation:** Every agent is rigorously formalized with its Performance Measure (P), Environment (E), Actuators (A), and Sensors (S).
2. **Canonical Environment Dimensions:** Formal evaluation across all 7 environment properties: *Partially Observable, Multi-Agent, Stochastic, Sequential, Dynamic, Discrete, Unknown Transition Model*.
3. **Adversarial Game Theory & Dialectic:** Replaces naive single-agent generation with a dialectical triad:
   - **Thesis** (Pro Debater)
   - **Antithesis** (Con Debater)
   - **Synthesis & Cross-Examination** (Impartial Cross-Examiner)
4. **Algorithmic Search & Information Retrieval:** Implements and benchmarks sparse lexical retrieval (**BM25 Okapi**), dense semantic vector search (**FAISS IndexFlatIP**), and rank-harmonized **Reciprocal Rank Fusion (RRF)**.
5. **Epistemic Calibration & Uncertainty Modeling:** Incorporates Bayesian-inspired calibration to quantify epistemic uncertainty, ensuring ambiguous claims yield hedged confidence.

---

## 3. What We Have Built in Detail

### A. The 6-Agent Architecture
1. **Claim Normalizer Agent (`src/agents/claim_agent.py`):**
   - Ingests raw, messy, or compound user assertions.
   - Decomposes them into 1–3 independent, atomic, checkable sub-claims.
   - Eliminates multi-hop retrieval errors before search begins.
2. **PRO Debater Agent (`src/agents/pro_agent.py`):**
   - Assumes a supporting stance ($H_0$).
   - Formulates stance-conditioned queries to discover affirmative evidence.
   - Generates persuasive, evidence-grounded arguments citing source IDs `[E1]`, `[E2]`.
3. **CON Debater Agent (`src/agents/con_agent.py`):**
   - Assumes a refuting stance ($\neg H_0$).
   - Formulates adversarial search queries to surface counter-evidence, confounding variables, and negative clinical trials.
   - Actively attacks the vulnerabilities of prior PRO arguments.
4. **Dialectical Cross-Examiner Agent (`src/agents/cross_examiner.py`):**
   - Impartial auditor that does not take a side.
   - Analyzes debate turns for formal fallacies:
     - *Correlation vs. Causation* (treating observational correlations as direct biological causation).
     - *Hasty Generalization* (extrapolating universal claims from isolated small-cohort studies).
     - *False Dichotomy* (reducing multifaceted health/policy issues to black-and-white outcomes).
     - *Selection Bias / Cherry-Picking* (citing favorable pilot data while ignoring systematic reviews).
   - Maps out undisputed **Points of Consensus** vs. disputed **Points of Contention**.
5. **Citation Integrity Guardrail (`src/agents/verify.py`):**
   - Deterministic regex parser that extracts all citation tags (e.g., `[E1]`, `[E99]`).
   - Cross-checks every tag against the active evidence pool registry.
   - If an agent invents a non-existent citation ID, the guardrail intercepts it, triggers a violation flag, and automatically applies a confidence penalty.
6. **Supreme Judge Agent (`src/agents/judge_agent.py`):**
   - Impartial judicial arbitrator powered by high-capacity reasoning (`openai/gpt-oss-120b`).
   - Ingests the full transcript, verified evidence, source credibility tiers, and cross-examination audit.
   - Delivers a final calibrated verdict:
     - `TRUE`: Unambiguous consensus with robust Tier-1 backing.
     - `FALSE`: Overwhelming counter-evidence refuting the core claim.
     - `UNVERIFIABLE`: Mixed, conflicting, or non-causal evidence (automatically hedges confidence to 45–65% and produces an explicit Uncertainty Note).

### B. Epistemic Source Authority Scorer (`src/retrieval/source_scorer.py`)
Categorizes every retrieved web source into institutional credibility tiers:
- **Tier 1 (0.95–0.98):** Peer-Reviewed Academic Journals (`nature.com`, `science.org`, `thelancet.com`, `.edu`) and Government Agencies (`cdc.gov`, `nih.gov`, `who.int`, `nasa.gov`).
- **Tier 2 (0.80–0.90):** International Wire News & Curated Encyclopedias (`reuters.com`, `apnews.com`, `bbc.com`, `britannica.com`).
- **Tier 3 (0.65–0.75):** General Web Publications & Media.
- **Tier 4 (0.30–0.50):** Unvetted User-Generated Content & Community Forums (`reddit.com`, `medium.com`).

### C. Resilient Multi-Tier Web Retrieval (`src/retrieval/web_search.py`)
Guarantees **100% demo safety and sub-second execution** during classroom presentations:
- **Tier 1:** Tavily Live Search API (Deep advanced academic retrieval).
- **Tier 2:** DuckDuckGo Live Search Engine (Keyless live web search).
- **Tier 3:** Query Simplification Retry (Removes strict stance words).
- **Tier 4:** In-Memory Session Cache & Grounded Benchmark Knowledge (Zero-latency fallback ensuring presentations never crash even without internet).

### D. Executive 5-Tab Modern Dashboard (`app/streamlit_app.py`)
A glassmorphic, enterprise-grade web application featuring:
- **Tab 1: Fact-Check Arena** (Live debate streaming, side-by-side cards, trust badges, verdict meter, and JSON dossier download).
- **Tab 2: Evidence & Authority Explorer** (Searchable database of all retrieved sources with credibility scores).
- **Tab 3: Algorithmic Search Benchmark** (Interactive BM25 vs. FAISS vs. Hybrid RRF comparison with millisecond latency metrics).
- **Tab 4: Automated Benchmark Suite** (1-click execution of 5 canonical scenarios with pass/fail evaluation tables).
- **Tab 5: PEAS & Architecture Specs** (Formal reference for examiners).

---

## 4. Evaluation Rubric Alignment (Full 20/20 Marks Strategy)

Both Review 1 and Review 2 are evaluated simultaneously. Here is exactly how Aletheia AI addresses every rubric requirement:

| Rubric Item | Weight | Project Implementation | Presentation Slide |
| :--- | :---: | :--- | :---: |
| **Review 1: PEAS Formulation** | **3M** | Formalized Russell & Norvig matrix across all 6 agents (Claim Normalizer, Pro, Con, Cross-Examiner, Guardrail, Judge). | Slide 3 |
| **Review 1: Environment & Agent Analysis** | **3M** | Detailed evaluation across 7 canonical dimensions: Stochastic, Partially Observable, Sequential, Dynamic, Multi-Agent, Mixed Cooperative-Competitive, Discrete. | Slide 4 |
| **Review 1: Algorithmic Modeling & Search Strategy** | **3M** | Mathematical formulation of Atomic Decomposition, Stance Query Generation, Hybrid Search (BM25 + FAISS Dense + RRF $c=60$), Domain Scorer, and Fallacy Auditing. | Slide 6 |
| **Review 1: Q&A & Presentation Mechanics** | **1M** | Professional 16:9 widescreen presentation without blurry screenshots + comprehensive defense cards. | Slide 10 |
| **Review 2: Tool/Package Selection & Setup** | **3M** | Documented selection and justification for Python 3.11, LangGraph, Groq LPU, Tavily/DDGS, FAISS, BM25, Streamlit, Pydantic, pytest. | Slide 7 |
| **Review 2: Multi-Agent Execution & Interaction** | **3M** | Full cyclic StateGraph architecture in LangGraph, shared `DebateState`, inter-agent communication, and Dialectical Triad synthesis. | Slides 5 & 8 |
| **Review 2: Demo Quality & Testing Scenarios** | **3M** | 5 diverse real-world scenarios (Clear False, Clear True, Ambiguous, Misleading, Time-Sensitive) tested with 100% pass rate in `eval/run_eval.py`. | Slide 9 |
| **Review 2: Code Structure & Scalability** | **1M** | Modular clean architecture, decoupled agent layers, type-safe schemas, and automated test suite (6/6 tests passing). | Slides 8 & 10 |
| **TOTAL** | **20M** | **Comprehensive Full Marks Coverage** | **All Slides** |
