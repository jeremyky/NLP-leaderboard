import os
import sys
import pytest

# Ensure the project root is on sys.path so we can import app modules
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from database import SessionLocal, init_db
from models import Dataset, Submission
from evaluators import get_evaluator
from seed_data import seed_database, clear_database
from finance_datasets import seed_finance_datasets
from multilingual_datasets import seed_multilingual_datasets


@pytest.fixture(scope="module")
def seeded_db():
    """
    Seed the database with all internal datasets and baseline models.

    This uses the same seed helpers that the application relies on so we can
    verify that all stored scores are consistent with the evaluators.
    """
    init_db()
    # Start from a clean slate to make the assertions deterministic
    clear_database()
    seed_database()
    seed_finance_datasets()
    seed_multilingual_datasets()
    try:
        yield
    finally:
        # Leave the database in a clean state after the module tests run
        clear_database()


def test_internal_baseline_submissions_match_evaluators(seeded_db):
    """
    For every internally-seeded submission:
    - Re-run the appropriate evaluator against ground truth and predictions
    - Assert the stored detailed_scores and primary_score are consistent
    """
    db = SessionLocal()
    try:
        datasets = db.query(Dataset).all()
        assert datasets, "Expected at least one dataset after seeding"

        for dataset in datasets:
            evaluator = get_evaluator(dataset.task_type.value)
            submissions = (
                db.query(Submission)
                .filter(Submission.dataset_id == dataset.id)
                .all()
            )

            # There should be at least one internal submission per seeded dataset
            assert submissions, f"No submissions found for dataset {dataset.name}"

            for submission in submissions:
                scores = evaluator.evaluate(dataset.ground_truth, submission.predictions)

                # Primary metric must exist and match the stored primary_score
                assert dataset.primary_metric in scores, (
                    f"Primary metric '{dataset.primary_metric}' "
                    f"missing from scores for dataset {dataset.name}"
                )

                assert submission.primary_score == pytest.approx(
                    scores[dataset.primary_metric]
                )

                # All computed metrics should be reflected in detailed_scores
                assert isinstance(submission.detailed_scores, dict)
                for metric_name, metric_value in scores.items():
                    assert metric_name in submission.detailed_scores, (
                        f"Metric '{metric_name}' missing from detailed_scores "
                        f"for submission {submission.id}"
                    )
                    assert submission.detailed_scores[metric_name] == pytest.approx(
                        metric_value
                    )
    finally:
        db.close()


