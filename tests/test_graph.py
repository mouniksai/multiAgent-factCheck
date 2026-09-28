import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.agents.claim_agent import normalize_claim
from src.agents.verify import verify_citations
from src.agents.cross_examiner import cross_examine, detect_rule_based_fallacies
from src.retrieval.source_scorer import score_source_credibility, enrich_evidence_pool_with_credibility
from src.agents.judge_agent import judge
from src.graph.debate_graph import run_debate


def test_claim_decomposition():
    sub_claims = normalize_claim("Moderate coffee consumption reduces mortality and improves focus.")
    assert isinstance(sub_claims, list)
    assert len(sub_claims) >= 1


def test_verify_citations_clean():
    evidence_pool = {
        "E1": {"title": "Study 1", "url": "https://example.com/1", "snippet": "Evidence 1 snippet."},
        "E2": {"title": "Study 2", "url": "https://example.com/2", "snippet": "Evidence 2 snippet."}
    }
    pro_turns = [{"round": 1, "argument": "Supports claim [E1].", "cited_evidence_ids": ["E1"]}]
    con_turns = [{"round": 1, "argument": "Challenges claim [E2].", "cited_evidence_ids": ["E2"]}]

    report = verify_citations(pro_turns, con_turns, evidence_pool)
    assert report["is_clean"] is True
    assert "E1" in report["valid_citations"]
    assert "E2" in report["valid_citations"]
    assert len(report["hallucinated_citations"]) == 0


def test_verify_citations_hallucinated_injection():
    """
    Step 7 Guardrail Checkpoint: Manually inject fake evidence ID [E99] and assert
    that verify_citations flags the hallucination and judge incorporates guardrail warning.
    """
    evidence_pool = {
        "E1": {"title": "Study 1", "url": "https://example.com/1", "snippet": "Evidence 1 snippet."}
    }
    pro_turns = [{"round": 1, "argument": "Supports claim with fake study [E99].", "cited_evidence_ids": ["E99"]}]
    con_turns = [{"round": 1, "argument": "Valid challenge [E1].", "cited_evidence_ids": ["E1"]}]

    report = verify_citations(pro_turns, con_turns, evidence_pool)
    assert report["is_clean"] is False
    assert len(report["hallucinated_citations"]) == 1
    assert report["hallucinated_citations"][0]["cited_id"] == "E99"

    # Test judge reaction to hallucinated citation
    verdict = judge(
        claim="Test claim",
        sub_claims=["Test sub-claim"],
        pro_turns=pro_turns,
        con_turns=con_turns,
        evidence_pool=evidence_pool
    )
    assert verdict["guardrail_report"]["is_clean"] is False
    assert verdict["confidence"] <= 65
    assert "GUARDRAIL" in verdict["rationale"] or "uncited" in verdict["rationale"] or "hallucinated" in verdict["rationale"].lower() or "unverified" in verdict["uncertainty_note"].lower()


def test_source_credibility_scorer():
    """Validates epistemic tiering and domain authority weighting."""
    t1 = score_source_credibility("https://www.nature.com/articles/s41586-021")
    assert t1["credibility_score"] >= 0.95
    assert t1["is_authoritative"] is True
    assert "Tier-1" in t1["tier_label"]

    t1_gov = score_source_credibility("https://www.cdc.gov/heartdisease/facts.htm")
    assert t1_gov["credibility_score"] >= 0.95
    assert t1_gov["is_authoritative"] is True

    t2 = score_source_credibility("https://www.reuters.com/business/healthcare")
    assert t2["credibility_score"] >= 0.85
    assert "Tier-2" in t2["tier_label"]

    t4 = score_source_credibility("https://www.reddit.com/r/science/comments/123")
    assert t4["credibility_score"] <= 0.40
    assert t4["is_authoritative"] is False


def test_cross_examiner_fallacies_and_synthesis():
    """Validates dialectical cross-examination and reasoning fallacy identification."""
    pro_arg = "This pilot cohort proves that everyone will always be cured resulting directly from caffeine."
    con_arg = "Observational data shows either it is completely lethal or entirely benign."
    
    fallacies = detect_rule_based_fallacies(pro_arg, con_arg)
    assert len(fallacies) >= 1
    
    pro_turns = [{"round": 1, "argument": pro_arg, "cited_evidence_ids": ["E1"]}]
    con_turns = [{"round": 1, "argument": con_arg, "cited_evidence_ids": ["E2"]}]
    evidence_pool = {
        "E1": {"title": "Harvard Cohort", "url": "https://www.hsph.harvard.edu/1", "snippet": "Study", "credibility_score": 0.94},
        "E2": {"title": "Lancet Review", "url": "https://www.thelancet.com/2", "snippet": "Trial", "credibility_score": 0.97}
    }
    
    cx = cross_examine("Moderate coffee consumption", ["Sub-claim 1"], pro_turns, con_turns, evidence_pool)
    assert "consensus_points" in cx
    assert "contention_points" in cx
    assert "synthesis_summary" in cx
    assert len(cx["consensus_points"]) >= 1


def test_full_debate_graph_execution():
    state = run_debate("Regular exercise reduces the risk of cardiovascular disease.", max_rounds=1)
    assert "claim" in state
    assert len(state["sub_claims"]) >= 1
    assert len(state["pro_turns"]) >= 1
    assert len(state["con_turns"]) >= 1
    assert isinstance(state["evidence_pool"], dict)
    assert state.get("cross_examination") is not None
    assert state["verdict"] is not None
    assert "verdict" in state["verdict"]
    assert "confidence" in state["verdict"]
    assert "rationale" in state["verdict"]
    assert "total_seconds" in state["latency_log"]
