"""
Example usage of the Leaderboard API

This script demonstrates how to:
1. Create a new dataset
2. Submit model predictions
3. Check submission status
4. Query the leaderboard
"""

import requests
import json
import time

# API base URL (adjust for your deployment)
BASE_URL = "http://localhost:8000"


def create_sample_dataset():
    """Create a sample text classification dataset"""
    
    dataset = {
        "name": "Product Sentiment - Classification Accuracy",
        "description": "Binary sentiment classification for product reviews",
        "url": "https://example.com/product-sentiment-dataset",
        "task_type": "text_classification",
        "test_set_public": False,  # Keep test questions private to prevent gaming
        "labels_public": False,
        "primary_metric": "accuracy",
        "additional_metrics": ["f1", "precision", "recall"],
        "ground_truth": [
            {
                "id": "q1",
                "question": "This product exceeded my expectations!",
                "answer": "positive"
            },
            {
                "id": "q2",
                "question": "Terrible quality, broke after one use.",
                "answer": "negative"
            },
            {
                "id": "q3",
                "question": "Good value for money.",
                "answer": "positive"
            },
            {
                "id": "q4",
                "question": "Not worth the price.",
                "answer": "negative"
            },
            {
                "id": "q5",
                "question": "Amazing product, highly recommend!",
                "answer": "positive"
            }
        ]
    }
    
    response = requests.post(f"{BASE_URL}/api/datasets", json=dataset)
    
    if response.status_code == 201:
        data = response.json()
        print(f"✓ Dataset created: {data['data']['name']}")
        print(f"  Dataset ID: {data['data']['dataset_id']}")
        return data['data']['dataset_id']
    else:
        print(f"✗ Failed to create dataset: {response.json()}")
        return None


def submit_model_predictions(dataset_id: str):
    """Submit predictions from a hypothetical model"""
    
    submission = {
        "dataset_id": dataset_id,
        "model_name": "GPT-4o",
        "model_version": "2024-11-01",
        "organization": "OpenAI",
        "is_internal": False,
        "predictions": [
            {"id": "q1", "prediction": "positive"},
            {"id": "q2", "prediction": "negative"},
            {"id": "q3", "prediction": "positive"},
            {"id": "q4", "prediction": "negative"},
            {"id": "q5", "prediction": "positive"}
        ],
        "submission_metadata": {
            "temperature": 0.0,
            "max_tokens": 10
        }
    }
    
    response = requests.post(f"{BASE_URL}/api/submissions", json=submission)
    
    if response.status_code == 202:
        data = response.json()
        print(f"\n✓ Submission accepted: {submission['model_name']}")
        print(f"  Submission ID: {data['data']['submission_id']}")
        print(f"  Status: {data['data']['status']}")
        return data['data']['submission_id']
    else:
        print(f"✗ Failed to submit: {response.json()}")
        return None


def check_submission_status(submission_id: str, max_retries=10):
    """Poll submission status until evaluation is complete"""
    
    print(f"\nChecking evaluation status...")
    
    for i in range(max_retries):
        response = requests.get(f"{BASE_URL}/api/submissions/{submission_id}")
        
        if response.status_code == 200:
            data = response.json()
            status = data['status']
            
            print(f"  Attempt {i+1}: {status}")
            
            if status == "completed":
                print(f"\n✓ Evaluation completed!")
                print(f"  Model: {data['model_name']}")
                print(f"  Primary Score: {data['primary_score']}")
                print(f"  Detailed Scores: {json.dumps(data['detailed_scores'], indent=2)}")
                print(f"  Confidence Interval: {data['confidence_interval']}")
                return data
            elif status == "failed":
                print(f"\n✗ Evaluation failed: {data.get('error_message')}")
                return None
            
            time.sleep(2)  # Wait 2 seconds before next check
        else:
            print(f"✗ Failed to check status: {response.json()}")
            return None
    
    print("✗ Timeout waiting for evaluation")
    return None


def get_leaderboard(dataset_id: str):
    """Retrieve leaderboard for a dataset"""
    
    response = requests.get(f"{BASE_URL}/api/leaderboard/{dataset_id}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n{'='*60}")
        print(f"LEADERBOARD: {data['dataset_name']}")
        print(f"Task: {data['task_type']} | Metric: {data['primary_metric']}")
        print(f"{'='*60}")
        print(f"{'Rank':<6} {'Model':<30} {'Score':<10}")
        print(f"{'-'*60}")
        
        for entry in data['entries']:
            print(f"{entry['rank']:<6} {entry['model_name']:<30} {entry['score']:<10.4f}")
        
        print(f"{'='*60}\n")
        return data
    else:
        print(f"✗ Failed to get leaderboard: {response.json()}")
        return None


def submit_another_model(dataset_id: str):
    """Submit a second model with different accuracy"""
    
    submission = {
        "dataset_id": dataset_id,
        "model_name": "Claude 3.5 Sonnet",
        "model_version": "2024-10-22",
        "organization": "Anthropic",
        "is_internal": False,
        "predictions": [
            {"id": "q1", "prediction": "positive"},
            {"id": "q2", "prediction": "negative"},
            {"id": "q3", "prediction": "positive"},
            {"id": "q4", "prediction": "positive"},  # Wrong prediction
            {"id": "q5", "prediction": "positive"}
        ]
    }
    
    response = requests.post(f"{BASE_URL}/api/submissions", json=submission)
    
    if response.status_code == 202:
        data = response.json()
        print(f"\n✓ Second submission accepted: {submission['model_name']}")
        return data['data']['submission_id']
    return None


def main():
    """Run complete example workflow"""
    
    print("\n" + "="*60)
    print("LEADERBOARD API - EXAMPLE USAGE")
    print("="*60)
    
    # 1. Create dataset
    print("\n[1] Creating sample dataset...")
    dataset_id = create_sample_dataset()
    
    if not dataset_id:
        print("Failed to create dataset. Exiting.")
        return
    
    # 2. Submit first model
    print("\n[2] Submitting first model predictions...")
    submission_id_1 = submit_model_predictions(dataset_id)
    
    if not submission_id_1:
        print("Failed to submit predictions. Exiting.")
        return
    
    # 3. Wait for evaluation
    print("\n[3] Waiting for evaluation...")
    result_1 = check_submission_status(submission_id_1)
    
    # 4. Submit second model
    print("\n[4] Submitting second model...")
    submission_id_2 = submit_another_model(dataset_id)
    
    if submission_id_2:
        result_2 = check_submission_status(submission_id_2)
    
    # 5. View leaderboard
    print("\n[5] Viewing final leaderboard...")
    time.sleep(1)  # Brief pause for dramatic effect
    get_leaderboard(dataset_id)
    
    # 6. Query all leaderboards
    print("\n[6] Querying all leaderboards...")
    response = requests.get(f"{BASE_URL}/api/leaderboard")
    if response.status_code == 200:
        all_leaderboards = response.json()
        print(f"Total leaderboards: {len(all_leaderboards)}")
        for lb in all_leaderboards:
            print(f"  - {lb['dataset_name']}: {len(lb['entries'])} submissions")
    
    print("\n" + "="*60)
    print("EXAMPLE COMPLETED!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()

