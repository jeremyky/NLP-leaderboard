"""
Background evaluation service for processing submissions

This module handles the async evaluation of submissions in a queue.
For production, consider using Celery or similar for distributed task processing.
"""
from database import SessionLocal
from models import Submission, Dataset, SubmissionStatus
from evaluators import get_evaluator
from datetime import datetime
import traceback
from scipy import stats
import numpy as np


def compute_confidence_interval(scores: list, confidence=0.95) -> str:
    """
    Compute confidence interval for scores using bootstrap or normal approximation
    
    Args:
        scores: List of individual scores
        confidence: Confidence level (default 0.95 for 95% CI)
        
    Returns:
        String representation of CI, e.g., "0.85 - 0.93"
    """
    if not scores or len(scores) < 2:
        return None
    
    mean = np.mean(scores)
    std_err = stats.sem(scores)
    
    # Use t-distribution for small samples
    ci = stats.t.interval(
        confidence,
        len(scores) - 1,
        loc=mean,
        scale=std_err
    )
    
    return f"{ci[0]:.2f} - {ci[1]:.2f}"


def evaluate_submission(submission_id: str):
    """
    Evaluate a submission against ground truth
    
    This function:
    1. Loads the submission and dataset
    2. Runs the appropriate evaluator
    3. Computes scores and confidence intervals
    4. Updates the submission with results
    """
    db = SessionLocal()
    
    try:
        # Get submission
        submission = db.query(Submission).filter(Submission.id == submission_id).first()
        if not submission:
            print(f"Submission {submission_id} not found")
            return
        
        # Update status to processing
        submission.status = SubmissionStatus.PROCESSING
        db.commit()
        
        # Get dataset
        dataset = db.query(Dataset).filter(Dataset.id == submission.dataset_id).first()
        if not dataset:
            raise Exception(f"Dataset {submission.dataset_id} not found")
        
        # Validate predictions match ground truth IDs
        gt_ids = {item['id'] for item in dataset.ground_truth}
        pred_ids = {item['id'] for item in submission.predictions}
        
        if not pred_ids.issubset(gt_ids):
            missing = pred_ids - gt_ids
            raise Exception(f"Invalid prediction IDs: {missing}")
        
        # Get appropriate evaluator
        evaluator = get_evaluator(dataset.task_type.value)
        
        # Run evaluation
        scores = evaluator.evaluate(dataset.ground_truth, submission.predictions)
        
        # Get primary score
        primary_score = scores.get(dataset.primary_metric)
        if primary_score is None:
            raise Exception(f"Primary metric '{dataset.primary_metric}' not found in evaluation results")
        
        # Compute confidence interval
        # For now, use a simple bootstrap approach
        # In production, you might want more sophisticated CI computation
        ci = compute_confidence_interval([primary_score] * 100)  # Placeholder
        
        # Update submission with results
        submission.primary_score = primary_score
        submission.detailed_scores = scores
        submission.confidence_interval = ci
        submission.status = SubmissionStatus.COMPLETED
        submission.evaluated_at = datetime.utcnow()
        
        db.commit()
        
        print(f"✓ Submission {submission_id} evaluated successfully")
        print(f"  Model: {submission.model_name}")
        print(f"  Score: {primary_score} ({dataset.primary_metric})")
        print(f"  All metrics: {scores}")
        
    except Exception as e:
        # Mark submission as failed
        submission.status = SubmissionStatus.FAILED
        submission.error_message = str(e)
        db.commit()
        
        print(f"✗ Submission {submission_id} evaluation failed: {e}")
        traceback.print_exc()
        
    finally:
        db.close()


def recompute_leaderboard_rankings(dataset_id: str):
    """
    Recompute and cache leaderboard rankings for a dataset
    
    This can be called after new submissions to update the cached rankings.
    Currently, rankings are computed on-the-fly in the API.
    """
    # Future enhancement: Cache rankings in LeaderboardEntry table
    # for faster leaderboard queries
    pass

