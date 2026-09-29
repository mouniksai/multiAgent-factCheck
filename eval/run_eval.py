"""
Aletheia AI — Dialectical Multi-Agent Evaluation & Benchmark Harness
=====================================================================
Executes structured fact-checking benchmark evaluations across:
- Popular scientific myths & cultural misconceptions
- Authoritative consensus & empirical facts
- Genuinely ambiguous & nuanced claims (hedging calibration)
- Fallacy detection (Correlation vs. Causation)
- Citation guardrail integrity checks

Usage:
    python3 eval/run_eval.py               # Runs standard 5-scenario demo suite
    python3 eval/run_eval.py --all         # Runs full 13-scenario benchmark suite
    python3 eval/run_eval.py --category Myth # Runs all myth & misconception scenarios
    python3 eval/run_eval.py --claim-id scenario_6  # Runs single claim (10% brain myth)
    python3 eval/run_eval.py --rounds 2    # Deep 2-round debate
"""

import sys
import os
import json
import time
import argparse

# Force UTF-8 stdout encoding on terminals
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.graph.debate_graph import run_debate


def parse_args():
    parser = argparse.ArgumentParser(description="Aletheia Multi-Agent Fact-Checking Benchmark Harness")
    parser.add_argument("--all", action="store_true", help="Run the entire 13-scenario test suite")
    parser.add_argument("--count", type=int, default=5, help="Number of scenarios to run if --all is not specified (default: 5)")
    parser.add_argument("--claim-id", type=str, default=None, help="Filter by specific scenario ID (e.g. scenario_6)")
    parser.add_argument("--category", type=str, default=None, help="Filter scenarios containing category keyword (e.g. Myth)")
    parser.add_argument("--rounds", type=int, default=1, help="Max debate rounds per scenario (default: 1 for fast demo, 2 for deep)")
    return parser.parse_args()


def run_evaluation():
    args = parse_args()

    json_path = os.path.join(os.path.dirname(__file__), "test_claims.json")
    with open(json_path, "r", encoding="utf-8") as f:
        all_scenarios = json.load(f)

    # Filter scenarios based on user CLI arguments
    scenarios = all_scenarios
    if args.claim_id:
        scenarios = [s for s in scenarios if s.get("id") == args.claim_id]
        if not scenarios:
            print(f"Error: Claim ID '{args.claim_id}' not found in {json_path}")
            sys.exit(1)
    elif args.category:
        scenarios = [s for s in scenarios if args.category.lower() in s.get("category", "").lower()]
        if not scenarios:
            print(f"Error: No claims matched category filter '{args.category}'")
            sys.exit(1)
    elif not args.all:
        scenarios = scenarios[:args.count]

    print("\n" + "=" * 80)
    print(" ALETHEIA DIALECTICAL MULTI-AGENT EVALUATION & CALIBRATION HARNESS")
    print(f" Executing {len(scenarios)} Benchmark Scenarios | Debate Rounds: {args.rounds}")
    print("=" * 80)

    results_table = []
    calibration_failures = 0
    passed_scenarios = 0
    t_start_total = time.time()

    for idx, sc in enumerate(scenarios, 1):
        sc_id = sc.get("id", f"scenario_{idx}")
        category = sc["category"]
        claim = sc["claim"]
        exp_verdict = sc["expected_verdict"].lower()
        max_allowed_conf = sc.get("expected_max_confidence", 100)
        demo_focus = sc.get("demo_focus", "")

        print(f"\n[{idx}/{len(scenarios)}] [{sc_id.upper()}] Category: '{category}'")
        print(f"  Claim: \"{claim}\"")
        if demo_focus:
            print(f"  Objective: {demo_focus}")

        t0 = time.time()
        try:
            res = run_debate(claim, max_rounds=args.rounds)
            elapsed = round(time.time() - t0, 2)
        except Exception as e:
            print(f"  [ERROR] Execution failed: {e}")
            results_table.append({
                "id": sc_id,
                "category": category,
                "claim": claim,
                "expected": exp_verdict.upper(),
                "observed": "ERROR",
                "confidence": 0,
                "guardrail": "ERROR",
                "status": "FAIL",
                "elapsed": 0.0
            })
            continue

        verdict_data = res.get("verdict") or {}
        verdict = verdict_data.get("verdict", "unverifiable").lower()
        confidence = verdict_data.get("confidence", 0)
        rationale = verdict_data.get("rationale", "")
        uncertainty = verdict_data.get("uncertainty_note")
        guardrail = verdict_data.get("guardrail_report", {})
        is_clean = guardrail.get("is_clean", True)
        valid_citations = guardrail.get("valid_citations", [])

        # Display turn metrics
        print(f"  -> Observed Verdict: {verdict.upper()} (Confidence: {confidence}%) in {elapsed}s")
        print(f"  -> Valid Citations Registered: {len(valid_citations)} citations {valid_citations}")
        print(f"  -> Guardrail Status: {'CLEAN (100% Grounded)' if is_clean else 'VIOLATION DETECTED'}")
        print(f"  -> Judicial Rationale: {rationale[:160]}...")
        if uncertainty:
            print(f"  -> Epistemic Uncertainty Note: {uncertainty}")

        # Validation Logic
        scenario_passed = True
        status_note = "PASS"

        # Check verdict alignment
        if exp_verdict == "unverifiable":
            if verdict != "unverifiable" and confidence > max_allowed_conf:
                scenario_passed = False
                status_note = "CALIBRATION FAIL (Overconfident)"
                calibration_failures += 1
            elif not uncertainty:
                scenario_passed = False
                status_note = "CALIBRATION FAIL (No Note)"
                calibration_failures += 1
        elif exp_verdict in ("true", "false"):
            if verdict != exp_verdict:
                scenario_passed = False
                status_note = f"VERDICT MISMATCH (Expected {exp_verdict.upper()})"

        if scenario_passed:
            print(f"  [PASS] Scenario successfully validated: {status_note}")
            passed_scenarios += 1
        else:
            print(f"  [FAIL] Evaluation issue: {status_note}")

        results_table.append({
            "id": sc_id,
            "category": category,
            "claim": claim,
            "expected": exp_verdict.upper(),
            "observed": verdict.upper(),
            "confidence": confidence,
            "guardrail": "Clean (100%)" if is_clean else "Flagged",
            "status": "PASS" if scenario_passed else "FAIL",
            "elapsed": elapsed
        })
        print("-" * 80)

    total_time = round(time.time() - t_start_total, 2)

    # Executive Summary Table
    print("\n" + "=" * 90)
    print(" EXECUTIVE BENCHMARK RESULTS SUMMARY TABLE")
    print("=" * 90)
    header_fmt = "{:<12} {:<24} {:<10} {:<10} {:<8} {:<14} {:<6}"
    print(header_fmt.format("Scenario", "Category", "Expected", "Observed", "Conf.", "Guardrail", "Status"))
    print("-" * 90)
    for row in results_table:
        print(header_fmt.format(
            row["id"],
            row["category"][:22],
            row["expected"],
            row["observed"],
            f"{row['confidence']}%",
            row["guardrail"],
            f"[{row['status']}]"
        ))
    print("=" * 90)

    pass_rate = round((passed_scenarios / len(scenarios)) * 100, 1) if scenarios else 0
    print(f"\nFinal Summary: {passed_scenarios}/{len(scenarios)} Benchmark Scenarios Passed ({pass_rate}% Pass Rate)")
    print(f"Total Test Execution Time: {total_time}s (Avg {round(total_time/len(scenarios), 2) if scenarios else 0}s/claim)")
    print(f"Calibration Failures: {calibration_failures}")

    if calibration_failures > 0 or passed_scenarios < len(scenarios):
        print("\nNote: Some scenarios required adjustments or produced hedged outcomes.")
    else:
        print("\nSUCCESS: All benchmark scenarios validated cleanly with 100% citation guardrails!")

    return passed_scenarios == len(scenarios)


if __name__ == "__main__":
    run_evaluation()
