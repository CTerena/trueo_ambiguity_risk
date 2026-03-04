"""
Main entry point for the Market Prompt Ambiguity Risk Scoring System.

This module provides the primary interface for analyzing market prompts
and detecting ambiguity risks.
"""

from typing import Optional

from agent import SemanticAnalysisAgent
from scorer import RiskScorer
from models import RiskScoreResult, MarketProposal


def analyze_market_prompt(
    question: str,
    context: Optional[str] = None,
    use_few_shot: bool = True,
    use_web_search: bool = False
) -> RiskScoreResult:
    """
    Analyze a market prompt for ambiguity risks.
    
    This is the main entry point for the risk scoring system. It takes a
    market question and returns a comprehensive risk assessment.
    
    Args:
        question: The market question to analyze
        context: Optional additional context (for future web search integration)
        use_few_shot: Whether to use few-shot examples for better prompting
        use_web_search: Whether to perform web search (not yet implemented)
        
    Returns:
        RiskScoreResult containing:
            - risk_score: Integer 0-100 (higher = more ambiguous)
            - risk_tags: List of identified risk categories
            - rationale: Detailed explanation of the assessment
            
    Example:
        >>> result = analyze_market_prompt(
        ...     "Will OpenAI release a new model in March this year?"
        ... )
        >>> print(result.risk_score)
        65
        >>> print(result.risk_tags)
        ['ambiguous_time', 'undefined_term']
    """
    # TODO: Implement web search when context is None and use_web_search is True
    if use_web_search and context is None:
        # Placeholder for future web search integration
        pass
    
    # Create scorer and analyze
    scorer = RiskScorer()
    return scorer.score(
        question=question,
        context=context,
        include_few_shot=use_few_shot
    )


def analyze_proposal(proposal: MarketProposal) -> RiskScoreResult:
    """
    Analyze a MarketProposal object for ambiguity risks.
    
    Args:
        proposal: MarketProposal containing the question and optional context
        
    Returns:
        RiskScoreResult containing the risk assessment
    """
    scorer = RiskScorer()
    return scorer.score_proposal(proposal)


# CLI interface for testing
if __name__ == "__main__":
    import argparse
    import json
    
    parser = argparse.ArgumentParser(
        description="Analyze market prompts for ambiguity risks"
    )
    parser.add_argument(
        "question",
        type=str,
        help="The market question to analyze"
    )
    parser.add_argument(
        "--context",
        type=str,
        default=None,
        help="Optional context for the analysis"
    )
    parser.add_argument(
        "--no-few-shot",
        action="store_true",
        help="Disable few-shot examples in prompting"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )
    
    args = parser.parse_args()
    
    result = analyze_market_prompt(
        question=args.question,
        context=args.context,
        use_few_shot=not args.no_few_shot
    )
    
    if args.json:
        print(result.model_dump_json(indent=2))
    else:
        print(f"\n{'='*60}")
        print("MARKET PROMPT RISK ANALYSIS")
        print(f"{'='*60}")
        print(f"\nQuestion: {args.question}")
        print(f"\nRisk Score: {result.risk_score}/100")
        print(f"\nRisk Tags: {', '.join(result.risk_tags) if result.risk_tags else 'None'}")
        print(f"\nRationale:\n{result.rationale}")
        print(f"\n{'='*60}\n")
