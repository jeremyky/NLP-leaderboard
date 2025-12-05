"""
Leaderboard integrity tests for CI/CD

Critical tests to prevent regression of common bugs:
- No duplicate dataset entries in leaderboard API
- All models shown for each dataset
- Proper ranking and sorting
- Internal vs external submission filtering
"""
import pytest
from fastapi.testclient import TestClient
import uuid

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
def dataset_with_multiple_submissions(db_session):
    """Create a dataset with 10 submissions to test deduplication"""
    dataset_id = str(uuid.uuid4())
    dataset = Dataset(
        id=dataset_id,
        name=f"Test Dataset {uuid.uuid4()}",
        description="Dataset with multiple submissions",
        url="https://example.com/test",
        task_type=TaskType.TEXT_CLASSIFICATION,
        test_set_public=False,
        labels_public=False,
        primary_metric="accuracy",
        additional_metrics=["f1"],
        num_examples=3,
        ground_truth=[
            {"id": "1", "question": "Q1", "answer": "A"},
            {"id": "2", "question": "Q2", "answer": "B"},
            {"id": "3", "question": "Q3", "answer": "C"},
        ]
    )
    db_session.add(dataset)
    db_session.flush()
    
    # Create 10 submissions
    for i in range(10):
        submission = Submission(
            id=str(uuid.uuid4()),
            dataset_id=dataset_id,
            model_name=f"Model {i+1}",
            model_version="1.0",
            organization="Test",
            predictions=[
                {"id": "1", "prediction": "A"},
                {"id": "2", "prediction": "B"},
                {"id": "3", "prediction": "C"},
            ],
            status=SubmissionStatus.COMPLETED,
            primary_score=0.90 - (i * 0.01),  # Decreasing scores
            detailed_scores={"accuracy": 0.90 - (i * 0.01)},
            is_internal=(i < 5),  # First 5 are internal
            evaluated_at=db_session.query(Dataset).first().created_at
        )
        db_session.add(submission)
    
    db_session.commit()
    db_session.refresh(dataset)
    return dataset


class TestLeaderboardDeduplication:
    """Test that leaderboards don't have duplicate dataset entries"""
    
    def test_no_duplicate_datasets_in_all_leaderboards(self, dataset_with_multiple_submissions):
        """CRITICAL: Each dataset should appear EXACTLY ONCE in /api/leaderboard response"""
        response = client.get("/api/leaderboard")
        assert response.status_code == 200
        data = response.json()
        
        # Count occurrences of each dataset_id
        dataset_counts = {}
        for leaderboard in data:
            dataset_id = leaderboard["dataset_id"]
            dataset_counts[dataset_id] = dataset_counts.get(dataset_id, 0) + 1
        
        # Assert no duplicates
        for dataset_id, count in dataset_counts.items():
            assert count == 1, f"Dataset {dataset_id} appears {count} times (should be 1)"
    
    def test_all_submissions_in_single_entry(self, dataset_with_multiple_submissions):
        """Each dataset's leaderboard should contain ALL submissions in entries array"""
        response = client.get("/api/leaderboard")
        assert response.status_code == 200
        data = response.json()
        
        # Find our test dataset
        test_leaderboard = next(
            (lb for lb in data if lb["dataset_id"] == dataset_with_multiple_submissions.id),
            None
        )
        assert test_leaderboard is not None, "Test dataset not found in leaderboard"
        
        # Should have exactly 10 entries (all submissions)
        assert len(test_leaderboard["entries"]) == 10, \
            f"Expected 10 entries, got {len(test_leaderboard['entries'])}"
        
        # Verify all models are present
        model_names = {e["model_name"] for e in test_leaderboard["entries"]}
        expected_models = {f"Model {i+1}" for i in range(10)}
        assert model_names == expected_models


class TestLeaderboardRanking:
    """Test ranking and sorting logic"""
    
    def test_submissions_sorted_by_score_descending(self, dataset_with_multiple_submissions):
        """Submissions should be ranked from highest to lowest score"""
        response = client.get(f"/api/leaderboard/{dataset_with_multiple_submissions.id}")
        assert response.status_code == 200
        data = response.json()
        
        # Check scores are descending
        scores = [entry["score"] for entry in data["entries"]]
        assert scores == sorted(scores, reverse=True), "Scores not in descending order"
        
        # Check ranks are sequential starting from 1
        ranks = [entry["rank"] for entry in data["entries"]]
        assert ranks == list(range(1, len(ranks) + 1)), "Ranks not sequential"
    
    def test_rank_1_has_highest_score(self, dataset_with_multiple_submissions):
        """Rank 1 should have the highest score"""
        response = client.get(f"/api/leaderboard/{dataset_with_multiple_submissions.id}")
        assert response.status_code == 200
        data = response.json()
        
        if len(data["entries"]) > 0:
            rank_1 = next(e for e in data["entries"] if e["rank"] == 1)
            all_scores = [e["score"] for e in data["entries"]]
            assert rank_1["score"] == max(all_scores)


class TestInternalExternalFiltering:
    """Test filtering of internal vs external submissions"""
    
    def test_include_internal_true(self, dataset_with_multiple_submissions):
        """Should include internal submissions when include_internal=true"""
        response = client.get(
            f"/api/leaderboard/{dataset_with_multiple_submissions.id}",
            params={"include_internal": True}
        )
        assert response.status_code == 200
        data = response.json()
        
        # Should have both internal and external (10 total)
        assert len(data["entries"]) == 10
        
        internal_count = sum(1 for e in data["entries"] if e["is_internal"])
        external_count = sum(1 for e in data["entries"] if not e["is_internal"])
        
        assert internal_count == 5
        assert external_count == 5
    
    def test_include_internal_false(self, dataset_with_multiple_submissions):
        """Should exclude internal submissions when include_internal=false"""
        response = client.get(
            f"/api/leaderboard/{dataset_with_multiple_submissions.id}",
            params={"include_internal": False}
        )
        assert response.status_code == 200
        data = response.json()
        
        # Should only have external submissions (5 total)
        assert len(data["entries"]) == 5
        assert all(not e["is_internal"] for e in data["entries"])


class TestDataIntegrity:
    """Test data consistency and completeness"""
    
    def test_submission_has_all_required_fields(self, dataset_with_multiple_submissions):
        """Each leaderboard entry should have all required fields"""
        response = client.get(f"/api/leaderboard/{dataset_with_multiple_submissions.id}")
        assert response.status_code == 200
        data = response.json()
        
        required_fields = [
            "rank", "model_name", "score", "confidence_interval",
            "updated_at", "is_internal", "submission_id", "detailed_scores"
        ]
        
        for entry in data["entries"]:
            for field in required_fields:
                assert field in entry, f"Missing field: {field}"
    
    def test_detailed_scores_contain_primary_metric(self, dataset_with_multiple_submissions):
        """Detailed scores should include the primary metric"""
        response = client.get(f"/api/leaderboard/{dataset_with_multiple_submissions.id}")
        assert response.status_code == 200
        data = response.json()
        
        primary_metric = data["primary_metric"]
        
        for entry in data["entries"]:
            if entry["detailed_scores"]:
                assert primary_metric in entry["detailed_scores"], \
                    f"Primary metric '{primary_metric}' not in detailed_scores"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

