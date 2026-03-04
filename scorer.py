"""
Risk Scorer module for the Market Prompt Ambiguity Risk Scoring System.

This module contains the RiskScorer class that orchestrates the risk
assessment process using the SemanticAnalysisAgent.
"""

from typing import Optional, List
from agent import SemanticAnalysisAgent
from models import RiskScoreResult, MarketProposal
from config import DEFAULT_RISK_THRESHOLD


class RiskScorer:
    """
    Risk scorer for market prompts.
    
    This class orchestrates the risk assessment process by using
    a SemanticAnalysisAgent to analyze market questions and generate
    risk scores.
    
    Attributes:
        agent: SemanticAnalysisAgent instance for LLM-based analysis
        risk_threshold: Threshold above which prompts are considered high risk
    """
    
    def __init__(
        self,
        agent: Optional[SemanticAnalysisAgent] = None,
        risk_threshold: int = DEFAULT_RISK_THRESHOLD
    ):
        """
        Initialize the RiskScorer.
        
        Args:
            agent: SemanticAnalysisAgent instance (created if not provided)
            risk_threshold: Risk score threshold for high-risk classification
        """
        self.agent = agent or SemanticAnalysisAgent()
        self.risk_threshold = risk_threshold
    
    def score(
        self,
        question: str,
        context: Optional[str] = None,
        include_few_shot: bool = True
    ) -> RiskScoreResult:
        """
        Calculate risk score for a market question.
        
        Args:
            question: The market question to score
            context: Optional additional context (e.g., from web search)
            include_few_shot: Whether to use few-shot prompting
            
        Returns:
            RiskScoreResult containing the assessment
        """
        return self.agent.analyze(
            question=question,
            context=context,
            include_few_shot=include_few_shot
        )
    
    def score_proposal(
        self,
        proposal: MarketProposal,
        include_few_shot: bool = True
    ) -> RiskScoreResult:
        """
        Calculate risk score for a MarketProposal object.
        
        Args:
            proposal: MarketProposal to analyze
            include_few_shot: Whether to use few-shot prompting
            
        Returns:
            RiskScoreResult containing the assessment
        """
        return self.score(
            question=proposal.question,
            context=proposal.context,
            include_few_shot=include_few_shot
        )
    
    def is_high_risk(self, result: RiskScoreResult) -> bool:
        """
        Determine if a result indicates high risk.
        
        Args:
            result: RiskScoreResult to evaluate
            
        Returns:
            True if risk score exceeds threshold
        """
        return result.risk_score >= self.risk_threshold
    
    def batch_score(
        self,
        questions: List[str],
        **kwargs
    ) -> List[RiskScoreResult]:
        """
        Score multiple questions in batch.
        
        Args:
            questions: List of questions to score
            **kwargs: Additional arguments passed to score()
            
        Returns:
            List of RiskScoreResult objects
        """
        return [self.score(q, **kwargs) for q in questions]
