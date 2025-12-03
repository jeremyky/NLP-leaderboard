import os
import sys

import pytest
from fastapi.testclient import TestClient as FastAPITestClient

# Ensure project root on sys.path
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from main import app
from metrics_info import METRICS_CATALOG, get_metrics_for_task


@pytest.fixture
def client() -> FastAPITestClient:
    return FastAPITestClient(app)


def test_get_all_metrics_endpoint(client: FastAPITestClient):
    resp = client.get("/api/metrics")
    assert resp.status_code == 200
    data = resp.json()
    # Should at least contain all catalog keys
    for key in METRICS_CATALOG.keys():
        assert key in data


def test_get_single_metric_endpoint(client: FastAPITestClient):
    resp = client.get("/api/metrics/f1")
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"].lower().startswith("f1")
    assert "description" in data
    assert "formula" in data


def test_get_task_metrics_endpoint(client: FastAPITestClient):
    for task in ["text_classification", "named_entity_recognition", "document_qa", "retrieval"]:
        resp = client.get(f"/api/metrics/task/{task}")
        assert resp.status_code == 200
        data = resp.json()
        expected = get_metrics_for_task(task)
        # Response should contain at least the expected keys
        for metric_name in expected:
            assert metric_name in data


