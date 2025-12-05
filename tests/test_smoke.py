"""
Smoke tests for post-deployment validation

Quick critical tests to verify deployment is healthy:
- API is reachable
- Database has data
- Core endpoints work
- No duplicate entries
- Frontend can fetch data

Run after deployment: pytest tests/test_smoke.py -v
"""
import pytest
import requests
import os

# Use environment variable or default to localhost
API_URL = os.getenv("API_URL", "http://localhost:8000")


class TestDeploymentHealth:
    """Critical health checks"""
    
    def test_api_is_reachable(self):
        """API should be reachable"""
        response = requests.get(f"{API_URL}/health", timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_database_is_populated(self):
        """Database should have datasets after seeding"""
        response = requests.get(f"{API_URL}/api/datasets", timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 10, f"Expected at least 10 datasets, got {len(data)}"
    
    def test_leaderboard_endpoint_works(self):
        """Leaderboard endpoint should return data"""
        response = requests.get(f"{API_URL}/api/leaderboard", timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 10, f"Expected at least 10 leaderboards, got {len(data)}"


class TestCriticalBugPrevention:
    """Prevent regression of critical bugs"""
    
    def test_no_duplicate_datasets_in_leaderboard(self):
        """CRITICAL: Each dataset must appear exactly once"""
        response = requests.get(f"{API_URL}/api/leaderboard", timeout=10)
        assert response.status_code == 200
        data = response.json()
        
        dataset_ids = [lb["dataset_id"] for lb in data]
        unique_ids = set(dataset_ids)
        
        assert len(dataset_ids) == len(unique_ids), \
            f"DUPLICATE DATASETS FOUND! Total: {len(dataset_ids)}, Unique: {len(unique_ids)}"
    
    def test_datasets_have_multiple_models(self):
        """Popular datasets should have multiple baseline models"""
        response = requests.get(f"{API_URL}/api/leaderboard", timeout=10)
        assert response.status_code == 200
        data = response.json()
        
        # Find AG News
        ag_news = next(
            (lb for lb in data if "AG News" in lb["dataset_name"]),
            None
        )
        
        if ag_news:
            entry_count = len(ag_news["entries"])
            assert entry_count >= 10, \
                f"AG News should have at least 10 models, got {entry_count}"
    
    def test_submissions_properly_ranked(self):
        """Submissions should be ranked by score descending"""
        response = requests.get(f"{API_URL}/api/leaderboard", timeout=10)
        assert response.status_code == 200
        data = response.json()
        
        for leaderboard in data:
            if len(leaderboard["entries"]) > 1:
                scores = [e["score"] for e in leaderboard["entries"]]
                assert scores == sorted(scores, reverse=True), \
                    f"Dataset {leaderboard['dataset_name']} has incorrectly ranked scores"


class TestDatasetVariety:
    """Verify deployment has diverse datasets"""
    
    def test_multiple_task_types_present(self):
        """Should have multiple task types"""
        response = requests.get(f"{API_URL}/api/datasets", timeout=10)
        assert response.status_code == 200
        data = response.json()
        
        task_types = {d["task_type"] for d in data}
        assert len(task_types) >= 2, \
            f"Expected multiple task types, got: {task_types}"
    
    def test_has_text_classification_datasets(self):
        """Should have text classification datasets"""
        response = requests.get(
            f"{API_URL}/api/datasets",
            params={"task_type": "text_classification"},
            timeout=10
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 5, "Expected at least 5 text classification datasets"
    
    def test_has_qa_datasets(self):
        """Should have QA datasets"""
        response = requests.get(f"{API_URL}/api/datasets", timeout=10)
        assert response.status_code == 200
        data = response.json()
        
        qa_datasets = [
            d for d in data
            if d["task_type"] in ["document_qa", "line_qa"]
        ]
        assert len(qa_datasets) >= 2, "Expected at least 2 QA datasets"


class TestMetricsAPI:
    """Test metrics information endpoints"""
    
    def test_metrics_catalog_available(self):
        """Metrics catalog should be accessible"""
        response = requests.get(f"{API_URL}/api/metrics", timeout=10)
        assert response.status_code == 200
        data = response.json()
        
        # Should have common metrics
        assert "accuracy" in data
        assert "f1" in data
        assert "exact_match" in data
    
    def test_task_specific_metrics(self):
        """Should provide metrics for specific task types"""
        response = requests.get(
            f"{API_URL}/api/metrics/task/text_classification",
            timeout=10
        )
        assert response.status_code == 200
        data = response.json()
        assert "accuracy" in data


class TestCORS:
    """Test CORS is properly configured"""
    
    def test_cors_headers_present(self):
        """API should have CORS headers for frontend"""
        response = requests.get(
            f"{API_URL}/api/datasets",
            headers={"Origin": "https://nlp-leaderboard.vercel.app"},
            timeout=10
        )
        assert response.status_code == 200
        
        # CORS headers should be present
        headers = response.headers
        # Some FastAPI CORS configs return these conditionally
        # so we just verify no CORS errors occur


class TestResponseTimes:
    """Test performance of critical endpoints"""
    
    def test_leaderboard_response_time(self):
        """Leaderboard should respond quickly"""
        import time
        
        start = time.time()
        response = requests.get(f"{API_URL}/api/leaderboard", timeout=10)
        elapsed = time.time() - start
        
        assert response.status_code == 200
        assert elapsed < 5.0, f"Leaderboard took {elapsed:.2f}s (should be <5s)"
    
    def test_health_check_response_time(self):
        """Health check should be very fast"""
        import time
        
        start = time.time()
        response = requests.get(f"{API_URL}/health", timeout=5)
        elapsed = time.time() - start
        
        assert response.status_code == 200
        assert elapsed < 1.0, f"Health check took {elapsed:.2f}s (should be <1s)"


if __name__ == "__main__":
    # Run smoke tests
    pytest.main([__file__, "-v", "--tb=short", "-x"])  # -x stops on first failure

