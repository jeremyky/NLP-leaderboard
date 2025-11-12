"""
Comprehensive metrics information and documentation

Provides detailed explanations for all evaluation metrics used in the leaderboard.
"""

METRICS_CATALOG = {
    # Classification Metrics
    "accuracy": {
        "name": "Accuracy",
        "formula": "Correct Predictions / Total Predictions",
        "range": "0.0 - 1.0 (higher is better)",
        "description": "Proportion of correct predictions across all classes. Simple and intuitive, but can be misleading for imbalanced datasets.",
        "example": "If a model correctly classifies 95 out of 100 examples, accuracy = 0.95",
        "when_to_use": "Use when classes are balanced and false positives/negatives have equal cost",
        "limitations": "Not suitable for imbalanced datasets. A model predicting only the majority class can have high accuracy.",
        "interpretation": {
            "0.9-1.0": "Excellent - Model is highly accurate",
            "0.7-0.9": "Good - Model performs well",
            "0.5-0.7": "Fair - Model has moderate performance",
            "0.0-0.5": "Poor - Model performs worse than random"
        }
    },
    
    "precision": {
        "name": "Precision (Macro-Averaged)",
        "formula": "True Positives / (True Positives + False Positives)",
        "range": "0.0 - 1.0 (higher is better)",
        "description": "Of all instances predicted as positive, what proportion were actually positive? Averaged across all classes.",
        "example": "If model predicts 100 as 'positive' and 85 are actually positive, precision = 0.85",
        "when_to_use": "Use when false positives are costly (e.g., spam detection, medical diagnosis)",
        "limitations": "Doesn't account for false negatives. High precision may come at cost of low recall.",
        "interpretation": {
            "0.9-1.0": "Excellent - Very few false positives",
            "0.7-0.9": "Good - Acceptable false positive rate",
            "0.5-0.7": "Fair - Significant false positives",
            "0.0-0.5": "Poor - Many false positives"
        }
    },
    
    "recall": {
        "name": "Recall (Macro-Averaged)",
        "formula": "True Positives / (True Positives + False Negatives)",
        "range": "0.0 - 1.0 (higher is better)",
        "description": "Of all actual positive instances, what proportion did we correctly identify? Averaged across all classes.",
        "example": "If there are 100 positive cases and model finds 90 of them, recall = 0.90",
        "when_to_use": "Use when false negatives are costly (e.g., fraud detection, disease screening)",
        "limitations": "Doesn't account for false positives. High recall may come at cost of low precision.",
        "interpretation": {
            "0.9-1.0": "Excellent - Catches nearly all positive cases",
            "0.7-0.9": "Good - Catches most positive cases",
            "0.5-0.7": "Fair - Misses many positive cases",
            "0.0-0.5": "Poor - Misses most positive cases"
        }
    },
    
    "f1": {
        "name": "F1 Score (Macro-Averaged)",
        "formula": "2 × (Precision × Recall) / (Precision + Recall)",
        "range": "0.0 - 1.0 (higher is better)",
        "description": "Harmonic mean of precision and recall. Balances both metrics and is useful for imbalanced datasets.",
        "example": "If precision=0.8 and recall=0.9, F1 = 2 × (0.8 × 0.9) / (0.8 + 0.9) = 0.847",
        "when_to_use": "Use when you need balance between precision and recall, especially for imbalanced data",
        "limitations": "Gives equal weight to precision and recall. May not be ideal if one is more important.",
        "interpretation": {
            "0.9-1.0": "Excellent - Strong balance of precision and recall",
            "0.7-0.9": "Good - Good balance",
            "0.5-0.7": "Fair - Moderate performance",
            "0.0-0.5": "Poor - Weak performance"
        }
    },
    
    # Q&A Metrics
    "exact_match": {
        "name": "Exact Match (EM)",
        "formula": "1 if prediction == answer else 0 (normalized)",
        "range": "0.0 - 1.0 (higher is better)",
        "description": "Percentage of predictions that exactly match the ground truth after normalization (lowercase, punctuation removal).",
        "example": "Question: 'Who wrote Hamlet?' Answer: 'Shakespeare' vs 'William Shakespeare' = no match",
        "when_to_use": "Use for factual questions where precision is critical",
        "limitations": "Very strict - doesn't give credit for partial correctness or synonyms",
        "interpretation": {
            "0.8-1.0": "Excellent - Model answers very precisely",
            "0.6-0.8": "Good - Model usually gets exact answer",
            "0.4-0.6": "Fair - Model often close but not exact",
            "0.0-0.4": "Poor - Model rarely matches exactly"
        }
    },
    
    "token_f1": {
        "name": "Token-level F1",
        "formula": "F1 computed on word overlap between prediction and answer",
        "range": "0.0 - 1.0 (higher is better)",
        "description": "Measures word-level overlap between prediction and ground truth. More lenient than Exact Match.",
        "example": "Answer: 'New York City', Prediction: 'New York' → F1 = 0.8 (2 of 3 words match)",
        "when_to_use": "Use when partial credit should be given for partially correct answers",
        "limitations": "Doesn't understand semantics - 'car' and 'automobile' get no credit",
        "interpretation": {
            "0.8-1.0": "Excellent - High word overlap with answers",
            "0.6-0.8": "Good - Decent word overlap",
            "0.4-0.6": "Fair - Moderate overlap",
            "0.0-0.4": "Poor - Little overlap with correct answers"
        }
    },
    
    # NER Metrics
    "ner_precision": {
        "name": "NER Precision",
        "formula": "Correct Entities / Predicted Entities",
        "range": "0.0 - 1.0 (higher is better)",
        "description": "Of all entities extracted, what proportion are correct? Entity must match both span (start/end) and type.",
        "example": "Model predicts 10 entities, 8 are correct → precision = 0.8",
        "when_to_use": "Use when false positive entities are problematic",
        "limitations": "Doesn't penalize missed entities. Very strict on boundaries.",
        "interpretation": {
            "0.9-1.0": "Excellent - Very few spurious entities",
            "0.7-0.9": "Good - Most predictions are valid entities",
            "0.5-0.7": "Fair - Many false positive entities",
            "0.0-0.5": "Poor - Most predictions are incorrect"
        }
    },
    
    "ner_recall": {
        "name": "NER Recall",
        "formula": "Correct Entities / True Entities",
        "range": "0.0 - 1.0 (higher is better)",
        "description": "Of all true entities in text, what proportion did we find? Both span and type must match.",
        "example": "Text has 10 entities, model finds 7 correctly → recall = 0.7",
        "when_to_use": "Use when missing entities is problematic",
        "limitations": "Doesn't penalize false positives. Requires exact span match.",
        "interpretation": {
            "0.9-1.0": "Excellent - Finds nearly all entities",
            "0.7-0.9": "Good - Finds most entities",
            "0.5-0.7": "Fair - Misses many entities",
            "0.0-0.5": "Poor - Misses most entities"
        }
    },
    
    "ner_f1": {
        "name": "NER F1 Score",
        "formula": "2 × (Precision × Recall) / (Precision + Recall)",
        "range": "0.0 - 1.0 (higher is better)",
        "description": "Harmonic mean of NER precision and recall. Standard metric for entity extraction.",
        "example": "NER precision=0.85, recall=0.80 → F1 = 0.824",
        "when_to_use": "Standard metric for comparing NER systems. Balances finding vs accuracy.",
        "limitations": "Requires exact span + type match. Doesn't give partial credit.",
        "interpretation": {
            "0.9-1.0": "Excellent - State-of-the-art performance",
            "0.8-0.9": "Good - Strong entity extraction",
            "0.6-0.8": "Fair - Moderate performance",
            "0.0-0.6": "Poor - Weak entity extraction"
        }
    },
    
    # Retrieval Metrics
    "retrieval_accuracy": {
        "name": "Retrieval Accuracy",
        "formula": "Queries with correct doc retrieved / Total queries",
        "range": "0.0 - 1.0 (higher is better)",
        "description": "Proportion of queries where at least one correct document was retrieved.",
        "example": "For 100 queries, 85 retrieve at least one correct document → accuracy = 0.85",
        "when_to_use": "Use for evaluating document retrieval or RAG systems",
        "limitations": "Binary - doesn't distinguish between retrieving 1 vs all correct docs",
        "interpretation": {
            "0.9-1.0": "Excellent - Retrieves correctly almost always",
            "0.7-0.9": "Good - Usually retrieves correct documents",
            "0.5-0.7": "Fair - Often fails to retrieve correctly",
            "0.0-0.5": "Poor - Rarely retrieves correct documents"
        }
    },
    
    "mrr": {
        "name": "Mean Reciprocal Rank (MRR)",
        "formula": "Average of 1/rank where rank = position of first correct result",
        "range": "0.0 - 1.0 (higher is better)",
        "description": "Measures how high the first correct result appears in rankings. Focuses on top results.",
        "example": "If correct doc is rank 1,3,2 for 3 queries: MRR = (1/1 + 1/3 + 1/2) / 3 = 0.61",
        "when_to_use": "Use when position of first correct result matters (e.g., search engines)",
        "limitations": "Only considers first correct result, ignores others",
        "interpretation": {
            "0.8-1.0": "Excellent - Correct result usually at top",
            "0.6-0.8": "Good - Correct result in top few",
            "0.4-0.6": "Fair - Correct result often buried",
            "0.0-0.4": "Poor - Correct result rarely near top"
        }
    },
    
    "ndcg": {
        "name": "Normalized Discounted Cumulative Gain",
        "formula": "DCG / Ideal DCG (where DCG = Σ relevance / log2(rank+1))",
        "range": "0.0 - 1.0 (higher is better)",
        "description": "Measures ranking quality with position-based discounting. Values top results more.",
        "example": "Perfect ranking gets 1.0, worse rankings get progressively lower scores",
        "when_to_use": "Use when multiple relevant docs exist and ranking matters",
        "limitations": "Requires relevance scores, not just binary labels",
        "interpretation": {
            "0.9-1.0": "Excellent - Near-perfect ranking",
            "0.7-0.9": "Good - Strong ranking quality",
            "0.5-0.7": "Fair - Moderate ranking quality",
            "0.0-0.5": "Poor - Poor ranking"
        }
    }
}


def get_metric_info(metric_name: str) -> dict:
    """Get information about a specific metric"""
    return METRICS_CATALOG.get(metric_name, {
        "name": metric_name.replace("_", " ").title(),
        "description": "Metric information not available",
        "range": "Unknown",
        "formula": "Unknown"
    })


def get_metrics_for_task(task_type: str) -> list:
    """Get all relevant metrics for a task type"""
    task_metrics = {
        "text_classification": ["accuracy", "precision", "recall", "f1"],
        "named_entity_recognition": ["ner_f1", "ner_precision", "ner_recall"],
        "document_qa": ["exact_match", "token_f1"],
        "line_qa": ["exact_match", "token_f1"],
        "retrieval": ["retrieval_accuracy", "mrr", "ndcg"]
    }
    return task_metrics.get(task_type, ["accuracy"])

