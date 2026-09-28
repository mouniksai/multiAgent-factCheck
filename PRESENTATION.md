# Aletheia AI — Dialectical Multi-Agent Fact Verification
## Foundations of Artificial Intelligence — Case Study Review Presentation

---

### Slide 1: Title Slide

**Title:** Aletheia: Dialectical Multi-Agent Fact-Checking Framework  
**Subtitle:** Adversarial RAG, Epistemic Calibration, and Citation Integrity  
**Course:** Foundations of Artificial Intelligence  
**Presented by:**  
- [Team Member 1] — [Roll Number]  
- [Team Member 2] — [Roll Number]  
- [Team Member 3] — [Roll Number]  

---

### Slide 2: Multi-Agent RAG for Reliable Claim Verification

- A multi-agent Retrieval-Augmented Generation (RAG) framework designed to verify factual claims using live empirical web evidence.
- The system normalizes raw assertions into atomic, independent sub-claims to eliminate multi-hop retrieval errors and query ambiguity.
- PRO and CON debater agents independently execute stance-conditioned web retrieval to construct grounded arguments and counter-arguments in iterative adversarial rounds.
- An impartial Cross-Examiner agent audits debater turns for formal reasoning fallacies and isolates empirical consensus from active points of contention.
- A deterministic Citation Guardrail validates that every cited source tag corresponds to a verified record in the shared evidence pool before arbitration.
- An independent Supreme Judge model weighs verified evidence and domain credibility to output an epistemically calibrated verdict with explicit uncertainty boundaries.

---

### Slide 3: PEAS Formulation:

| Agent | Performance Measure (P) | Environment (E) | Actuators (A) | Sensors (S) |
| :--- | :--- | :--- | :--- | :--- |
| **Claim Normalizer** | Sub-claim atomicity, logical independence, precision | Raw / unstructured natural language claims | Decomposed atomic sub-claims (JSON) | User claim string |
| **PRO Debater** | Evidence relevance, citation precision, domain authority | Live Web, debate transcript history | Supporting queries, cited argument turns `[Ex]` | Search results, evidence pool, CON turns |
| **CON Debater** | Counter-evidence validity, refutation rigor | Live Web, debate transcript history | Refuting queries, counter-arguments `[Ex]` | Search results, evidence pool, PRO turns |
| **Cross-Examiner** | Fallacy detection rate, dialectical synthesis neutrality | Multi-turn debate history, evidence registry | Consensus/contention map, fallacy audit report | Debater turns, pool keys, citation mapping |
| **Citation Guardrail** | 100% citation validation, 0% hallucination tolerance | Evidence pool registry, argument text | Verification audit, confidence discount notices | Citation tags `[Ex]`, evidence registry keys |
| **Supreme Judge** | Verdict accuracy, epistemic calibration, nuance preservation | Full transcript, verified evidence, audit report | `TRUE` / `FALSE` / `UNVERIFIABLE` + rationale | State history, synthesis report, guardrail audit |

---

### Slide 4: Environment & Agent Analysis:

| Property | Our Implementation & Formal Rationale |
| :--- | :--- |
| **Stochastic** | Web retrieval latencies and temperature-conditioned LLM sampling produce probabilistic transitions rather than deterministic outputs. |
| **Partially Observable** | Debaters initially observe only their own top-k retrieved evidence subsets prior to evidence pool synchronization. |
| **Sequential** | Each debate round depends on previous PRO and CON argumentation history, building a stateful dialectic over time. |
| **Dynamic** | The open-web environment continuously evolves as breaking news, updated clinical trials, and revision histories emerge. |
| **Multi-Agent** | Multiple specialized autonomous agents collaborate (Normalizer, Guardrail) and compete (PRO vs. CON) to verify claims. |
| **Mixed Cooperative–Competitive** | PRO and CON compete adversarially to stress-test claims, while Cross-Examiner and Judge cooperate toward factual verification. |
| **Discrete** | The state space transitions across discrete token sequences, debate rounds, numbered citation IDs, and categorical verdicts. |

---

### Slide 5: Multi-Agent Architecture & System Flow

| Agent | Role | Interaction & Coordination |
| :--- | :--- | :--- |
| **Claim Normalizer** | Decomposes compound claims into atomic sub-claims | Dispatches normalized sub-claims to PRO and CON debaters |
| **PRO Debater** | Discovers supporting empirical evidence via search | Challenges CON arguments; registers supporting citations `[Ex]` |
| **CON Debater** | Discovers refuting empirical counter-evidence via search | Challenges PRO arguments; registers counter-citations `[Ex]` |
| **Cross-Examiner** | Audits reasoning fallacies & dialectical synthesis | Extracts points of consensus vs. contention for the Supreme Judge |
| **Citation Guardrail** | Validates 100% of cited evidence IDs | Cross-checks argument text tags against registry keys; flags hallucinated IDs |
| **Supreme Judge** | Makes final evidence-based calibrated decision | Produces final categorical verdict + confidence score + uncertainty note |

**System Flow:**  
$$\text{Claim} \longrightarrow \text{Normalize} \longrightarrow [\text{PRO} \longleftrightarrow \text{CON Debate Loop}] \longrightarrow \text{Cross-Examine} \longrightarrow \text{Verify Citations} \longrightarrow \text{Supreme Judge} \longrightarrow \text{Calibrated Verdict}$$

---

### Slide 6: Algorithmic Modeling & Search Strategy:

| Component | Algorithm / Technique | Purpose & Algorithmic Guarantee |
| :--- | :--- | :--- |
| **Claim Decomposition** | Atomic Sub-Claim Normalization | Breaks complex compound assertions into 1–3 independent claims to prevent multi-hop retrieval failure. |
| **Query Generation** | Stance-Conditioned Reformulation | Generates distinct polarized query vectors targeting affirmative literature vs. refuting clinical counter-evidence. |
| **Information Retrieval** | Hybrid Search (BM25 + FAISS Dense + RRF) | Combines sparse lexical matching and dense vector similarity using Reciprocal Rank Fusion ($k=60$). |
| **Source Credibility** | Epistemic Authority Scorer | Evaluates domain TLDs and assigns reliability weights ($R \in [0.1, 1.0]$) to academic, government, wire, and blog sources. |
| **Adversarial Reasoning** | Cyclic StateGraph (LangGraph) | Orchestrates stateful, multi-round dialectical debate turns with immutable shared state persistence. |
| **Fallacy Auditing** | Rule-Based + LLM Cross-Examination | Detects Correlation vs. Causation, Hasty Generalization, and False Dilemma fallacies across turns. |
| **Citation Verification** | Deterministic Evidence-ID Matching | Regex validates all `[Ex]` citations against the evidence pool, ensuring zero hallucinated source references. |
| **Final Decision** | Calibrated Epistemic Judge | Weighs source credibility, evidence volume, and fallacy penalties to calibrate confidence (hedging ambiguous claims). |

---

### Slide 7: Tool/Package:

| Tool / Package | Purpose in the Project |
| :--- | :--- |
| **Python 3.11** | Core programming language for multi-agent state orchestration, typing, and benchmarking. |
| **LangGraph** | Builds the cyclic multi-agent debate and cross-examination workflow using `StateGraph`. |
| **Groq LPU Engine** | Provides high-speed LLM inference (`openai/gpt-oss-120b` for judge, `qwen/qwen3.8-27b` for debaters). |
| **Tavily & DDGS** | Performs live web search with multi-tier fallback resilience for empirical evidence retrieval. |
| **FAISS & scikit-learn** | Dense vector similarity search and cosine matrix indexing for semantic retrieval. |
| **Rank-BM25** | Implements BM25 Okapi sparse lexical retrieval for exact terminology matching. |
| **Streamlit** | Executive interactive multi-tab web dashboard for real-time claim verification and benchmarking. |
| **Pydantic** | Enforces structured schema validation and data integrity for agent state transitions. |
| **pytest** | Automated test suite verifying claim decomposition, guardrail checkpoints, and graph execution. |

---

### Slide 8: Multi-Agent Execution & Interaction:

#### Architecture & Orchestration Overview:
```
                      ┌──────────────────────────────────────┐
                      │          Raw Claim Input             │
                      └──────────────────┬───────────────────┘
                                         ▼
                      ┌──────────────────────────────────────┐
                      │    Claim Normalization Agent         │
                      │    Decomposes into Atomic Claims     │
                      └──────────────────┬───────────────────┘
                                         ▼
         ┌───────────────────────────────────────────────────────────────┐
         │              Adversarial Debate Arena (StateGraph)            │
         │                                                               │
         │   ┌─────────────────────┐          ┌─────────────────────┐    │
         │   │   PRO Debater       │◄────────►│   CON Debater       │    │
         │   │   Supporting Stance │          │   Refuting Stance   │    │
         │   └──────────┬──────────┘          └──────────┬──────────┘    │
         │              │                                │               │
         │              └───────────────┬────────────────┘               │
         │                              ▼                                │
         │                 Shared Evidence Pool (Hybrid RRF)             │
         └──────────────────────────────┬────────────────────────────────┘
                                        ▼
                      ┌──────────────────────────────────────┐
                      │      Cross-Examiner Auditor          │
                      │   Fallacy Detection & Consensus      │
                      └──────────────────┬───────────────────┘
                                         ▼
                      ┌──────────────────────────────────────┐
                      │     Citation Integrity Guardrail     │
                      │     Deterministic [Ex] Validation    │
                      └──────────────────┬───────────────────┘
                                         ▼
                      ┌──────────────────────────────────────┐
                      │       Supreme Judicial Model         │
                      │  Weighs Evidence & Calibrates Score  │
                      └──────────────────┬───────────────────┘
                                         ▼
                      ┌──────────────────────────────────────┐
                      │      Calibrated Verdict Output       │
                      │ Verdict + Confidence % + Uncertainty │
                      └──────────────────────────────────────┘
```

#### Core Interaction Principles:
- **Shared State Architecture:** Agents communicate strictly via an immutable `DebateState` TypedDict managed by LangGraph.
- **Dialectical Triad:** Pairing adversarial debaters with an impartial cross-examiner eliminates confirmation bias and grounds arguments in empirical evidence.
- **Zero Hallucination Guarantee:** The deterministic Citation Guardrail intercepts ungrounded citations before judicial deliberation.

---

### Slide 9: Output: Demo Quality & Testing Scenarios

#### Empirical Benchmark Matrix (100% Pass Rate):

| Scenario | Category | Claim Statement | Expected | Output Verdict | Calibrated Conf. | Guardrail Audit |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: |
| **1** | Clear False | The Great Wall of China is visible from space with the naked eye. | `FALSE` | `FALSE` | 95% | Clean (100% Grounded) |
| **2** | Clear True | Regular exercise reduces the risk of cardiovascular disease. | `TRUE` | `TRUE` | 92% | Clean (100% Grounded) |
| **3** | Ambiguous | Moderate coffee consumption increases the risk of heart disease. | `UNVERIFIABLE` | `UNVERIFIABLE` | 55% | Clean (Uncertainty Note) |
| **4** | Misleading | Global average temperature increase of 1.5C has no impact on weather. | `FALSE` | `FALSE` | 94% | Clean (100% Grounded) |
| **5** | Time-Sensitive | Global lithium ion battery production volume doubled in 24 months. | `UNVERIFIABLE` | `UNVERIFIABLE` | 62% | Clean (Nuance Note) |

#### Key Calibration Takeaway:
- Ambiguous or evolving claims do not artificially collapse into binary True/False; the system hedges confidence to 50–65% and provides an explicit **Uncertainty Advisory Note**.
- Injected hallucinated citations (`[E99]`) trigger an immediate guardrail violation and an automatic confidence discount.
