import os
import sys
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
from models import Dataset, TaskType


@pytest.fixture(autouse=True)
def clean_db():
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


def _fake_hf_dataset() -> Dict[str, Any]:
    return {
        "name": "AG News (HuggingFace)",
        "description": "Imported AG News dataset from HuggingFace",
        "url": "https://huggingface.co/datasets/ag_news",
        "task_type": "text_classification",
        "test_set_public": False,
        "labels_public": False,
        "primary_metric": "accuracy",
        "additional_metrics": ["f1"],
        "ground_truth": [
            {"id": "1", "question": "Some news headline", "answer": "world"},
            {"id": "2", "question": "Another news headline", "answer": "business"},
        ],
    }


def test_hf_import_endpoint_creates_dataset(client: FastAPITestClient, monkeypatch: pytest.MonkeyPatch):
    """
    Test /api/admin/import-huggingface by monkeypatching HuggingFaceImporter
    so we don't depend on the external HF datasets-server.
    """
    from hf_importer import HuggingFaceImporter

    def fake_import_dataset(self, dataset_name: str, config: str = "default", split: str = "test", num_samples: int = 100):
        return _fake_hf_dataset()

    monkeypatch.setattr(HuggingFaceImporter, "import_dataset", fake_import_dataset, raising=True)

    resp = client.post(
        "/api/admin/import-huggingface",
        params={
            "dataset_name": "ag_news",
            "config": "default",
            "split": "test",
            "num_samples": 50,
        },
    )

    assert resp.status_code == 200, resp.text
    data = resp.json()["data"]
    dataset_id = data["dataset_id"]
    assert data["name"] == "AG News (HuggingFace)"
    assert data["num_examples"] == 2

    # Verify dataset persisted correctly
    db = SessionLocal()
    try:
        ds = db.query(Dataset).filter(Dataset.id == dataset_id).first()
        assert ds is not None
        assert ds.name == "AG News (HuggingFace)"
        assert ds.url == "https://huggingface.co/datasets/ag_news"
        assert ds.task_type == TaskType.TEXT_CLASSIFICATION
        assert ds.primary_metric == "accuracy"
        assert ds.additional_metrics == ["f1"]
        assert len(ds.ground_truth) == 2
    finally:
        db.close()


