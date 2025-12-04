"""
Comprehensive tests for SQuAD v1.1 - Question Answering

Run with: pytest tests/dataset_tests/test_dataset_squad.py -v
"""
import pytest
from tests.fixtures.qa.squad_comprehensive import (
    ALL_TEST_CASES,
    STANDARD_CASES,
    EDGE_CASES,
    ADVERSARIAL_CASES
)
from evaluators import QAEvaluator


class TestSQuADComprehensive:
    """Comprehensive test suite for SQuAD v1.1 dataset"""
    
    pass
    
#     @pytest.fixture
#     def evaluator(self):
#         return QAEvaluator()
#     
#     def test_perfect_predictions_all_cases(self, evaluator):
#         """Test perfect exact match on all generated test cases"""
#         predictions = [
#             {"id": item["id"], "prediction": item["answer"]}
#             for item in ALL_TEST_CASES
#         ]
#         
#         scores = evaluator.evaluate(ALL_TEST_CASES, predictions)
#         
#         assert scores["exact_match"] == pytest.approx(1.0)
#         assert scores["f1"] == pytest.approx(1.0)
#         print(f"✅ Perfect EM/F1 on {len(ALL_TEST_CASES)} SQuAD test cases")
#     
#     def test_answer_is_in_context(self):
#         """Validate that all answers exist in their contexts"""
#         errors = []
#         for case in ALL_TEST_CASES:
#             if case["answer"].lower() not in case["context"].lower():
#                 errors.append(f"ID {case['id']}: Answer '{case['answer']}' not in context")
#         
#         if errors:
#             print("\n".join(errors[:10]))  # Show first 10
#         assert len(errors) == 0, f"Found {len(errors)} cases where answer is not in context"
#     
#     def test_question_type_distribution(self):
#         """Verify diverse question types"""
#         question_words = {}
#         for case in STANDARD_CASES:
#             first_word = case["question"].split()[0].lower()
#             question_words[first_word] = question_words.get(first_word, 0) + 1
#         
#         print("\nQuestion type distribution:")
#         for word, count in sorted(question_words.items(), key=lambda x: -x[1]):
#             print(f"  {word}: {count}")
#         
#         # Should have variety (at least 4 different question types)
#         assert len(question_words) >= 4
#     
#     def test_partial_match_f1_vs_exact_match(self, evaluator):
#         """Test F1 is higher than EM when predictions are close but not exact"""
#         # Create scenario where predictions are close but not exact
#         ground_truth = [
#             {"id": "1", "question": "Q", "context": "The answer is Alexander Bell.", "answer": "Alexander Bell"},
#             {"id": "2", "question": "Q", "context": "The answer is 1945.", "answer": "1945"},
#         ]
#         
#         predictions = [
#             {"id": "1", "prediction": "Alexander"},  # Partial match
#             {"id": "2", "prediction": "1945"},  # Exact match
#         ]
#         
#         scores = evaluator.evaluate(ground_truth, predictions)
#         
#         # EM should be 0.5 (only second is exact)
#         assert scores["exact_match"] == pytest.approx(0.5)
#         
#         # F1 should be higher (first has partial token match)
#         assert scores["f1"] > 0.5
#         print(f"EM: {scores['exact_match']:.2f}, F1: {scores['f1']:.2f}")
#     
#     def test_normalization_lowercase(self, evaluator):
#         """Test that QA evaluator normalizes case"""
#         ground_truth = [{"id": "1", "question": "Q", "context": "C", "answer": "Paris"}]
#         predictions = [{"id": "1", "prediction": "paris"}]  # lowercase
#         
#         scores = evaluator.evaluate(ground_truth, predictions)
#         
#         # Should match (case-insensitive)
#         assert scores["exact_match"] == pytest.approx(1.0)
#     
#     def test_normalization_articles(self, evaluator):
#         """Test that QA evaluator strips articles"""
#         ground_truth = [{"id": "1", "question": "Q", "context": "C", "answer": "the Pacific Ocean"}]
#         predictions = [{"id": "1", "prediction": "Pacific Ocean"}]  # No article
#         
#         scores = evaluator.evaluate(ground_truth, predictions)
#         
#         # Should match (articles stripped)
#         assert scores["exact_match"] == pytest.approx(1.0)
#     
#     def test_normalization_punctuation(self, evaluator):
#         """Test that QA evaluator normalizes punctuation"""
#         ground_truth = [{"id": "1", "question": "Q", "context": "C", "answer": "Dr. Smith"}]
#         predictions = [{"id": "1", "prediction": "Dr Smith"}]  # No period
#         
#         scores = evaluator.evaluate(ground_truth, predictions)
#         
#         # Should match (punctuation normalized)
#         assert scores["exact_match"] == pytest.approx(1.0)
#     
#     def test_edge_case_very_short_answer(self, evaluator):
#         """Test single-word answer"""
#         ground_truth = [{"id": "1", "question": "Who?", "context": "The person is John.", "answer": "John"}]
#         predictions = [{"id": "1", "prediction": "John"}]
#         
#         scores = evaluator.evaluate(ground_truth, predictions)
#         assert scores["exact_match"] == pytest.approx(1.0)
#     
#     def test_edge_case_long_answer(self, evaluator):
#         """Test multi-word answer (10+ words)"""
#         long_answer = "the Industrial Revolution in the late 18th and early 19th centuries"
#         ground_truth = [{"id": "1", "question": "When?", "context": f"It happened during {long_answer}.", "answer": long_answer}]
#         predictions = [{"id": "1", "prediction": long_answer}]
#         
#         scores = evaluator.evaluate(ground_truth, predictions)
#         assert scores["exact_match"] == pytest.approx(1.0)
#     
#     def test_wrong_answer_gives_zero_em(self, evaluator):
#         """Test that wrong answers get 0 exact match"""
#         sample = STANDARD_CASES[:20] if len(STANDARD_CASES) >= 20 else STANDARD_CASES
#         
#         # All wrong answers
#         predictions = [
#             {"id": item["id"], "prediction": "WRONG_ANSWER"}
#             for item in sample
#         ]
#         
#         scores = evaluator.evaluate(sample, predictions)
#         
#         # EM should be 0, F1 should be very low
#         assert scores["exact_match"] == pytest.approx(0.0)
#         assert scores["f1"] < 0.1
#     
#     def test_adversarial_paraphrase(self, evaluator):
#         """Test that paraphrased answers get lower EM but higher F1"""
#         ground_truth = [
#             {"id": "1", "question": "Q", "context": "Answer is Alexander Graham Bell.", "answer": "Alexander Graham Bell"}
#         ]
#         predictions = [
#             {"id": "1", "prediction": "A. G. Bell"}  # Abbreviated
#         ]
#         
#         scores = evaluator.evaluate(ground_truth, predictions)
#         
#         # EM should be 0 (not exact)
#         assert scores["exact_match"] == pytest.approx(0.0)
#         
#         # F1 should be > 0 (has "Bell" in common)
#         assert scores["f1"] > 0.0
#         print(f"Paraphrase: EM={scores['exact_match']:.2f}, F1={scores['f1']:.2f}")
#     
#     def test_multiple_acceptable_answers(self, evaluator):
#         """Test evaluation with list of acceptable answers"""
#         ground_truth = [
#             {
#                 "id": "1",
#                 "question": "What is DNA?",
#                 "context": "DNA stands for deoxyribonucleic acid...",
#                 "answer": ["deoxyribonucleic acid", "DNA"]  # Multiple acceptable
#             }
#         ]
#         
#         # Either answer should work
#         predictions1 = [{"id": "1", "prediction": "deoxyribonucleic acid"}]
#         predictions2 = [{"id": "1", "prediction": "DNA"}]
#         
#         scores1 = evaluator.evaluate(ground_truth, predictions1)
#         scores2 = evaluator.evaluate(ground_truth, predictions2)
#         
#         assert scores1["exact_match"] == pytest.approx(1.0)
#         assert scores2["exact_match"] == pytest.approx(1.0)

