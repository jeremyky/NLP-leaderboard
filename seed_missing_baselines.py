"""
Create internal baseline submissions for any datasets that currently have none.

This is especially useful for newly imported HuggingFace benchmarks that were
added via `hf_seed_from_proposals.py`, which by default only create Dataset
rows without model submissions.

The script:
  - Scans all datasets in the database.
  - For each dataset with ZERO completed submissions, it:
      * Chooses a small set of generic baseline models based on task_type.
      * Uses `create_baseline_predictions` from `seed_data` to generate
        predictions that roughly match a target score.
      * Evaluates those predictions with the appropriate evaluator.
      * Writes internal `Submission` records so the frontend leaderboards show
        non-empty model tables.

Usage (from project root):

    python seed_missing_baselines.py
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Dict, List

from database import SessionLocal, init_db
from evaluators import get_evaluator
from models import Dataset, Submission, SubmissionStatus, TaskType
from seed_data import create_baseline_predictions


# Simple generic baselines per task type. Scores are approximate targets; the
# evaluator recomputes actual metrics from the generated predictions.
GENERIC_BASELINES: Dict[str, List[Dict[str, str]]] = {
    "text_classification": [
        {"model": "GPT-4o (synthetic baseline)", "score": 0.88, "organization": "Internal"},
        {"model": "Claude 3.5 Sonnet (synthetic baseline)", "score": 0.86, "organization": "Internal"},
        {"model": "Llama 3.1 70B (synthetic baseline)", "score": 0.83, "organization": "Internal"},
    ],
    "document_qa": [
        {"model": "GPT-4o (synthetic baseline)", "score": 0.78, "organization": "Internal"},
        {"model": "Claude 3.5 Sonnet (synthetic baseline)", "score": 0.75, "organization": "Internal"},
    ],
    "line_qa": [
        {"model": "GPT-4o (synthetic baseline)", "score": 0.80, "organization": "Internal"},
        {"model": "Claude 3.5 Sonnet (synthetic baseline)", "score": 0.77, "organization": "Internal"},
    ],
    "named_entity_recognition": [
        {"model": "Generic NER baseline", "score": 0.70, "organization": "Internal"},
    ],
    "retrieval": [
        {"model": "Generic retriever baseline", "score": 0.65, "organization": "Internal"},
    ],
}


def seed_missing_baselines() -> None:
    init_db()
    db = SessionLocal()

    try:
        print("\n" + "=" * 60)
        print("📊 SEEDING MISSING BASELINE SUBMISSIONS")
        print("=" * 60 + "\n")

        datasets = db.query(Dataset).all()
        total_added = 0

        for dataset in datasets:
            # Count existing completed submissions
            existing_submissions = (
                db.query(Submission)
                .filter(
                    Submission.dataset_id == dataset.id,
                    Submission.status == SubmissionStatus.COMPLETED,
                )
                .count()
            )

            if existing_submissions > 0:
                # Already has baselines or user submissions
                continue

            task_type_str = dataset.task_type.value if isinstance(dataset.task_type, TaskType) else str(dataset.task_type)
            baselines_for_task = GENERIC_BASELINES.get(task_type_str)

            if not baselines_for_task:
                print(f"⏭️  Skipping dataset '{dataset.name}' (task_type={task_type_str}) – no generic baselines configured.")
                continue

            if not dataset.ground_truth:
                print(f"⏭️  Skipping dataset '{dataset.name}' – no ground truth available.")
                continue

            print(f"📚 Dataset '{dataset.name}' has no submissions; creating generic baselines...")

            evaluator = get_evaluator(task_type_str)

            for baseline in baselines_for_task:
                submission_id = str(uuid.uuid4())

                predictions = create_baseline_predictions(
                    dataset.ground_truth,
                    baseline["score"],
                )

                scores = evaluator.evaluate(dataset.ground_truth, predictions)
                primary_score = scores.get(dataset.primary_metric, baseline["score"])

                submission = Submission(
                    id=submission_id,
                    dataset_id=dataset.id,
                    model_name=baseline["model"],
                    model_version=None,
                    organization=baseline.get("organization"),
                    predictions=predictions,
                    status=SubmissionStatus.COMPLETED,
                    primary_score=primary_score,
                    detailed_scores=scores,
                    confidence_interval=f"{primary_score-0.02:.2f} - {primary_score+0.02:.2f}",
                    is_internal=True,
                    created_at=datetime.utcnow(),
                    evaluated_at=datetime.utcnow(),
                )
                db.add(submission)
                total_added += 1

                print(
                    f"   ✓ {baseline['model']} for '{dataset.name}': "
                    f"{primary_score:.4f} {dataset.primary_metric}"
                )

            db.commit()
            print(f"   ✅ Finished '{dataset.name}'\n")

        print("=" * 60)
        print(f"✅ Completed seeding missing baselines. Added {total_added} submissions.")
        print("=" * 60 + "\n")

    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_missing_baselines()


