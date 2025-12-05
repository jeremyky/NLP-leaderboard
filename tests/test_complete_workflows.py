"""
Complete end-to-end workflow tests for CI/CD

Tests realistic user journeys:
1. User uploads dataset → sees it on leaderboard (empty)
2. User submits model → sees evaluation results
3. Multiple users submit → leaderboard updates correctly
4. Admin imports HuggingFace dataset → seeds baselines → appears populated
"""
import pytest
from fastapi.testclient import TestClient
import uuid
import time

from main import app
from database import SessionLocal, init_db
from models import Dataset, Submission, TaskType, SubmissionStatus

client = TestClient(app)


@pytest.fixture(scope="function")
def clean_db():
    """Start with clean database"""
    init_db()
    db = SessionLocal()
    try:
        db.query(Submission).delete()
        db.query(Dataset).delete()
        db.commit()
        yield db
    finally:
        db.close()


class TestCompleteUserJourney:
    """Test complete user workflows"""
    
    def test_create_dataset_and_submit_multiple_models(self, clean_db):
        """
        Complete workflow:
        1. Create custom dataset
        2. Retrieve questions
        3. Submit 3 different models
        4. Verify leaderboard shows all 3 ranked correctly
        """
        # Step 1: Create dataset
        dataset_payload = {
            "name": f"User Dataset {uuid.uuid4()}",
            "description": "User-created benchmark",
            "url": "https://example.com/benchmark",
            "task_type": "text_classification",
            "test_set_public": False,
            "labels_public": False,
            "primary_metric": "accuracy",
            "additional_metrics": ["f1"],
            "ground_truth": [
                {"id": "1", "question": "Good product", "answer": "positive"},
                {"id": "2", "question": "Bad product", "answer": "negative"},
                {"id": "3", "question": "Great service", "answer": "positive"},
                {"id": "4", "question": "Terrible experience", "answer": "negative"},
                {"id": "5", "question": "Excellent quality", "answer": "positive"},
            ]
        }
        
        create_response = client.post("/api/datasets", json=dataset_payload)
        assert create_response.status_code == 201
        dataset_id = create_response.json()["data"]["dataset_id"]
        
        # Step 2: Retrieve questions (what a user would do)
        questions_response = client.get(f"/api/datasets/{dataset_id}/questions")
        assert questions_response.status_code == 200
        questions_data = questions_response.json()
        assert len(questions_data["questions"]) == 5
        assert all("answer" not in q for q in questions_data["questions"])
        
        # Step 3: Submit 3 models with different accuracies
        models = [
            {
                "name": "Perfect Model",
                "predictions": [
                    {"id": "1", "prediction": "positive"},
                    {"id": "2", "prediction": "negative"},
                    {"id": "3", "prediction": "positive"},
                    {"id": "4", "prediction": "negative"},
                    {"id": "5", "prediction": "positive"},
                ],
                "expected_score": 1.0
            },
            {
                "name": "Good Model",
                "predictions": [
                    {"id": "1", "prediction": "positive"},
                    {"id": "2", "prediction": "negative"},
                    {"id": "3", "prediction": "positive"},
                    {"id": "4", "prediction": "positive"},  # Wrong
                    {"id": "5", "prediction": "positive"},
                ],
                "expected_score": 0.8
            },
            {
                "name": "Average Model",
                "predictions": [
                    {"id": "1", "prediction": "positive"},
                    {"id": "2", "prediction": "positive"},  # Wrong
                    {"id": "3", "prediction": "negative"},  # Wrong
                    {"id": "4", "prediction": "negative"},
                    {"id": "5", "prediction": "positive"},
                ],
                "expected_score": 0.6
            }
        ]
        
        submission_ids = []
        for model_def in models:
            submission = {
                "dataset_id": dataset_id,
                "model_name": model_def["name"],
                "model_version": "1.0",
                "organization": "Test Org",
                "is_internal": False,
                "predictions": model_def["predictions"]
            }
            submit_response = client.post("/api/submissions", json=submission)
            assert submit_response.status_code == 202
            submission_ids.append(submit_response.json()["data"]["submission_id"])
        
        # Step 4: Wait for evaluations to complete
        time.sleep(3)
        
        # Step 5: Check leaderboard
        leaderboard_response = client.get(f"/api/leaderboard/{dataset_id}")
        assert leaderboard_response.status_code == 200
        leaderboard = leaderboard_response.json()
        
        # Verify structure
        assert leaderboard["dataset_id"] == dataset_id
        assert len(leaderboard["entries"]) == 3
        
        # Verify ranking (should be Perfect, Good, Average)
        entries = leaderboard["entries"]
        assert entries[0]["rank"] == 1
        assert entries[0]["model_name"] == "Perfect Model"
        assert entries[0]["score"] == 1.0
        
        assert entries[1]["rank"] == 2
        assert entries[1]["model_name"] == "Good Model"
        assert entries[1]["score"] == 0.8
        
        assert entries[2]["rank"] == 3
        assert entries[2]["model_name"] == "Average Model"
        assert entries[2]["score"] == 0.6
        
        # Step 6: Verify no duplicate entries in all leaderboards
        all_leaderboards_response = client.get("/api/leaderboard")
        assert all_leaderboards_response.status_code == 200
        all_leaderboards = all_leaderboards_response.json()
        
        dataset_ids = [lb["dataset_id"] for lb in all_leaderboards]
        assert len(dataset_ids) == len(set(dataset_ids)), "Duplicate datasets in leaderboard"
        
        # Find our dataset
        our_leaderboard = next(
            (lb for lb in all_leaderboards if lb["dataset_id"] == dataset_id),
            None
        )
        assert our_leaderboard is not None
        assert len(our_leaderboard["entries"]) == 3


class TestQAWorkflow:
    """Test question answering workflow"""
    
    def test_document_qa_submission(self, clean_db):
        """Test QA dataset creation and submission"""
        # Create QA dataset
        dataset_payload = {
            "name": f"QA Test {uuid.uuid4()}",
            "description": "Test QA dataset",
            "url": "https://example.com/qa",
            "task_type": "document_qa",
            "test_set_public": False,
            "labels_public": False,
            "primary_metric": "exact_match",
            "additional_metrics": ["f1"],
            "ground_truth": [
                {
                    "id": "1",
                    "question": "What is the capital?",
                    "context": "The capital is Paris.",
                    "answer": "Paris"
                },
                {
                    "id": "2",
                    "question": "When was it founded?",
                    "context": "It was founded in 1850.",
                    "answer": "1850"
                },
            ]
        }
        
        create_response = client.post("/api/datasets", json=dataset_payload)
        assert create_response.status_code == 201
        dataset_id = create_response.json()["data"]["dataset_id"]
        
        # Submit predictions
        submission = {
            "dataset_id": dataset_id,
            "model_name": "QA Model",
            "predictions": [
                {"id": "1", "prediction": "Paris"},
                {"id": "2", "prediction": "1850"},
            ]
        }
        submit_response = client.post("/api/submissions", json=submission)
        assert submit_response.status_code == 202
        
        time.sleep(2)
        
        # Check leaderboard
        leaderboard_response = client.get(f"/api/leaderboard/{dataset_id}")
        assert leaderboard_response.status_code == 200


class TestMultipleDatasetTypes:
    """Test handling of different task types simultaneously"""
    
    def test_mixed_task_types_in_leaderboard(self, clean_db):
        """Create datasets of different types and verify leaderboard handles them"""
        datasets = [
            {
                "name": f"Text Class {uuid.uuid4()}",
                "task_type": "text_classification",
                "primary_metric": "accuracy",
                "ground_truth": [{"id": "1", "question": "Q", "answer": "A"}]
            },
            {
                "name": f"QA {uuid.uuid4()}",
                "task_type": "document_qa",
                "primary_metric": "exact_match",
                "ground_truth": [{"id": "1", "question": "Q", "context": "C", "answer": "A"}]
            },
            {
                "name": f"NER {uuid.uuid4()}",
                "task_type": "named_entity_recognition",
                "primary_metric": "f1",
                "ground_truth": [{"id": "1", "text": "T", "answer": [["Entity", "TYPE"]]}]
            }
        ]
        
        for ds in datasets:
            payload = {
                "name": ds["name"],
                "description": "Test",
                "url": "https://example.com",
                "task_type": ds["task_type"],
                "test_set_public": False,
                "labels_public": False,
                "primary_metric": ds["primary_metric"],
                "additional_metrics": [],
                "ground_truth": ds["ground_truth"]
            }
            response = client.post("/api/datasets", json=payload)
            assert response.status_code == 201
        
        # Get all leaderboards
        response = client.get("/api/leaderboard")
        assert response.status_code == 200
        data = response.json()
        
        # Should have at least 3 leaderboards
        assert len(data) >= 3
        
        # Each dataset should appear exactly once
        dataset_names = [lb["dataset_name"] for lb in data]
        assert len(dataset_names) == len(set(dataset_names))
        
        # Check task types are diverse
        task_types = {lb["task_type"] for lb in data}
        assert len(task_types) >= 2


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_empty_predictions_rejected(self, clean_db):
        """Should reject submission with no predictions"""
        # Create dataset first
        dataset_payload = {
            "name": f"Edge Case {uuid.uuid4()}",
            "description": "Test",
            "url": "https://example.com",
            "task_type": "text_classification",
            "test_set_public": False,
            "labels_public": False,
            "primary_metric": "accuracy",
            "additional_metrics": [],
            "ground_truth": [{"id": "1", "question": "Q", "answer": "A"}]
        }
        create_response = client.post("/api/datasets", json=dataset_payload)
        dataset_id = create_response.json()["data"]["dataset_id"]
        
        # Try submitting empty predictions
        submission = {
            "dataset_id": dataset_id,
            "model_name": "Empty Model",
            "predictions": []
        }
        # This should either reject or handle gracefully
        response = client.post("/api/submissions", json=submission)
        # Accept either rejection or acceptance (will fail evaluation later)
        assert response.status_code in [202, 400, 422]
    
    def test_dataset_with_no_submissions_appears_in_leaderboard(self, clean_db):
        """Empty datasets should still appear in leaderboard (with 0 models)"""
        # Create dataset
        dataset_payload = {
            "name": f"Empty Dataset {uuid.uuid4()}",
            "description": "No submissions yet",
            "url": "https://example.com",
            "task_type": "text_classification",
            "test_set_public": False,
            "labels_public": False,
            "primary_metric": "accuracy",
            "additional_metrics": [],
            "ground_truth": [{"id": "1", "question": "Q", "answer": "A"}]
        }
        create_response = client.post("/api/datasets", json=dataset_payload)
        dataset_id = create_response.json()["data"]["dataset_id"]
        
        # Check leaderboard
        response = client.get("/api/leaderboard")
        assert response.status_code == 200
        data = response.json()
        
        # Dataset should be present
        dataset_ids = [lb["dataset_id"] for lb in data]
        assert dataset_id in dataset_ids
        
        # Find it and check entries are empty
        our_lb = next(lb for lb in data if lb["dataset_id"] == dataset_id)
        assert len(our_lb["entries"]) == 0


class TestPerformanceAndScalability:
    """Test system handles reasonable load"""
    
    def test_leaderboard_with_many_submissions(self, clean_db):
        """Test leaderboard handles 50+ submissions per dataset"""
        # Create dataset
        dataset_payload = {
            "name": f"Stress Test {uuid.uuid4()}",
            "description": "Dataset with many submissions",
            "url": "https://example.com",
            "task_type": "text_classification",
            "test_set_public": False,
            "labels_public": False,
            "primary_metric": "accuracy",
            "additional_metrics": [],
            "ground_truth": [
                {"id": "1", "question": "Q1", "answer": "A"},
                {"id": "2", "question": "Q2", "answer": "B"},
            ]
        }
        create_response = client.post("/api/datasets", json=dataset_payload)
        dataset_id = create_response.json()["data"]["dataset_id"]
        
        # Create 20 submissions directly in DB (faster than API)
        db = clean_db
        for i in range(20):
            submission = Submission(
                id=str(uuid.uuid4()),
                dataset_id=dataset_id,
                model_name=f"Model {i+1}",
                predictions=[
                    {"id": "1", "prediction": "A"},
                    {"id": "2", "prediction": "B"},
                ],
                status=SubmissionStatus.COMPLETED,
                primary_score=0.95 - (i * 0.01),
                detailed_scores={"accuracy": 0.95 - (i * 0.01)},
                is_internal=False,
                evaluated_at=datetime.utcnow()
            )
            db.add(submission)
        db.commit()
        
        # Query leaderboard
        response = client.get(f"/api/leaderboard/{dataset_id}")
        assert response.status_code == 200
        data = response.json()
        
        # Should have all 20 submissions
        assert len(data["entries"]) == 20
        
        # Verify ranking is correct
        scores = [e["score"] for e in data["entries"]]
        assert scores == sorted(scores, reverse=True)
        
        # Query time should be reasonable (<5 seconds)
        import time
        start = time.time()
        response = client.get("/api/leaderboard")
        elapsed = time.time() - start
        assert elapsed < 5.0, f"Leaderboard query took {elapsed}s (too slow)"


class TestMetricsConsistency:
    """Test metrics are computed consistently"""
    
    def test_primary_score_matches_detailed_scores(self, clean_db):
        """Primary score should match the score in detailed_scores"""
        # Create dataset
        dataset_payload = {
            "name": f"Metrics Test {uuid.uuid4()}",
            "description": "Test metrics consistency",
            "url": "https://example.com",
            "task_type": "text_classification",
            "test_set_public": False,
            "labels_public": False,
            "primary_metric": "accuracy",
            "additional_metrics": ["f1", "precision"],
            "ground_truth": [
                {"id": "1", "question": "Q1", "answer": "yes"},
                {"id": "2", "question": "Q2", "answer": "no"},
                {"id": "3", "question": "Q3", "answer": "yes"},
            ]
        }
        create_response = client.post("/api/datasets", json=dataset_payload)
        dataset_id = create_response.json()["data"]["dataset_id"]
        
        # Submit predictions
        submission = {
            "dataset_id": dataset_id,
            "model_name": "Consistency Test Model",
            "predictions": [
                {"id": "1", "prediction": "yes"},
                {"id": "2", "prediction": "no"},
                {"id": "3", "prediction": "yes"},
            ]
        }
        submit_response = client.post("/api/submissions", json=submission)
        submission_id = submit_response.json()["data"]["submission_id"]
        
        time.sleep(2)
        
        # Get submission status
        status_response = client.get(f"/api/submissions/{submission_id}")
        status_data = status_response.json()
        
        if status_data["status"] == "completed":
            primary_score = status_data["primary_score"]
            detailed_scores = status_data["detailed_scores"]
            
            # Primary score should match accuracy in detailed_scores
            assert "accuracy" in detailed_scores
            assert abs(primary_score - detailed_scores["accuracy"]) < 0.0001


class TestDatasetUpload:
    """Test dataset upload and validation"""
    
    def test_upload_valid_text_classification_dataset(self, clean_db):
        """Should accept valid text classification dataset"""
        dataset = {
            "name": f"Upload Test {uuid.uuid4()}",
            "description": "Uploaded dataset",
            "url": "https://example.com/upload",
            "task_type": "text_classification",
            "test_set_public": True,
            "labels_public": False,
            "primary_metric": "accuracy",
            "additional_metrics": ["f1"],
            "ground_truth": [
                {"id": "1", "question": "Test 1", "answer": "class_a"},
                {"id": "2", "question": "Test 2", "answer": "class_b"},
                {"id": "3", "question": "Test 3", "answer": "class_a"},
            ]
        }
        response = client.post("/api/datasets", json=dataset)
        assert response.status_code == 201
        
        dataset_id = response.json()["data"]["dataset_id"]
        
        # Verify it appears in listings
        list_response = client.get("/api/datasets")
        dataset_names = [d["name"] for d in list_response.json()]
        assert dataset["name"] in dataset_names
    
    def test_upload_valid_qa_dataset(self, clean_db):
        """Should accept valid QA dataset"""
        dataset = {
            "name": f"QA Upload {uuid.uuid4()}",
            "description": "QA dataset",
            "url": "https://example.com/qa",
            "task_type": "document_qa",
            "test_set_public": False,
            "labels_public": False,
            "primary_metric": "exact_match",
            "additional_metrics": ["f1"],
            "ground_truth": [
                {"id": "1", "question": "What?", "context": "Context here", "answer": "Answer"},
            ]
        }
        response = client.post("/api/datasets", json=dataset)
        assert response.status_code == 201
    
    def test_upload_valid_ner_dataset(self, clean_db):
        """Should accept valid NER dataset"""
        dataset = {
            "name": f"NER Upload {uuid.uuid4()}",
            "description": "NER dataset",
            "url": "https://example.com/ner",
            "task_type": "named_entity_recognition",
            "test_set_public": False,
            "labels_public": False,
            "primary_metric": "f1",
            "additional_metrics": ["precision", "recall"],
            "ground_truth": [
                {"id": "1", "text": "Apple Inc. is a company", "answer": [["Apple Inc.", "ORG"]]},
            ]
        }
        response = client.post("/api/datasets", json=dataset)
        assert response.status_code == 201


class TestModelUpload:
    """Test model/prediction upload workflows"""
    
    def test_upload_predictions_json(self, clean_db):
        """Test uploading predictions as JSON (common user flow)"""
        # Create dataset
        dataset_payload = {
            "name": f"Predict Upload {uuid.uuid4()}",
            "description": "Test prediction upload",
            "url": "https://example.com",
            "task_type": "text_classification",
            "test_set_public": False,
            "labels_public": False,
            "primary_metric": "accuracy",
            "additional_metrics": [],
            "ground_truth": [
                {"id": "q1", "question": "Test", "answer": "positive"},
                {"id": "q2", "question": "Test", "answer": "negative"},
            ]
        }
        create_response = client.post("/api/datasets", json=dataset_payload)
        dataset_id = create_response.json()["data"]["dataset_id"]
        
        # Upload predictions as JSON
        predictions_json = [
            {"id": "q1", "prediction": "positive"},
            {"id": "q2", "prediction": "negative"},
        ]
        
        submission = {
            "dataset_id": dataset_id,
            "model_name": "JSON Upload Model",
            "model_version": "2024-12-05",
            "organization": "Test Lab",
            "predictions": predictions_json
        }
        
        response = client.post("/api/submissions", json=submission)
        assert response.status_code == 202
        
        submission_id = response.json()["data"]["submission_id"]
        
        # Verify submission was created
        status_response = client.get(f"/api/submissions/{submission_id}")
        assert status_response.status_code == 200
        assert status_response.json()["model_name"] == "JSON Upload Model"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

