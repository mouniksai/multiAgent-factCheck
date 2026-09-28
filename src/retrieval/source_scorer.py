"""
Source Credibility & Epistemic Authority Scorer
===============================================
Evaluates domain authorities, top-level domains (TLDs), and institutional
origins for web evidence to compute an objective reliability weight R in [0.0, 1.0].
"""

import re
from urllib.parse import urlparse
from typing import Dict, Any, Tuple

# Domain classification database with epistemic reliability weights
TIER_1_DOMAINS = {
    # Peer-reviewed & Academic institutions
    "nature.com": (0.98, "Tier-1 Peer-Reviewed Journal"),
    "science.org": (0.98, "Tier-1 Peer-Reviewed Journal"),
    "cell.com": (0.97, "Tier-1 Peer-Reviewed Journal"),
    "thelancet.com": (0.97, "Tier-1 Peer-Reviewed Journal"),
    "nejm.org": (0.97, "Tier-1 Medical Journal"),
    "sciencedirect.com": (0.95, "Tier-1 Academic Repository"),
    "nih.gov": (0.98, "Tier-1 Institutional / NIH"),
    "ncbi.nlm.nih.gov": (0.98, "Tier-1 PubMed / Medline"),
    "cdc.gov": (0.96, "Tier-1 Government Health Agency"),
    "who.int": (0.96, "Tier-1 Global Health Organization"),
    "nasa.gov": (0.98, "Tier-1 Government Space & Science"),
    "ieee.org": (0.95, "Tier-1 Scientific Society"),
    "arxiv.org": (0.90, "Tier-1 Academic Preprint Archive"),
}

TIER_2_DOMAINS = {
    # High-standard fact-checkers & international news agencies
    "reuters.com": (0.90, "Tier-2 Verified International Wire"),
    "apnews.com": (0.90, "Tier-2 Verified International Wire"),
    "bbc.com": (0.88, "Tier-2 Public Broadcaster"),
    "bbc.co.uk": (0.88, "Tier-2 Public Broadcaster"),
    "nytimes.com": (0.85, "Tier-2 Major News Organization"),
    "wsj.com": (0.85, "Tier-2 Major News Organization"),
    "economist.com": (0.86, "Tier-2 Investigative Journal"),
    "scientificamerican.com": (0.89, "Tier-2 Science Journalism"),
    "snopes.com": (0.88, "Tier-2 Dedicated Fact-Checker"),
    "politifact.com": (0.88, "Tier-2 Dedicated Fact-Checker"),
    "factcheck.org": (0.90, "Tier-2 Verified Fact-Checker"),
    "wikipedia.org": (0.80, "Tier-2 Curated Collaborative Encyclopedia"),
    "britannica.com": (0.87, "Tier-2 Verified Encyclopedia"),
}

TIER_4_DOMAINS = {
    # User-generated / social / forums / unverified blogs
    "reddit.com": (0.35, "Tier-4 Community Forum"),
    "twitter.com": (0.30, "Tier-4 Social Media"),
    "x.com": (0.30, "Tier-4 Social Media"),
    "facebook.com": (0.30, "Tier-4 Social Media"),
    "quora.com": (0.35, "Tier-4 Community Q&A"),
    "medium.com": (0.50, "Tier-4 Unvetted Blog"),
    "substack.com": (0.55, "Tier-4 Independent Newsletter"),
}


def extract_domain(url: str) -> str:
    """Extracts normalized hostname from a URL."""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        if domain.startswith("www."):
            domain = domain[4:]
        # Remove port if present
        domain = domain.split(":")[0]
        return domain
    except Exception:
        return ""


def score_source_credibility(url: str, title: str = "", snippet: str = "") -> Dict[str, Any]:
    """
    Computes an epistemic credibility score, authority tier, and badge for a source.
    Returns:
        dict: {
            "domain": str,
            "credibility_score": float (0.0 to 1.0),
            "tier_label": str,
            "is_authoritative": bool,
            "badge_color": str
        }
    """
    domain = extract_domain(url)
    
    # 1. Exact or suffix match in Tier 1
    for k, (score, label) in TIER_1_DOMAINS.items():
        if domain == k or domain.endswith("." + k):
            return {
                "domain": domain,
                "credibility_score": score,
                "tier_label": label,
                "is_authoritative": True,
                "badge_color": "#10b981"  # Emerald green
            }
            
    # Check institutional TLDs (.edu, .gov, .ac.uk)
    if domain.endswith(".edu") or domain.endswith(".ac.uk"):
        return {
            "domain": domain,
            "credibility_score": 0.94,
            "tier_label": "Tier-1 Accredited Educational Domain",
            "is_authoritative": True,
            "badge_color": "#10b981"
        }
    if domain.endswith(".gov") or domain.endswith(".mil"):
        return {
            "domain": domain,
            "credibility_score": 0.95,
            "tier_label": "Tier-1 Official Government Source",
            "is_authoritative": True,
            "badge_color": "#10b981"
        }
        
    # 2. Check Tier 2
    for k, (score, label) in TIER_2_DOMAINS.items():
        if domain == k or domain.endswith("." + k):
            return {
                "domain": domain,
                "credibility_score": score,
                "tier_label": label,
                "is_authoritative": True,
                "badge_color": "#3b82f6"  # Blue
            }
            
    # 3. Check Tier 4 (Low reliability / user generated)
    for k, (score, label) in TIER_4_DOMAINS.items():
        if domain == k or domain.endswith("." + k):
            return {
                "domain": domain,
                "credibility_score": score,
                "tier_label": label,
                "is_authoritative": False,
                "badge_color": "#f59e0b"  # Amber
            }
            
    # 4. Default Tier 3: General Web Content
    base_score = 0.65
    if domain.endswith(".org"):
        base_score = 0.75
        tier_desc = "Tier-3 Non-Profit / Organization Domain"
    else:
        tier_desc = "Tier-3 General Web Publication"

    return {
        "domain": domain or "external-source",
        "credibility_score": base_score,
        "tier_label": tier_desc,
        "is_authoritative": False,
        "badge_color": "#64748b"  # Slate grey
    }


def enrich_evidence_pool_with_credibility(evidence_pool: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    Enriches all entries in evidence_pool with source credibility metadata.
    """
    enriched = {}
    for eid, ev in evidence_pool.items():
        url = ev.get("url", "")
        title = ev.get("title", "")
        snippet = ev.get("snippet", "")
        cred = score_source_credibility(url=url, title=title, snippet=snippet)
        
        item = dict(ev)
        item["credibility_score"] = cred["credibility_score"]
        item["tier_label"] = cred["tier_label"]
        item["domain"] = cred["domain"]
        item["is_authoritative"] = cred["is_authoritative"]
        item["badge_color"] = cred["badge_color"]
        enriched[eid] = item
        
    return enriched
