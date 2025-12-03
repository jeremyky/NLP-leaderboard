import os
import sys

import pytest

# Ensure project root is on sys.path
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from database import init_db, SessionLocal
from models import Dataset, Submission
from science_datasets import seed_science_datasets
from seed_data import clear_database


@pytest.fixture(autouse=True)
def clean_db():
    init_db()
    clear_database()
    try:
        yield
    finally:
        clear_database()


def test_seed_science_datasets_creates_datasets_and_submissions():
    seed_science_datasets()

    db = SessionLocal()
    try:
        datasets = (
            db.query(Dataset)
            .filter(Dataset.name.like("Science QA%") | Dataset.name.like("Code Reasoning%"))
            .all()
        )
        assert len(datasets) >= 2

        for ds in datasets:
            subs = db.query(Submission).filter(Submission.dataset_id == ds.id).all()
            assert subs, f"Expected baseline submissions for {ds.name}"
            for sub in subs:
                assert sub.primary_score is not None
                assert isinstance(sub.detailed_scores, dict)
    finally:
        db.close()


