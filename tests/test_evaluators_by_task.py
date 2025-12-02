import os
import sys

import pytest

# Ensure project root is on sys.path
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from evaluators import (
    TextClassificationEvaluator,
    NEREvaluator,
    QAEvaluator,
    RetrievalEvaluator,
    get_evaluator,
)


def test_get_evaluator_returns_correct_types():
    assert isinstance(get_evaluator("text_classification"), TextClassificationEvaluator)
    assert isinstance(get_evaluator("named_entity_recognition"), NEREvaluator)
    assert isinstance(get_evaluator("document_qa"), QAEvaluator)
    assert isinstance(get_evaluator("line_qa"), QAEvaluator)
    assert isinstance(get_evaluator("retrieval"), RetrievalEvaluator)

    with pytest.raises(ValueError):
        get_evaluator("unknown_task_type")


def test_text_classification_evaluator_binary_perfect_and_partial():
    evaluator = TextClassificationEvaluator()

    ground_truth = [
        {"id": "1", "question": "a", "answer": "positive"},
        {"id": "2", "question": "b", "answer": "positive"},
        {"id": "3", "question": "c", "answer": "negative"},
        {"id": "4", "question": "d", "answer": "negative"},
    ]

    # All correct predictions
    perfect_preds = [
        {"id": "1", "prediction": "positive"},
        {"id": "2", "prediction": "positive"},
        {"id": "3", "prediction": "negative"},
        {"id": "4", "prediction": "negative"},
    ]

    # Half correct predictions
    partial_preds = [
        {"id": "1", "prediction": "positive"},
        {"id": "2", "prediction": "negative"},
        {"id": "3", "prediction": "negative"},
        {"id": "4", "prediction": "positive"},
    ]

    perfect_scores = evaluator.evaluate(ground_truth, perfect_preds)
    partial_scores = evaluator.evaluate(ground_truth, partial_preds)

    # Basic sanity checks
    assert perfect_scores["accuracy"] == pytest.approx(1.0)
    assert perfect_scores["f1"] == pytest.approx(1.0)
    assert perfect_scores["micro_f1"] == pytest.approx(1.0)
    assert perfect_scores["balanced_accuracy"] == pytest.approx(1.0)
    assert perfect_scores["num_classes"] == 2
    assert perfect_scores["total_predictions"] == 4
    # MCC is only defined/used for certain configurations; just ensure it is present
    # and between -1 and 1 if provided.
    if "matthews_corr" in perfect_scores:
        assert -1.0 <= perfect_scores["matthews_corr"] <= 1.0

    # Partial case should be strictly worse than perfect
    assert 0.0 < partial_scores["accuracy"] < 1.0
    assert 0.0 < partial_scores["f1"] < 1.0
    assert partial_scores["accuracy"] < perfect_scores["accuracy"]


def test_ner_evaluator_exact_and_partial_matches():
    evaluator = NEREvaluator()

    # Ground truth entities stored as tuples; JSON would store them as lists,
    # but the evaluator handles both representations.
    ground_truth = [
        {
            "id": "1",
            "text": "Apple Inc. reported revenue of $125.3B",
            "answer": [("Apple Inc.", "ORG"), ("$125.3B", "MONEY")],
        },
        {
            "id": "2",
            "text": "Microsoft acquired GitHub for $7.5B",
            "answer": [("Microsoft", "ORG"), ("GitHub", "ORG"), ("$7.5B", "MONEY")],
        },
    ]

    # Exact matches
    exact_preds = [
        {"id": "1", "prediction": [("Apple Inc.", "ORG"), ("$125.3B", "MONEY")]},
        {
            "id": "2",
            "prediction": [("Microsoft", "ORG"), ("GitHub", "ORG"), ("$7.5B", "MONEY")],
        },
    ]

    # Partial entity boundary matches (text overlaps but not identical)
    partial_preds = [
        {"id": "1", "prediction": [("Apple", "ORG"), ("$125.3B", "MONEY")]},
        {"id": "2", "prediction": [("Microsoft", "ORG"), ("GitHub", "ORG")]},
    ]

    exact_scores = evaluator.evaluate(ground_truth, exact_preds)
    partial_scores = evaluator.evaluate(ground_truth, partial_preds)

    # Exact predictions should yield perfect strict metrics
    assert exact_scores["f1"] == pytest.approx(1.0)
    assert exact_scores["precision"] == pytest.approx(1.0)
    assert exact_scores["recall"] == pytest.approx(1.0)

    # Partial predictions are worse on strict metrics
    assert 0.0 < partial_scores["f1"] < 1.0

    # But partial_* metrics should give credit for overlapping entity spans
    assert partial_scores["partial_f1"] >= partial_scores["f1"]
    assert partial_scores["partial_precision"] >= partial_scores["precision"]
    assert partial_scores["partial_recall"] >= partial_scores["recall"]


def test_qa_evaluator_exact_match_and_f1_multiple_answers():
    evaluator = QAEvaluator()

    ground_truth = [
        {"id": "1", "question": "Capital of France?", "answer": "Paris"},
        {
            "id": "2",
            "question": "What is H2O?",
            "answer": ["water", "H2O"],
        },
    ]

    preds_perfect = [
        {"id": "1", "prediction": "Paris"},
        {"id": "2", "prediction": "water"},
    ]

    preds_imperfect = [
        {"id": "1", "prediction": "the city of Paris"},
        {"id": "2", "prediction": "liquid"},
    ]

    perfect_scores = evaluator.evaluate(ground_truth, preds_perfect)
    imperfect_scores = evaluator.evaluate(ground_truth, preds_imperfect)

    # Perfect predictions: EM and F1 should be high (1.0 here)
    assert perfect_scores["exact_match"] == pytest.approx(1.0)
    assert perfect_scores["f1"] == pytest.approx(1.0)

    # Imperfect predictions: EM/F1 should be lower
    assert 0.0 <= imperfect_scores["exact_match"] < 1.0
    assert 0.0 <= imperfect_scores["f1"] < 1.0

    # BLEU-style score should correlate with token overlap
    assert imperfect_scores["bleu"] <= perfect_scores["bleu"]


def test_retrieval_evaluator_basic_metrics():
    evaluator = RetrievalEvaluator()

    ground_truth = [
        {"id": "1", "question": "q1", "answer": ["d1"]},
        {"id": "2", "question": "q2", "answer": ["d2"]},
        {"id": "3", "question": "q3", "answer": ["d3"]},
    ]

    # Predictions where the correct doc is always at rank 1
    preds_perfect = [
        {"id": "1", "prediction": ["d1", "dX"]},
        {"id": "2", "prediction": ["d2", "dY"]},
        {"id": "3", "prediction": ["d3", "dZ"]},
    ]

    # Predictions where the correct doc is present but not always at rank 1
    preds_mixed = [
        {"id": "1", "prediction": ["dX", "d1"]},  # correct at rank 2
        {"id": "2", "prediction": ["d2", "dY"]},  # correct at rank 1
        {"id": "3", "prediction": ["dZ", "d3"]},  # correct at rank 2
    ]

    perfect_scores = evaluator.evaluate(ground_truth, preds_perfect)
    mixed_scores = evaluator.evaluate(ground_truth, preds_mixed)

    # Perfect predictions: accuracy and MRR should both be 1.0
    assert perfect_scores["retrieval_accuracy"] == pytest.approx(1.0)
    assert perfect_scores["mrr"] == pytest.approx(1.0)
    assert perfect_scores["precision_at_1"] == pytest.approx(1.0)
    assert perfect_scores["recall_at_1"] == pytest.approx(1.0)

    # Mixed case: accuracy still 1.0 (all have at least one correct doc),
    # but MRR and precision@1 should be lower.
    assert mixed_scores["retrieval_accuracy"] == pytest.approx(1.0)
    assert 0.0 < mixed_scores["mrr"] < 1.0
    assert 0.0 < mixed_scores["precision_at_1"] < 1.0


