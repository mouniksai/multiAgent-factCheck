# 📂 Document 3: Codebase Architecture & File-by-File Guide — Aletheia AI

**Course:** Foundations of Artificial Intelligence (FAI)  
**Rubric Focus:** Review 2 — Code Structure & Scalability (1 Mark) + Setup (3 Marks)  

---

## 1. Directory Tree & Architecture Map

```
multiAgent-factCheck/
│
├── app/
│   └── streamlit_app.py        # Executive modern 5-tab Streamlit dashboard
│
├── docs/                       # Complete documentation & viva guides
│   ├── 01_PROJECT_OVERVIEW.md
│   ├── 02_SYSTEM_FLOW_AND_INTERACTION.md
│   ├── 03_CODEBASE_ARCHITECTURE_AND_FILE_GUIDE.md
│   ├── 04_LIVE_DEMO_SCRIPT_AND_STEPS.md
│   └── 05_VIVA_QA_AND_EXAMINER_DEFENSE.md
│
├── eval/
│   ├── run_eval.py             # 5-scenario benchmark evaluation & calibration harness
│   └── test_claims.json        # Benchmark dataset (Ground truth, categories, max confidence)
│
├── src/
│   ├── __init__.py             # Module root
│   ├── config.py               # Runtime configuration, model names & API keys
│   │
│   ├── agents/                 # Autonomous agent implementations
│   │   ├── __init__.py
│   │   ├── claim_agent.py      # Claim normalizer & sub-claim decomposition
│   │   ├── pro_agent.py        # PRO supporting debater agent
│   │   ├── con_agent.py        # CON refuting debater agent
│   │   ├── cross_examiner.py   # Dialectical cross-examiner & logical fallacy auditor
│   │   ├── judge_agent.py      # Supreme Judge & epistemic calibration arbitrator
│   │   ├── verify.py           # Citation integrity guardrail & hallucination detector
│   │   └── groq_client.py      # High-speed Groq LPU client with automatic retry
│   │
│   ├── graph/                  # LangGraph orchestration
│   │   ├── __init__.py
│   │   ├── state.py            # DebateState TypedDict definition
│   │   └── debate_graph.py     # StateGraph pipeline assembly & node definitions
│   │
│   ├── retrieval/              # Information retrieval & epistemic authority
│   │   ├── __init__.py
│   │   ├── source_scorer.py    # Domain authority & credibility tier classifier
│   │   ├── web_search.py       # Multi-tier web retrieval (Tavily, DDGS, Session Cache)
│   │   └── hybrid_search.py    # BM25 Okapi + FAISS Dense + Reciprocal Rank Fusion (RRF)
│   │
│   └── prompts/                # System prompts for LLM agents
│       ├── __init__.py
│       ├── claim_prompt.py     # Claim decomposition prompt
│       ├── debater_prompt.py   # PRO and CON debater prompt template
│       └── judge_prompt.py     # Supreme Judge prompt template
│
├── tests/
│   ├── test_graph.py           # Comprehensive pytest suite (6 automated tests)
│   └── test_graph_cli.py       # Fast CLI regression checks
│
├── fact_check_cli.py           # Full interactive CLI runner & algorithmic benchmark utility
├── generate_presentation.py    # Programmatic presentation generator (python-pptx)
├── Aletheia_Dialectical_Fact_Checking.pptx # 16:9 Presentation Deck (No AI screenshots)
├── requirements.txt            # Python dependencies
└── README.md                   # Project overview & quickstart
```

---

## 2. Comprehensive File-by-File Breakdown

### 🎯 Entry Points & User Interfaces

#### 1. `app/streamlit_app.py`
- **Purpose:** Modern, glassmorphic executive web interface for live presentations and user interaction.
- **Key Features:**
  - **Tab 1: Fact-Check Arena:** Real-time state progress streaming, decomposed sub-claims, side-by-side Pro vs. Con cards with colored credibility badges, Cross-Examiner audit box, Supreme Judicial Verdict Card, and one-click JSON audit dossier download.
  - **Tab 2: Evidence Explorer:** Searchable tabular database of all retrieved sources, showing domain, authority tier, and numerical credibility score.
  - **Tab 3: Algorithmic Search Benchmark:** Interactive comparison of BM25 (Sparse), FAISS (Dense), and Hybrid RRF with live latency metrics (satisfies Rubric 1).
  - **Tab 4: Automated Benchmark Suite:** 1-click evaluation of all 5 canonical test scenarios with pass/fail tables (satisfies Rubric 2).
  - **Tab 5: PEAS & Specs:** Formal Russell & Norvig taxonomy table and 7 environment dimensions ready for examiner inspection.

#### 2. `fact_check_cli.py`
- **Purpose:** Command-line interface for terminal-based fact-checking and automated benchmarking.
- **Key Commands:**
  - `python fact_check_cli.py --claim "..." --rounds 1` (Runs full multi-agent pipeline).
  - `python fact_check_cli.py --peas` (Prints formal PEAS and Environment specifications).
  - `python fact_check_cli.py --benchmark-search` (Runs BM25 vs FAISS vs Hybrid RRF benchmark).
  - `python fact_check_cli.py --claim "..." --export report.json` (Exports full JSON audit report).

#### 3. `generate_presentation.py`
- **Purpose:** Programmatic script using `python-pptx` to generate the 16:9 widescreen presentation deck.
- **Key Features:** Replaced all blurry AI screenshots with native vector cards, tables, and structured typography matching the exact rubric headings.

---

### 🤖 Autonomous Agents (`src/agents/`)

#### 4. `src/agents/claim_agent.py`
- **Function:** `normalize_claim(raw_claim: str) -> List[str]`
- **Purpose:** Decomposes a raw, complex claim into 1–3 atomic, testable sub-claims using Groq (`qwen/qwen3.8-27b`) or a deterministic conjunction parser.
- **Why It Matters:** Prevents multi-hop retrieval errors by clarifying individual assertions.

#### 5. `src/agents/pro_agent.py`
- **Function:** `argue_pro(claim, evidence_pool, prior_turns) -> Dict[str, Any]`
- **Purpose:** Formulates affirmative queries, retrieves web evidence, attaches domain credibility tiers, and synthesizes a supporting argument citing `[Ex]` tags.
- **Input:** Claim string, shared `evidence_pool`, and prior debate transcript.
- **Output:** Stance dict containing argument text and list of cited evidence IDs.

#### 6. `src/agents/con_agent.py`
- **Function:** `argue_con(claim, evidence_pool, prior_turns) -> Dict[str, Any]`
- **Purpose:** Formulates adversarial refuting queries, surfaces counter-evidence/risks, and constructs an argument attacking the Pro agent's vulnerabilities.
- **Input:** Claim string, shared `evidence_pool`, and prior debate transcript.
- **Output:** Stance dict containing counter-argument text and list of cited counter-evidence IDs.

#### 7. `src/agents/cross_examiner.py` *(Novel Innovation)*
- **Function:** `cross_examine(claim, sub_claims, pro_turns, con_turns, evidence_pool) -> Dict[str, Any]`
- **Purpose:** Impartial dialectical auditor that audits debater turns for formal logical fallacies (**Correlation vs. Causation, Hasty Generalization, False Dichotomy, Selection Bias**) and synthesizes **Points of Consensus** vs. **Points of Contention**.
- **Output:** Synthesis dict passed directly to the Supreme Judge to prevent confirmation bias.

#### 8. `src/agents/verify.py`
- **Function:** `verify_citations(pro_turns, con_turns, evidence_pool) -> Dict[str, Any]`
- **Purpose:** Deterministic regex citation guardrail that intercepts every `[Ex]` tag in debater turns and verifies it against the `evidence_pool` registry.
- **Output:** Report flagging valid vs. hallucinated citations and generating warning notices.

#### 9. `src/agents/judge_agent.py`
- **Function:** `judge(claim, sub_claims, pro_turns, con_turns, evidence_pool, cross_examination) -> Dict[str, Any]`
- **Purpose:** Impartial judicial arbitrator powered by `openai/gpt-oss-120b` (or calibrated fallback). Ingests transcript, verified evidence, source credibility tiers, and cross-examination audit to produce calibrated verdicts (`TRUE`, `FALSE`, `UNVERIFIABLE`) with explicit confidence and uncertainty notes.

#### 10. `src/agents/groq_client.py`
- **Function:** `call_groq_with_retry(model, prompt, temperature, max_retries, fallback_model)`
- **Purpose:** Wraps Groq API calls with automatic exponential backoff retry on HTTP 429 rate limits and model fallback.

---

### 🕸️ Graph Orchestration (`src/graph/`)

#### 11. `src/graph/state.py`
- **Definition:** `DebateState` (`TypedDict`)
- **Purpose:** The centralized, immutable state contract that flows through every node in the LangGraph state machine.

#### 12. `src/graph/debate_graph.py`
- **Functions:** `build_debate_graph()`, `get_debate_graph()`, `run_debate(claim, max_rounds)`
- **Purpose:** Assembles the multi-agent pipeline using LangGraph `StateGraph`. Defines the nodes (`normalize`, `pro_turn`, `con_turn`, `advance_round`, `cross_examine`, `judge`) and conditional routing logic.

---

### 🔍 Retrieval & Source Authority (`src/retrieval/`)

#### 13. `src/retrieval/source_scorer.py` *(Novel Innovation)*
- **Functions:** `score_source_credibility(url, title, snippet)`, `enrich_evidence_pool_with_credibility()`
- **Purpose:** Normalizes domain URLs and assigns epistemic credibility weights ($R \in [0.1, 1.0]$) and authority tiers:
  - Tier 1: Peer-reviewed journals and government agencies ($0.95–0.98$).
  - Tier 2: Verified international wires and encyclopedias ($0.80–0.90$).
  - Tier 3: General web media ($0.65–0.75$).
  - Tier 4: Community forums and unvetted blogs ($0.30–0.50$).

#### 14. `src/retrieval/web_search.py`
- **Functions:** `search(query, max_results)`, `search_tavily()`, `search_ddgs()`, `search_offline_fallback()`
- **Purpose:** Multi-tier resilient search pipeline. Uses Tavily, falls back to DuckDuckGo, and includes an in-memory session cache and grounded benchmark knowledge base to guarantee 100% demo safety and sub-second execution.

#### 15. `src/retrieval/hybrid_search.py`
- **Functions:** `bm25_search()`, `build_faiss_index()`, `dense_search()`, `reciprocal_rank_fusion()`, `hybrid_search()`
- **Purpose:** Implements sparse lexical retrieval (BM25), dense semantic vector search (FAISS IndexFlatIP / scikit-learn cosine matrix), and merges them using Reciprocal Rank Fusion (RRF with $c=60$).

---

### 🧪 Evaluation & Testing (`eval/` & `tests/`)

#### 16. `eval/run_eval.py`
- **Purpose:** Automated evaluation harness that runs all 5 benchmark scenarios from `test_claims.json`, validates verdicts against ground truth, and checks that ambiguous claims hedge confidence below allowed thresholds.

#### 17. `eval/test_claims.json`
- **Purpose:** Dataset containing 5 diverse real-world evaluation scenarios: Clear False, Clear True, Genuinely Ambiguous, Misleading Context, and Time-Sensitive.

#### 18. `tests/test_graph.py`
- **Purpose:** Pytest test suite verifying:
  1. `test_claim_decomposition` (Sub-claim atomicity).
  2. `test_verify_citations_clean` (Valid citations pass).
  3. `test_verify_citations_hallucinated_injection` (Fake `[E99]` citations trigger guardrail and penalty).
  4. `test_source_credibility_scorer` (Domain tiering).
  5. `test_cross_examiner_fallacies_and_synthesis` (Fallacy detection).
  6. `test_full_debate_graph_execution` (End-to-end StateGraph execution).

---

## 3. Inter-File Dependency Diagram

```
app/streamlit_app.py ──┐
fact_check_cli.py ────┼──► src/graph/debate_graph.py
eval/run_eval.py ─────┘             │
                                    ├──► src/graph/state.py
                                    │
                                    ├──► src/agents/claim_agent.py
                                    ├──► src/agents/pro_agent.py ──────┐
                                    ├──► src/agents/con_agent.py ──────┼──► src/retrieval/web_search.py
                                    ├──► src/agents/cross_examiner.py  │          │
                                    ├──► src/agents/verify.py          │          ▼
                                    └──► src/agents/judge_agent.py     └──► src/retrieval/source_scorer.py
                                                │
                                                ▼
                                         src/agents/groq_client.py
```
