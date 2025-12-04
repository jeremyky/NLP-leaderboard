"""
Comprehensive tests for SST-2 - Sentiment Analysis

Run with: pytest tests/dataset_tests/test_dataset_sst2.py -v
"""
import pytest
from tests.fixtures.text_classification.sst2_comprehensive import (
    ALL_TEST_CASES,
    STANDARD_CASES,
    EDGE_CASES,
    ADVERSARIAL_CASES
)
from evaluators import TextClassificationEvaluator


class TestSST2Comprehensive:
    """Comprehensive test suite for SST-2 Sentiment dataset"""
    
    pass
    
#     @pytest.fixture
#     def evaluator(self):
#         return TextClassificationEvaluator()
#     
#     def test_perfect_predictions_all_cases(self, evaluator):
#         """Test perfect accuracy on all generated test cases"""
#         predictions = [
#             {"id": item["id"], "prediction": item["answer"]}
#             for item in ALL_TEST_CASES
#         ]
#         
#         scores = evaluator.evaluate(ALL_TEST_CASES, predictions)
#         
#         assert scores["accuracy"] == pytest.approx(1.0)
#         assert scores["f1"] == pytest.approx(1.0)
#         print(f"✅ Perfect accuracy on {len(ALL_TEST_CASES)} SST-2 test cases")
#     
#     def test_binary_label_distribution(self, evaluator):
#         """Verify test cases have balanced positive/negative distribution"""
#         labels = [item["answer"] for item in STANDARD_CASES]
#         positive_count = labels.count("positive")
#         negative_count = labels.count("negative")
#         total = len(STANDARD_CASES)
#         
#         print(f"\nLabel distribution across {total} cases:")
#         print(f"  positive: {positive_count} ({positive_count/total*100:.1f}%)")
#         print(f"  negative: {negative_count} ({negative_count/total*100:.1f}%)")
#         
#         # Both classes should be present
#         assert positive_count > 0
#         assert negative_count > 0
#         
#         # Should be roughly balanced (40-60% for each class)
#         assert 0.4 <= positive_count / total <= 0.6
#         assert 0.4 <= negative_count / total <= 0.6
#     
#     def test_90_percent_accuracy_binary(self, evaluator):
#         """Test known accuracy on binary classification"""
#         sample = STANDARD_CASES[:100] if len(STANDARD_CASES) >= 100 else STANDARD_CASES
#         correct_count = int(len(sample) * 0.9)
#         
#         predictions = []
#         for i, item in enumerate(sample):
#             if i < correct_count:
#                 predictions.append({"id": item["id"], "prediction": item["answer"]})
#             else:
#                 # Flip sentiment
#                 wrong = "negative" if item["answer"] == "positive" else "positive"
#                 predictions.append({"id": item["id"], "prediction": wrong})
#         
#         scores = evaluator.evaluate(sample, predictions)
#         assert scores["accuracy"] == pytest.approx(0.9, abs=0.01)
#     
#     def test_negation_adversarial_cases(self, evaluator):
#         """Test that negations are evaluated correctly"""
#         # Filter for negation examples
#         negation_cases = [
#             c for c in ADVERSARIAL_CASES 
#             if any(word in c["question"].lower() for word in ["not", "n't", "never", "hardly", "barely"])
#         ]
#         
#         if not negation_cases:
#             pytest.skip("No negation cases defined yet")
#         
#         # Perfect predictions
#         predictions = [
#             {"id": item["id"], "prediction": item["answer"]}
#             for item in negation_cases
#         ]
#         
#         scores = evaluator.evaluate(negation_cases, predictions)
#         assert scores["accuracy"] == pytest.approx(1.0)
#         print(f"✅ Correctly evaluated {len(negation_cases)} negation cases")
#     
#     def test_edge_case_single_word_positive(self, evaluator):
#         """Test single positive word"""
#         ground_truth = [{"id": "1", "question": "brilliant", "answer": "positive"}]
#         predictions = [{"id": "1", "prediction": "positive"}]
#         
#         scores = evaluator.evaluate(ground_truth, predictions)
#         assert scores["accuracy"] == pytest.approx(1.0)
#     
#     def test_edge_case_single_word_negative(self, evaluator):
#         """Test single negative word"""
#         ground_truth = [{"id": "1", "question": "terrible", "answer": "negative"}]
#         predictions = [{"id": "1", "prediction": "negative"}]
#         
#         scores = evaluator.evaluate(ground_truth, predictions)
#         assert scores["accuracy"] == pytest.approx(1.0)
#     
#     def test_all_positive_predictions_on_balanced_set(self, evaluator):
#         """Test what happens if model always predicts positive"""
#         sample = STANDARD_CASES[:50] if len(STANDARD_CASES) >= 50 else STANDARD_CASES
#         
#         # Predict all positive
#         predictions = [
#             {"id": item["id"], "prediction": "positive"}
#             for item in sample
#         ]
#         
#         scores = evaluator.evaluate(sample, predictions)
#         
#         # Accuracy should be ~50% if dataset is balanced
#         assert 0.4 <= scores["accuracy"] <= 0.6
#         
#         # Recall for positive should be 1.0, for negative should be 0.0
#         # Precision for positive should be ~0.5
#         print(f"All-positive baseline: {scores['accuracy']:.2f} accuracy")
#     
#     def test_confusion_matrix_binary(self, evaluator):
#         """Test confusion matrix for binary classification"""
#         # Create specific scenario: TP=40, TN=40, FP=10, FN=10
#         ground_truth = (
#             [{"id": f"tp_{i}", "question": "positive example", "answer": "positive"} for i in range(50)] +
#             [{"id": f"tn_{i}", "question": "negative example", "answer": "negative"} for i in range(50)]
#         )
#         
#         predictions = []
#         # 40 correct positives, 10 wrong (FN)
#         for i in range(50):
#             pred = "positive" if i < 40 else "negative"
#             predictions.append({"id": f"tp_{i}", "prediction": pred})
#         
#         # 40 correct negatives, 10 wrong (FP)
#         for i in range(50):
#             pred = "negative" if i < 40 else "positive"
#             predictions.append({"id": f"tn_{i}", "prediction": pred})
#         
#         scores = evaluator.evaluate(ground_truth, predictions)
#         
#         # Accuracy = (TP + TN) / Total = 80/100 = 0.8
#         assert scores["accuracy"] == pytest.approx(0.8)
#         
#         # Precision = TP / (TP + FP) = 40 / (40 + 10) = 0.8
#         assert scores["precision"] == pytest.approx(0.8, abs=0.01)
#         
#         # Recall = TP / (TP + FN) = 40 / (40 + 10) = 0.8
#         assert scores["recall"] == pytest.approx(0.8, abs=0.01)

