import os
import json
import pytest
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.retrieval.web_search import OFFLINE_BENCHMARK_KNOWLEDGE
from src.graph.debate_graph import run_debate


def test_test_claims_schema_and_integrity():
    """Validates that test_claims.json is properly formatted with required fields."""
    claims_path = os.path.join(os.path.dirname(__file__), "..", "eval", "test_claims.json")
    assert os.path.exists(claims_path), f"Missing {claims_path}"

    with open(claims_path, "r", encoding="utf-8") as f:
        claims = json.load(f)

    assert isinstance(claims, list)
    assert len(claims) >= 10, "Expected at least 10 benchmark test claims"

    valid_verdicts = {"true", "false", "unverifiable"}
    for sc in claims:
        assert "id" in sc
        assert "category" in sc
        assert "claim" in sc and len(sc["claim"]) > 10
        assert sc["expected_verdict"].lower() in valid_verdicts
        assert "expected_max_confidence" in sc


def test_offline_knowledge_coverage():
    """Ensures offline knowledge base covers core scientific myth topics for demo resilience."""
    required_topics = ["brain", "vaccin", "knuckle", "carrot", "sugar", "fasting", "coffee", "exercise"]
    for topic in required_topics:
        assert topic in OFFLINE_BENCHMARK_KNOWLEDGE, f"Missing topic fallback: {topic}"
        entries = OFFLINE_BENCHMARK_KNOWLEDGE[topic]
        assert len(entries) >= 2, f"Expected at least 2 evidence entries for {topic}"
        for item in entries:
            assert "url" in item
            assert "title" in item
            assert "snippet" in item


def test_brain_myth_benchmark_claim():
    """Tests the viral 10% brain myth claim through the debate pipeline."""
    state = run_debate("Humans only use 10% of their brains.", max_rounds=1)
    verdict = state.get("verdict", {})
    assert verdict.get("verdict") == "false"
    assert verdict.get("confidence", 0) >= 70
    guardrail = verdict.get("guardrail_report", {})
    assert guardrail.get("is_clean") is True
