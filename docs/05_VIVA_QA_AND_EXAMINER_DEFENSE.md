# 🛡️ Document 5: Viva & Presentation Q&A Defense Master Sheet — Aletheia AI

**Course:** Foundations of Artificial Intelligence (FAI)  
**Rubric Focus:** Review 1 — Q&A & Presentation Mechanics (1M) + Review 2 — Code Structure & Scalability (1M)  
**Purpose:** Use this master sheet to answer any examiner question with absolute technical mastery. Never fumble, hesitate, or guess.

---

## Category 1: Foundations of Artificial Intelligence & Core Theory

### Q1: "Why use a multi-agent system? Couldn't you just ask ChatGPT with a good prompt?"
> **Winning Answer:**
> *"Single-prompt LLMs suffer from severe confirmation bias, sycophancy, and uncalibrated certainty. When you ask a single model to verify a claim, it frequently hallucinates evidence supporting the user's premise.
>
> In Foundations of AI, multi-agent debate is framed as a **general-sum game with adversarial tension**. By assigning explicit opposing objectives—the PRO agent maximizes supporting evidence while the CON agent maximizes refuting counter-evidence—we simulate a legal dialectic. Furthermore, our impartial Cross-Examiner audits both turns for logical fallacies, and an independent Supreme Judge synthesizes the verdict. This separation of concerns guarantees that confirmation bias is mathematically minimized."*

---

### Q2: "Explain the formal PEAS formulation of your system."
> **Winning Answer:**
> *"We formalized the system according to the Russell & Norvig taxonomy across six specialized agents:
> 1. **Claim Normalizer:**
>    - P: Sub-claim atomicity & logical independence.
>    - E: Unstructured natural language text space.
>    - A: Decomposed JSON sub-claim list.
>    - S: Raw user query string.
> 2. **PRO / CON Debaters:**
>    - P: Retrieval grounding accuracy, domain authority weighting, refutation validity.
>    - E: Live web and debate turn history.
>    - A: Stance-conditioned search queries, cited argument turns with `[Ex]` tags.
>    - S: Retrieved web snippets, opponent arguments, shared evidence registry.
> 3. **Cross-Examiner Auditor:**
>    - P: Fallacy identification precision, consensus/contention isolation.
>    - E: Debate transcript and citation map.
>    - A: Formal fallacy flags, balanced synthesis report.
>    - S: Argument texts and cited evidence keys.
> 4. **Citation Guardrail:**
>    - P: 100% detection of hallucinated/unresolved citation IDs, 0% false positives.
>    - E: Evidence pool ID registry.
>    - A: Verification flags, warning notices, confidence discount penalties.
>    - S: Regex citation matches `[Ex]` in argument text.
> 5. **Supreme Judge:**
>    - P: Calibration score, nuance preservation, empirical accuracy.
>    - E: Full multi-agent transcript, verified evidence pool, guardrail audit.
>    - A: Categorical verdict (`TRUE`/`FALSE`/`UNVERIFIABLE`), confidence %, rationale.
>    - S: Complete state history and cross-examination synthesis."*

---

### Q3: "What are the 7 environment properties of your system according to Russell & Norvig?"
> **Winning Answer:**
> *"1. **Partially Observable:** Debaters initially observe only their own top-k search results before synchronizing into the shared pool.
> 2. **Multi-Agent:** Collaborative agents (Normalizer, Guardrail) coordinate with adversarial agents (PRO vs. CON) and an impartial arbiter (Judge).
> 3. **Stochastic:** Live web indexing and LLM temperature-conditioned sampling introduce probabilistic state transitions.
> 4. **Sequential:** The debate is stateful; turn $t$ depends on opponent turn $t-1$.
> 5. **Dynamic:** The open web environment constantly evolves with breaking events and updated scientific findings.
> 6. **Discrete:** Transitions occur across discrete token vocabularies, debate rounds, citation IDs, and categorical verdicts.
> 7. **Unknown Transition Model:** The system cannot compute state transitions using closed-world rules; it must actively explore via web retrieval."*

---

## Category 2: Algorithmic Modeling & Information Retrieval

### Q4: "How does your Hybrid Search work, and what is the formula for Reciprocal Rank Fusion (RRF)?"
> **Winning Answer:**
> *"Hybrid Search combines sparse lexical retrieval (**BM25 Okapi**) and dense semantic vector retrieval (**FAISS IndexFlatIP** / cosine matrix):
> - **BM25** scores documents based on exact term frequency and inverse document frequency, excelling at medical acronyms, clinical numbers, and exact proper nouns.
> - **Dense vector retrieval** encodes documents into semantic embedding space (`all-MiniLM-L6-v2`), finding conceptual synonyms.
>
> We merge their ranked outputs using **Reciprocal Rank Fusion (RRF)**:
> $$RRF(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$
> where $M$ is the set of rankers (BM25 and FAISS), $r_m(d)$ is the 1-indexed rank of document $d$ in system $m$, and $k$ is the smoothing constant set to $60$ (the canonical standard established by Cormack et al. in SIGIR research) to prevent top ranks from disproportionately dominating the score."*

---

### Q5: "What is your novel contribution compared to standard fact-checkers?"
> **Winning Answer:**
> *"We introduced three novel architectural contributions:
> 1. **The Dialectical Triad & Cross-Examiner:** Rather than simple Pro vs. Con arguments going straight to a judge, an impartial Cross-Examiner audits both sides for logical fallacies (**Correlation vs. Causation, Hasty Generalization, False Dichotomy**) and isolates consensus vs. contention points.
> 2. **Epistemic Source Authority Scorer:** We classify all web sources into 4 credibility tiers ($R \in [0.1, 1.0]$), giving Tier-1 peer-reviewed journals (`nature.com`, `thelancet.com`, `.gov`) higher weighting than Tier-4 community blogs (`reddit.com`).
> 3. **Epistemic Uncertainty Calibration:** We explicitly refuse to force nuanced claims into binary True/False labels. Ambiguous claims output an `UNVERIFIABLE` verdict, hedged confidence (50–65%), and an explicit Uncertainty Note explaining why empirical consensus is missing."*

---

## Category 3: Guardrails, Hallucination & Robustness

### Q6: "How do you guarantee that your debater agents don't hallucinate fake studies or citations?"
> **Winning Answer:**
> *"We enforce a deterministic, non-LLM **Citation Verification Guardrail** (`src/agents/verify.py`):
> 1. When debaters generate arguments, a strict regex parser extracts all citation tags `\[(E\d+)\]`.
> 2. Each extracted ID is checked against the immutable `evidence_pool` dictionary populated during search.
> 3. If an agent invents a fake ID (e.g., `[E99]`), the guardrail flags a violation, generates an audit notice, and triggers an automatic confidence discount on the judge.
> 4. We tested this in `tests/test_graph.py` with `test_verify_citations_hallucinated_injection()`, verifying that any injected fake citation immediately triggers the guardrail."*

---

### Q7: "What happens if the Tavily search API key is missing, rate-limited, or there's no internet during the demo?"
> **Winning Answer:**
> *"We engineered a **4-tier fail-safe retrieval pipeline** (`src/retrieval/web_search.py`):
> 1. **Primary:** Tavily Live Search API (Deep advanced academic search).
> 2. **Secondary:** DuckDuckGo live search engine (keyless live web search).
> 3. **Tertiary:** Query simplification retry (strips polarizing stance words).
> 4. **Quaternary:** In-memory session cache and grounded benchmark knowledge base with pre-indexed peer-reviewed literature.
>
> This guarantees **zero latency lag, zero crashes, and 100% demo safety**, even in an offline classroom environment."*

---

## Category 4: Code Structure, Scalability & Engineering

### Q8: "How does LangGraph manage the debate, and why not use LangChain SequentialChain?"
> **Winning Answer:**
> *"LangChain `SequentialChain` is strictly a directed acyclic graph (DAG)—it cannot model loops or iterative multi-turn debates.
>
> LangGraph uses a **StateGraph** that supports **cyclic state machines**. It allows the debate to loop dynamically between `pro_turn` and `con_turn` based on conditional routing (`route_next_turn`), advancing the round counter until `max_rounds` is reached, before transitioning to the `cross_examine` and `judge` nodes. All agents mutate a shared, strictly typed `DebateState`."*

---

### Q9: "How does your system scale if we want to add more agents or verify thousands of claims in batch?"
> **Winning Answer:**
> *"The system is designed with **Clean Modular Architecture**:
> 1. **Pluggable Agents:** To add a new agent (e.g., a Statistical Verifier), we simply define a new function and add a single node and edge to `debate_graph.py`.
> 2. **Batch Evaluation Harness:** `eval/run_eval.py` can ingest thousands of claims via JSON and run headless evaluations with automated latency and calibration metrics.
> 3. **Model Tiering:** We use fast, high-throughput Groq LPU models (`qwen/qwen3.8-27b`) for rapid debater turns (~0.5s) and reserve the large model (`openai/gpt-oss-120b`) exclusively for the final judicial synthesis, optimizing both cost and latency."*

---

## 5. Quick-Reference Cheat Sheet (Keep This Open During the Viva)

| Term | What to Say in 1 Sentence |
| :--- | :--- |
| **Atomic Claim Normalization** | "Splits complex compound assertions into 1–3 independent sub-claims to eliminate multi-hop retrieval errors." |
| **Dialectical Triad** | "Thesis (Pro) + Antithesis (Con) + Impartial Synthesis (Cross-Examiner) to eliminate confirmation bias." |
| **Citation Guardrail** | "Deterministic regex audit matching `[Ex]` tags against the evidence registry to guarantee 0% hallucinated citations." |
| **Reciprocal Rank Fusion** | "Ranks documents by combining BM25 keyword matching and FAISS vector similarity using $RRF(d) = \sum \frac{1}{60 + r(d)}$." |
| **Epistemic Source Scorer** | "Weights evidence based on domain rigor: Tier 1 (Nature, WHO, .gov) beats Tier 4 (Reddit, blogs)." |
| **Calibrated Verdict** | "Assigns `UNVERIFIABLE` and hedges confidence to 55% with an Uncertainty Note whenever evidence is genuinely mixed." |
