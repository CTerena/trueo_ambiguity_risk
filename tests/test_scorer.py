"""
Test module for the Market Prompt Ambiguity Risk Scoring System.

This module contains test cases to validate the functionality of the
risk scoring system.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import analyze_market_prompt
from models import RiskScoreResult


def test_basic_analysis():
    """
    Test basic analysis with a simple market question.
    
    This test verifies that:
    1. The function returns a valid RiskScoreResult
    2. The risk_score is within 0-100 range
    3. The risk_tags is a list
    4. The rationale is a non-empty string
    """
    print("\n" + "="*60)
    print("TEST: Basic Analysis")
    print("="*60)
    
    question = "Will OpenAI release a new model in March this year?"
    
    print(f"\nInput Question: {question}")
    print("\nCalling API... (this may take a few seconds)")
    
    result = analyze_market_prompt(question)
    
    # Validate result type
    assert isinstance(result, RiskScoreResult), "Result should be RiskScoreResult"
    print(f"\n✓ Result type: RiskScoreResult")
    
    # Validate risk_score range
    assert 0 <= result.risk_score <= 100, "Risk score must be 0-100"
    print(f"✓ Risk score: {result.risk_score}/100")
    
    # Validate risk_tags
    assert isinstance(result.risk_tags, list), "Risk tags must be a list"
    print(f"✓ Risk tags: {result.risk_tags}")
    
    # Validate rationale
    assert isinstance(result.rationale, str), "Rationale must be a string"
    assert len(result.rationale) > 0, "Rationale must not be empty"
    print(f"✓ Rationale: {result.rationale[:100]}...")
    
    print("\n" + "="*60)
    print("✅ TEST PASSED: Basic Analysis")
    print("="*60)
    
    return result


def test_output_format():
    """
    Test that the output format matches the expected JSON structure.
    """
    print("\n" + "="*60)
    print("TEST: Output Format Validation")
    print("="*60)
    
    question = "Will Bitcoin exceed $100,000 USD on December 31, 2025?"
    
    print(f"\nInput Question: {question}")
    print("\nCalling API...")
    
    result = analyze_market_prompt(question)
    
    # Convert to dict
    result_dict = result.model_dump()
    
    print(f"\nOutput JSON:")
    print(result.model_dump_json(indent=2))
    
    # Validate JSON structure
    assert "risk_score" in result_dict, "Missing 'risk_score' field"
    assert "risk_tags" in result_dict, "Missing 'risk_tags' field"
    assert "rationale" in result_dict, "Missing 'rationale' field"
    
    print("\n✓ Output contains all required fields:")
    print("  - risk_score: integer")
    print("  - risk_tags: list")
    print("  - rationale: string")
    
    print("\n" + "="*60)
    print("✅ TEST PASSED: Output Format Validation")
    print("="*60)
    
    return result


def test_high_risk_question():
    """
    Test with a question that should have high risk score.
    """
    print("\n" + "="*60)
    print("TEST: High Risk Question Detection")
    print("="*60)
    
    # This question is intentionally vague
    question = "Will something important happen soon?"
    
    print(f"\nInput Question: {question}")
    print("\nCalling API...")
    
    result = analyze_market_prompt(question, use_few_shot=False)
    
    print(f"\nRisk Score: {result.risk_score}/100")
    print(f"Risk Tags: {result.risk_tags}")
    print(f"Rationale: {result.rationale}")
    
    # We expect this question to have a high risk score
    print(f"\n✓ High ambiguity detected: {result.risk_score >= 50}")
    
    print("\n" + "="*60)
    print("✅ TEST PASSED: High Risk Question Detection")
    print("="*60)
    
    return result


def run_all_tests():
    """
    Run all tests and report results.
    """
    print("\n" + "="*60)
    print("RUNNING ALL TESTS")
    print("="*60)
    
    tests = [
        ("Basic Analysis", test_basic_analysis),
        ("Output Format", test_output_format),
        ("High Risk Detection", test_high_risk_question),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"\n❌ TEST FAILED: {name}")
            print(f"Error: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run risk scorer tests")
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Run only the basic test"
    )
    
    args = parser.parse_args()
    
    if args.quick:
        result = test_basic_analysis()
        print("\n" + "="*60)
        print("FINAL OUTPUT")
        print("="*60)
        print(result.model_dump_json(indent=2))
    else:
        success = run_all_tests()
        sys.exit(0 if success else 1)
