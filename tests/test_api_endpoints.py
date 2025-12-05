"""
Comprehensive API endpoint tests for CI/CD

Tests all major API endpoints:
- Health check
- Dataset listing and retrieval
- Submission creation and status
- Leaderboard queries
- Metrics info
- Admin endpoints
"""
import pytest
from fastapi.testclient import TestClient
import uuid
from datetime import datetime

from main import app
from database import SessionLocal, init_db
from models import Dataset, Submission, TaskType, SubmissionStatus

client = TestClient(app)


@pytest.fixture(scope="function")
def db_session(clean_db):
    """Create a fresh database for each test"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def sample_dataset(db_session):
    """Create a sample dataset for testing"""
    dataset_id = str(uuid.uuid4())
    dataset = Dataset(
        id=dataset_id,
        name="Test Dataset - Classification",
        description="Test dataset for API testing",
        url="https://example.com/test",
        task_type=TaskType.TEXT_CLASSIFICATION,
        test_set_public=False,
        labels_public=False,
        primary_metric="accuracy",
        additional_metrics=["f1", "precision"],
        num_examples=5,
        ground_truth=[
            {"id": "1", "question": "Test question 1", "answer": "positive"},
            {"id": "2", "question": "Test question 2", "answer": "negative"},
            {"id": "3", "question": "Test question 3", "answer": "positive"},
            {"id": "4", "question": "Test question 4", "answer": "negative"},
            {"id": "5", "question": "Test question 5", "answer": "positive"},
        ]
    )
    db_session.add(dataset)
    db_session.commit()
    db_session.refresh(dataset)
    return dataset


class TestHealthCheck:
    """Test health check endpoint"""
    
    def test_health_check(self):
        """Health endpoint should return 200"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "leaderboard-api"


class TestDatasetEndpoints:
    """Test dataset CRUD operations"""
    
    def test_list_datasets(self, sample_dataset):
        """Should list all datasets"""
        response = client.get("/api/datasets")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        
        # Check dataset structure
        dataset = data[0]
        assert "id" in dataset
        assert "name" in dataset
        assert "task_type" in dataset
        assert "primary_metric" in dataset
    
    def test_get_dataset_by_id(self, sample_dataset):
        """Should retrieve specific dataset"""
        response = client.get(f"/api/datasets/{sample_dataset.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_dataset.id
        assert data["name"] == sample_dataset.name
    
    def test_get_nonexistent_dataset(self):
        """Should return 404 for nonexistent dataset"""
        fake_id = str(uuid.uuid4())
        response = client.get(f"/api/datasets/{fake_id}")
        assert response.status_code == 404
    
    def test_filter_datasets_by_task_type(self, sample_dataset):
        """Should filter datasets by task type"""
        response = client.get("/api/datasets", params={"task_type": "text_classification"})
        assert response.status_code == 200
        data = response.json()
        assert all(d["task_type"] == "text_classification" for d in data)
    
    def test_get_dataset_questions(self, sample_dataset):
        """Should retrieve dataset questions without answers"""
        response = client.get(f"/api/datasets/{sample_dataset.id}/questions")
        assert response.status_code == 200
        data = response.json()
        assert data["dataset_id"] == sample_dataset.id
        assert "questions" in data
        assert len(data["questions"]) == 5
        # Ensure answers are not exposed
        for q in data["questions"]:
            assert "answer" not in q
            assert "id" in q
    
    def test_create_dataset(self, db_session):
        """Should create a new dataset"""
        new_dataset = {
            "name": "New Test Dataset",
            "description": "Created via API",
            "url": "https://example.com/new",
            "task_type": "text_classification",
            "test_set_public": False,
            "labels_public": False,
            "primary_metric": "accuracy",
            "additional_metrics": ["f1"],
            "ground_truth": [
                {"id": "1", "question": "Q1", "answer": "A1"},
                {"id": "2", "question": "Q2", "answer": "A2"},
            ]
        }
        response = client.post("/api/datasets", json=new_dataset)
        assert response.status_code == 201
        data = response.json()
        assert data["message"] == "Dataset created successfully"
        assert "dataset_id" in data["data"]
    
    def test_create_duplicate_dataset(self, sample_dataset):
        """Should reject duplicate dataset names"""
        duplicate = {
            "name": sample_dataset.name,
            "description": "Duplicate",
            "url": "https://example.com",
            "task_type": "text_classification",
            "test_set_public": False,
            "labels_public": False,
            "primary_metric": "accuracy",
            "additional_metrics": [],
            "ground_truth": [{"id": "1", "question": "Q", "answer": "A"}]
        }
        response = client.post("/api/datasets", json=duplicate)
        assert response.status_code == 400


class TestSubmissionEndpoints:
    """Test submission creation and retrieval"""
    
    def test_submit_predictions(self, sample_dataset):
        """Should accept and evaluate submission"""
        submission = {
            "dataset_id": sample_dataset.id,
            "model_name": "Test Model",
            "model_version": "1.0",
            "organization": "Test Org",
            "is_internal": False,
            "predictions": [
                {"id": "1", "prediction": "positive"},
                {"id": "2", "prediction": "negative"},
                {"id": "3", "prediction": "positive"},
                {"id": "4", "prediction": "negative"},
                {"id": "5", "prediction": "positive"},
            ]
        }
        response = client.post("/api/submissions", json=submission)
        assert response.status_code == 202
        data = response.json()
        assert "submission_id" in data["data"]
        assert data["data"]["status"] == "pending"
        
        # Check submission status
        submission_id = data["data"]["submission_id"]
        return submission_id
    
    def test_get_submission_status(self, sample_dataset):
        """Should retrieve submission status"""
        # First create a submission
        submission = {
            "dataset_id": sample_dataset.id,
            "model_name": "Test Model 2",
            "model_version": "1.0",
            "organization": "Test Org",
            "is_internal": False,
            "predictions": [
                {"id": "1", "prediction": "positive"},
                {"id": "2", "prediction": "negative"},
                {"id": "3", "prediction": "positive"},
                {"id": "4", "prediction": "negative"},
                {"id": "5", "prediction": "positive"},
            ]
        }
        submit_response = client.post("/api/submissions", json=submission)
        submission_id = submit_response.json()["data"]["submission_id"]
        
        # Get status
        response = client.get(f"/api/submissions/{submission_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == submission_id
        assert "status" in data
        assert "model_name" in data
    
    def test_submit_to_nonexistent_dataset(self):
        """Should reject submission to nonexistent dataset"""
        fake_id = str(uuid.uuid4())
        submission = {
            "dataset_id": fake_id,
            "model_name": "Test",
            "predictions": [{"id": "1", "prediction": "test"}]
        }
        response = client.post("/api/submissions", json=submission)
        assert response.status_code == 404
    
    def test_list_submissions(self, sample_dataset):
        """Should list all submissions"""
        response = client.get("/api/submissions")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_filter_submissions_by_dataset(self, sample_dataset):
        """Should filter submissions by dataset"""
        response = client.get("/api/submissions", params={"dataset_id": sample_dataset.id})
        assert response.status_code == 200
        data = response.json()
        assert all(s["dataset_id"] == sample_dataset.id for s in data)


class TestLeaderboardEndpoints:
    """Test leaderboard queries"""
    
    def test_get_all_leaderboards(self, sample_dataset):
        """Should retrieve all leaderboards"""
        response = client.get("/api/leaderboard")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        
        # Verify no duplicate dataset entries
        dataset_ids = [lb["dataset_id"] for lb in data]
        assert len(dataset_ids) == len(set(dataset_ids)), "Duplicate dataset entries found"
    
    def test_get_single_dataset_leaderboard(self, sample_dataset):
        """Should retrieve leaderboard for specific dataset"""
        response = client.get(f"/api/leaderboard/{sample_dataset.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["dataset_id"] == sample_dataset.id
        assert "entries" in data
        assert isinstance(data["entries"], list)
    
    def test_filter_leaderboard_by_task_type(self, sample_dataset):
        """Should filter leaderboards by task type"""
        response = client.get("/api/leaderboard", params={"task_type": "text_classification"})
        assert response.status_code == 200
        data = response.json()
        assert all(lb["task_type"] == "text_classification" for lb in data)
    
    def test_leaderboard_excludes_internal(self, sample_dataset):
        """Should support filtering out internal submissions"""
        response = client.get(
            f"/api/leaderboard/{sample_dataset.id}",
            params={"include_internal": False}
        )
        assert response.status_code == 200
        data = response.json()
        # Should only show external submissions
        assert all(not entry["is_internal"] for entry in data["entries"])


class TestMetricsEndpoints:
    """Test metrics information endpoints"""
    
    def test_get_all_metrics(self):
        """Should list all available metrics"""
        response = client.get("/api/metrics")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "accuracy" in data
        assert "f1" in data
    
    def test_get_specific_metric(self):
        """Should retrieve info for specific metric"""
        response = client.get("/api/metrics/accuracy")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "description" in data
    
    def test_get_metrics_for_task(self):
        """Should list metrics relevant to task type"""
        response = client.get("/api/metrics/task/text_classification")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "accuracy" in data


class TestAdminEndpoints:
    """Test admin/management endpoints"""
    
    def test_cache_stats(self):
        """Should retrieve cache statistics"""
        response = client.get("/api/admin/cache-stats")
        assert response.status_code == 200
        data = response.json()
        assert "hits" in data or "size" in data or "keys" in data
    
    def test_clear_cache(self):
        """Should clear cache"""
        response = client.post("/api/admin/clear-cache")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Cache cleared successfully"


class TestEndToEndWorkflow:
    """Test complete workflows from dataset creation to leaderboard"""
    
    def test_full_submission_workflow(self, db_session):
        """Test complete flow: create dataset → submit → check leaderboard"""
        # 1. Create dataset
        dataset_payload = {
            "name": f"E2E Test Dataset {uuid.uuid4()}",
            "description": "End-to-end test",
            "url": "https://example.com/e2e",
            "task_type": "text_classification",
            "test_set_public": False,
            "labels_public": False,
            "primary_metric": "accuracy",
            "additional_metrics": ["f1", "precision"],
            "ground_truth": [
                {"id": "1", "question": "Q1", "answer": "positive"},
                {"id": "2", "question": "Q2", "answer": "negative"},
                {"id": "3", "question": "Q3", "answer": "positive"},
            ]
        }
        create_response = client.post("/api/datasets", json=dataset_payload)
        assert create_response.status_code == 201
        dataset_id = create_response.json()["data"]["dataset_id"]
        
        # 2. Submit predictions
        submission_payload = {
            "dataset_id": dataset_id,
            "model_name": "E2E Test Model",
            "model_version": "1.0",
            "organization": "E2E Org",
            "is_internal": False,
            "predictions": [
                {"id": "1", "prediction": "positive"},
                {"id": "2", "prediction": "negative"},
                {"id": "3", "prediction": "positive"},
            ]
        }
        submit_response = client.post("/api/submissions", json=submission_payload)
        assert submit_response.status_code == 202
        submission_id = submit_response.json()["data"]["submission_id"]
        
        # 3. Wait for evaluation (in real scenario, would poll)
        import time
        time.sleep(2)
        
        # 4. Check submission status
        status_response = client.get(f"/api/submissions/{submission_id}")
        assert status_response.status_code == 200
        status_data = status_response.json()
        assert status_data["status"] in ["pending", "processing", "completed"]
        
        # 5. Check leaderboard includes submission
        leaderboard_response = client.get(f"/api/leaderboard/{dataset_id}")
        assert leaderboard_response.status_code == 200
        leaderboard_data = leaderboard_response.json()
        
        # If evaluation completed, check it's in leaderboard
        if status_data["status"] == "completed":
            model_names = [e["model_name"] for e in leaderboard_data["entries"]]
            assert "E2E Test Model" in model_names


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

