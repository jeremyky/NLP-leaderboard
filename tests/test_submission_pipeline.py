import os
import sys
import time
from typing import Dict, Any

import pytest
from fastapi.testclient import TestClient as FastAPITestClient

# Ensure project root is on sys.path
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from main import app
from database import init_db, SessionLocal
from seed_data import clear_database
from models import Dataset, Submission, SubmissionStatus
from evaluators import get_evaluator


@pytest.fixture(autouse=True)
def clean_db():
    """
    Ensure each test runs against a clean database.
    """
    init_db()
    clear_database()
    try:
        yield
    finally:
        clear_database()


@pytest.fixture
def client() -> FastAPITestClient:
    # Use context manager style client to avoid compatibility issues
    return FastAPITestClient(app)


def _create_simple_dataset_payload() -> Dict[str, Any]:
    return {
        "name": "Test Text Classification Dataset",
        "description": "Synthetic dataset for submission pipeline tests",
        "url": "https://huggingface.co/datasets/test-dataset",
        "task_type": "text_classification",
        "test_set_public": False,
        "labels_public": False,
        "primary_metric": "accuracy",
        "additional_metrics": ["f1", "precision", "recall"],
        "ground_truth": [
            {"id": "1", "question": "sample text A", "answer": "positive"},
            {"id": "2", "question": "sample text B", "answer": "negative"},
            {"id": "3", "question": "sample text C", "answer": "positive"},
        ],
    }


def _create_document_qa_dataset_payload() -> Dict[str, Any]:
    return {
        "name": "Test Document QA Dataset",
        "description": "Synthetic document QA dataset for submission pipeline tests",
        "url": "https://huggingface.co/datasets/test-doc-qa",
        "task_type": "document_qa",
        "test_set_public": False,
        "labels_public": False,
        "primary_metric": "exact_match",
        "additional_metrics": ["f1"],
        "ground_truth": [
            {
                "id": "1",
                "question": "What is the capital of France?",
                "context": "France is a country in Europe. Paris is its capital city.",
                "answer": "Paris",
            },
            {
                "id": "2",
                "question": "What is H2O commonly called?",
                "context": "H2O is the chemical formula for water.",
                "answer": ["water", "H2O"],
            },
        ],
    }


def _create_ner_dataset_payload() -> Dict[str, Any]:
    return {
        "name": "Test NER Dataset",
        "description": "Synthetic NER dataset for submission pipeline tests",
        "url": "https://huggingface.co/datasets/test-ner",
        "task_type": "named_entity_recognition",
        "test_set_public": False,
        "labels_public": False,
        "primary_metric": "f1",
        "additional_metrics": ["precision", "recall", "partial_f1"],
        "ground_truth": [
            {
                "id": "1",
                "text": "Apple Inc. reported revenue of $125.3B",
                "answer": [["Apple Inc.", "ORG"], ["$125.3B", "MONEY"]],
            },
            {
                "id": "2",
                "text": "Microsoft acquired GitHub for $7.5B",
                "answer": [
                    ["Microsoft", "ORG"],
                    ["GitHub", "ORG"],
                    ["$7.5B", "MONEY"],
                ],
            },
        ],
    }


def _create_retrieval_dataset_payload() -> Dict[str, Any]:
    return {
        "name": "Test Retrieval Dataset",
        "description": "Synthetic retrieval dataset for submission pipeline tests",
        "url": "https://huggingface.co/datasets/test-retrieval",
        "task_type": "retrieval",
        "test_set_public": False,
        "labels_public": False,
        "primary_metric": "retrieval_accuracy",
        "additional_metrics": ["mrr", "precision_at_1"],
        "ground_truth": [
            {"id": "1", "question": "q1", "answer": ["d1"]},
            {"id": "2", "question": "q2", "answer": ["d2"]},
            {"id": "3", "question": "q3", "answer": ["d3"]},
        ],
    }


def test_submission_pipeline_end_to_end(client: FastAPITestClient):
    """
    End-to-end test of the submission pipeline:
    - Create dataset via API
    - Submit predictions via API
    - Manually run evaluation_service.evaluate_submission
    - Verify submission status and scores via API
    """
    # 1) Create dataset
    dataset_payload = _create_simple_dataset_payload()
    create_resp = client.post("/api/datasets", json=dataset_payload)
    assert create_resp.status_code == 201, create_resp.text
    dataset_data = create_resp.json()["data"]
    dataset_id = dataset_data["dataset_id"]

    # 2) Create a submission with partially-correct predictions
    submission_payload = {
        "dataset_id": dataset_id,
        "model_name": "TestModel-v1",
        "model_version": "1.0",
        "organization": "TestOrg",
        "predictions": [
            {"id": "1", "prediction": "positive"},
            {"id": "2", "prediction": "positive"},  # incorrect
            {"id": "3", "prediction": "positive"},
        ],
        "is_internal": False,
        "submission_metadata": {"source": "pytest"},
    }

    submit_resp = client.post("/api/submissions", json=submission_payload)
    assert submit_resp.status_code == 202, submit_resp.text
    payload = submit_resp.json()["data"]
    submission_id = payload["submission_id"]

    # 3) Manually trigger evaluation for deterministic testing
    from evaluation_service import evaluate_submission

    evaluate_submission(submission_id)

    # 4) Fetch submission status via API and verify evaluation results
    status_resp = client.get(f"/api/submissions/{submission_id}")
    assert status_resp.status_code == 200, status_resp.text
    submission = status_resp.json()

    assert submission["status"] == SubmissionStatus.COMPLETED.value
    assert submission["primary_score"] is not None
    assert submission["detailed_scores"] is not None
    assert submission["error_message"] is None

    # Verify scores are consistent with evaluator
    db = SessionLocal()
    try:
        ds = db.query(Dataset).filter(Dataset.id == dataset_id).first()
        sub = db.query(Submission).filter(Submission.id == submission_id).first()

        evaluator = get_evaluator(ds.task_type.value)
        scores = evaluator.evaluate(ds.ground_truth, sub.predictions)

        assert ds.primary_metric in scores
        assert pytest.approx(scores[ds.primary_metric]) == sub.primary_score

        for metric_name, metric_value in scores.items():
            assert metric_name in sub.detailed_scores
            assert pytest.approx(metric_value) == sub.detailed_scores[metric_name]
    finally:
        db.close()



def test_document_qa_submission_pipeline(client: FastAPITestClient):
    """
    End-to-end submission pipeline test for a document QA dataset.
    """
    dataset_payload = _create_document_qa_dataset_payload()
    create_resp = client.post("/api/datasets", json=dataset_payload)
    assert create_resp.status_code == 201, create_resp.text
    dataset_id = create_resp.json()["data"]["dataset_id"]

    # Predictions: first correct, second partially correct (one of the accepted answers)
    submission_payload = {
        "dataset_id": dataset_id,
        "model_name": "TestDocQAModel",
        "model_version": "1.0",
        "organization": "TestOrg",
        "predictions": [
            {"id": "1", "prediction": "Paris"},
            {"id": "2", "prediction": "water"},
        ],
        "is_internal": False,
        "submission_metadata": {"source": "pytest-doc-qa"},
    }

    submit_resp = client.post("/api/submissions", json=submission_payload)
    assert submit_resp.status_code == 202, submit_resp.text
    submission_id = submit_resp.json()["data"]["submission_id"]

    from evaluation_service import evaluate_submission

    evaluate_submission(submission_id)

    status_resp = client.get(f"/api/submissions/{submission_id}")
    assert status_resp.status_code == 200, status_resp.text
    submission = status_resp.json()

    assert submission["status"] == SubmissionStatus.COMPLETED.value
    assert submission["primary_score"] is not None
    assert submission["detailed_scores"] is not None

    db = SessionLocal()
    try:
        ds = db.query(Dataset).filter(Dataset.id == dataset_id).first()
        sub = db.query(Submission).filter(Submission.id == submission_id).first()

        evaluator = get_evaluator(ds.task_type.value)
        scores = evaluator.evaluate(ds.ground_truth, sub.predictions)

        assert ds.primary_metric in scores
        assert pytest.approx(scores[ds.primary_metric]) == sub.primary_score
        for metric_name, metric_value in scores.items():
            assert metric_name in sub.detailed_scores
            assert pytest.approx(metric_value) == sub.detailed_scores[metric_name]
    finally:
        db.close()


def test_ner_submission_pipeline(client: FastAPITestClient):
    """
    End-to-end submission pipeline test for a NER dataset.
    """
    dataset_payload = _create_ner_dataset_payload()
    create_resp = client.post("/api/datasets", json=dataset_payload)
    assert create_resp.status_code == 201, create_resp.text
    dataset_id = create_resp.json()["data"]["dataset_id"]

    # Predictions: some exact, some partial boundary matches
    submission_payload = {
        "dataset_id": dataset_id,
        "model_name": "TestNERModel",
        "model_version": "1.0",
        "organization": "TestOrg",
        "predictions": [
            {
                "id": "1",
                "prediction": [["Apple Inc.", "ORG"], ["$125.3B", "MONEY"]],
            },
            {
                "id": "2",
                "prediction": [["Microsoft", "ORG"], ["GitHub", "ORG"]],
            },
        ],
        "is_internal": False,
        "submission_metadata": {"source": "pytest-ner"},
    }

    submit_resp = client.post("/api/submissions", json=submission_payload)
    assert submit_resp.status_code == 202, submit_resp.text
    submission_id = submit_resp.json()["data"]["submission_id"]

    from evaluation_service import evaluate_submission

    evaluate_submission(submission_id)

    status_resp = client.get(f"/api/submissions/{submission_id}")
    assert status_resp.status_code == 200, status_resp.text
    submission = status_resp.json()

    assert submission["status"] == SubmissionStatus.COMPLETED.value
    assert submission["primary_score"] is not None
    assert submission["detailed_scores"] is not None

    db = SessionLocal()
    try:
        ds = db.query(Dataset).filter(Dataset.id == dataset_id).first()
        sub = db.query(Submission).filter(Submission.id == submission_id).first()

        evaluator = get_evaluator(ds.task_type.value)
        scores = evaluator.evaluate(ds.ground_truth, sub.predictions)

        assert ds.primary_metric in scores
        assert pytest.approx(scores[ds.primary_metric]) == sub.primary_score
        for metric_name, metric_value in scores.items():
            assert metric_name in sub.detailed_scores
            assert pytest.approx(metric_value) == sub.detailed_scores[metric_name]
    finally:
        db.close()


def test_retrieval_submission_pipeline(client: FastAPITestClient):
    """
    End-to-end submission pipeline test for a retrieval dataset.
    """
    dataset_payload = _create_retrieval_dataset_payload()
    create_resp = client.post("/api/datasets", json=dataset_payload)
    assert create_resp.status_code == 201, create_resp.text
    dataset_id = create_resp.json()["data"]["dataset_id"]

    # Predictions: all queries retrieve the correct doc in top-2
    submission_payload = {
        "dataset_id": dataset_id,
        "model_name": "TestRetrievalModel",
        "model_version": "1.0",
        "organization": "TestOrg",
        "predictions": [
            {"id": "1", "prediction": ["d1", "dx"]},
            {"id": "2", "prediction": ["dx", "d2"]},
            {"id": "3", "prediction": ["d3", "dy"]},
        ],
        "is_internal": False,
        "submission_metadata": {"source": "pytest-retrieval"},
    }

    submit_resp = client.post("/api/submissions", json=submission_payload)
    assert submit_resp.status_code == 202, submit_resp.text
    submission_id = submit_resp.json()["data"]["submission_id"]

    from evaluation_service import evaluate_submission

    evaluate_submission(submission_id)

    status_resp = client.get(f"/api/submissions/{submission_id}")
    assert status_resp.status_code == 200, status_resp.text
    submission = status_resp.json()

    assert submission["status"] == SubmissionStatus.COMPLETED.value
    assert submission["primary_score"] is not None
    assert submission["detailed_scores"] is not None

    db = SessionLocal()
    try:
        ds = db.query(Dataset).filter(Dataset.id == dataset_id).first()
        sub = db.query(Submission).filter(Submission.id == submission_id).first()

        evaluator = get_evaluator(ds.task_type.value)
        scores = evaluator.evaluate(ds.ground_truth, sub.predictions)

        assert ds.primary_metric in scores
        assert pytest.approx(scores[ds.primary_metric]) == sub.primary_score
        for metric_name, metric_value in scores.items():
            assert metric_name in sub.detailed_scores
            assert pytest.approx(metric_value) == sub.detailed_scores[metric_name]
    finally:
        db.close()

