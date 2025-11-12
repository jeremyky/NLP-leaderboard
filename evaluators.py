"""
Evaluation metrics for different task types

Each evaluator computes metrics comparing predictions against ground truth.
Designed to prevent metric gaming by supporting diverse evaluation strategies.
"""
from typing import List, Dict, Any
from collections import Counter
import re


class BaseEvaluator:
    """Base class for all evaluators"""
    
    def evaluate(self, ground_truth: List[Dict], predictions: List[Dict]) -> Dict[str, float]:
        """
        Evaluate predictions against ground truth
        
        Args:
            ground_truth: List of ground truth examples
            predictions: List of predictions (must match ground truth IDs)
            
        Returns:
            Dictionary of metric names to scores
        """
        raise NotImplementedError


class TextClassificationEvaluator(BaseEvaluator):
    """Evaluator for text classification tasks"""
    
    def evaluate(self, ground_truth: List[Dict], predictions: List[Dict]) -> Dict[str, float]:
        # Create lookup for predictions
        pred_map = {p["id"]: p["prediction"] for p in predictions}
        
        correct = 0
        total = 0
        
        # Per-class metrics
        class_correct = Counter()
        class_total = Counter()
        class_pred_total = Counter()
        
        for gt in ground_truth:
            gt_id = gt["id"]
            true_label = gt["answer"]
            
            if gt_id not in pred_map:
                continue  # Skip missing predictions
            
            pred_label = pred_map[gt_id]
            total += 1
            class_total[true_label] += 1
            class_pred_total[pred_label] += 1
            
            if str(pred_label).strip().lower() == str(true_label).strip().lower():
                correct += 1
                class_correct[true_label] += 1
        
        if total == 0:
            return {"accuracy": 0.0, "precision": 0.0, "recall": 0.0, "f1": 0.0}
        
        accuracy = correct / total
        
        # Macro-averaged precision and recall
        precisions = []
        recalls = []
        
        all_classes = set(class_total.keys()) | set(class_pred_total.keys())
        for cls in all_classes:
            tp = class_correct.get(cls, 0)
            fp = class_pred_total.get(cls, 0) - tp
            fn = class_total.get(cls, 0) - tp
            
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            
            precisions.append(precision)
            recalls.append(recall)
        
        macro_precision = sum(precisions) / len(precisions) if precisions else 0
        macro_recall = sum(recalls) / len(recalls) if recalls else 0
        
        f1 = (2 * macro_precision * macro_recall / (macro_precision + macro_recall) 
              if (macro_precision + macro_recall) > 0 else 0)
        
        # Compute micro-averaged metrics as well
        total_tp = sum(class_correct.values())
        total_fp = sum(class_pred_total.values()) - total_tp
        total_fn = total - total_tp
        
        micro_precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0
        micro_recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0
        micro_f1 = (2 * micro_precision * micro_recall / (micro_precision + micro_recall)
                   if (micro_precision + micro_recall) > 0 else 0)
        
        return {
            "accuracy": round(accuracy, 4),
            "precision": round(macro_precision, 4),
            "recall": round(macro_recall, 4),
            "f1": round(f1, 4),
            "micro_precision": round(micro_precision, 4),
            "micro_recall": round(micro_recall, 4),
            "micro_f1": round(micro_f1, 4),
            "num_classes": len(all_classes),
            "total_predictions": total
        }


class NEREvaluator(BaseEvaluator):
    """Evaluator for Named Entity Recognition tasks"""
    
    def evaluate(self, ground_truth: List[Dict], predictions: List[Dict]) -> Dict[str, float]:
        pred_map = {p["id"]: p["prediction"] for p in predictions}
        
        total_tp = 0
        total_fp = 0
        total_fn = 0
        
        for gt in ground_truth:
            gt_id = gt["id"]
            true_entities = set(tuple(e) if isinstance(e, list) else e 
                               for e in gt.get("answer", []))
            
            if gt_id not in pred_map:
                total_fn += len(true_entities)
                continue
            
            pred_entities = set(tuple(e) if isinstance(e, list) else e 
                               for e in pred_map[gt_id])
            
            tp = len(true_entities & pred_entities)
            fp = len(pred_entities - true_entities)
            fn = len(true_entities - pred_entities)
            
            total_tp += tp
            total_fp += fp
            total_fn += fn
        
        precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0
        recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0
        
        return {
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
            "true_positives": total_tp,
            "false_positives": total_fp,
            "false_negatives": total_fn
        }


class QAEvaluator(BaseEvaluator):
    """Evaluator for Question Answering tasks (both document and line level)"""
    
    @staticmethod
    def normalize_answer(answer: str) -> str:
        """Normalize answer for comparison"""
        answer = answer.lower()
        answer = re.sub(r'\b(a|an|the)\b', ' ', answer)
        answer = re.sub(r'[^\w\s]', '', answer)
        answer = ' '.join(answer.split())
        return answer
    
    def compute_exact_match(self, prediction: str, ground_truth: str) -> float:
        """Exact match after normalization"""
        return float(self.normalize_answer(prediction) == self.normalize_answer(ground_truth))
    
    def compute_f1(self, prediction: str, ground_truth: str) -> float:
        """Token-level F1 score"""
        pred_tokens = self.normalize_answer(prediction).split()
        gt_tokens = self.normalize_answer(ground_truth).split()
        
        if not pred_tokens or not gt_tokens:
            return float(pred_tokens == gt_tokens)
        
        common = Counter(pred_tokens) & Counter(gt_tokens)
        num_same = sum(common.values())
        
        if num_same == 0:
            return 0.0
        
        precision = num_same / len(pred_tokens)
        recall = num_same / len(gt_tokens)
        f1 = (2 * precision * recall) / (precision + recall)
        
        return f1
    
    def evaluate(self, ground_truth: List[Dict], predictions: List[Dict]) -> Dict[str, float]:
        pred_map = {p["id"]: p["prediction"] for p in predictions}
        
        exact_matches = []
        f1_scores = []
        
        for gt in ground_truth:
            gt_id = gt["id"]
            true_answer = gt["answer"]
            
            if gt_id not in pred_map:
                exact_matches.append(0.0)
                f1_scores.append(0.0)
                continue
            
            pred_answer = pred_map[gt_id]
            
            # Handle multiple acceptable answers
            if isinstance(true_answer, list):
                em = max(self.compute_exact_match(pred_answer, ans) for ans in true_answer)
                f1 = max(self.compute_f1(pred_answer, ans) for ans in true_answer)
            else:
                em = self.compute_exact_match(pred_answer, true_answer)
                f1 = self.compute_f1(pred_answer, true_answer)
            
            exact_matches.append(em)
            f1_scores.append(f1)
        
        avg_em = sum(exact_matches) / len(exact_matches) if exact_matches else 0.0
        avg_f1 = sum(f1_scores) / len(f1_scores) if f1_scores else 0.0
        
        return {
            "exact_match": round(avg_em, 4),
            "f1": round(avg_f1, 4),
            "token_f1": round(avg_f1, 4),  # Alias for clarity
            "total_questions": len(exact_matches),
            "exact_matches_count": sum(exact_matches)
        }


class RetrievalEvaluator(BaseEvaluator):
    """Evaluator for retrieval/RAG tasks"""
    
    def evaluate(self, ground_truth: List[Dict], predictions: List[Dict]) -> Dict[str, float]:
        pred_map = {p["id"]: p["prediction"] for p in predictions}
        
        correct = 0
        total = 0
        
        for gt in ground_truth:
            gt_id = gt["id"]
            true_doc_ids = gt.get("answer", [])
            
            if not isinstance(true_doc_ids, list):
                true_doc_ids = [true_doc_ids]
            
            if gt_id not in pred_map:
                total += 1
                continue
            
            pred_doc_ids = pred_map[gt_id]
            if not isinstance(pred_doc_ids, list):
                pred_doc_ids = [pred_doc_ids]
            
            # Check if any predicted doc is in the ground truth
            if any(pred_id in true_doc_ids for pred_id in pred_doc_ids):
                correct += 1
            
            total += 1
        
        accuracy = correct / total if total > 0 else 0.0
        
        return {
            "retrieval_accuracy": round(accuracy, 4),
            "correct_retrievals": correct,
            "total_queries": total,
            "failed_retrievals": total - correct
        }


def get_evaluator(task_type: str) -> BaseEvaluator:
    """Factory function to get appropriate evaluator for task type"""
    evaluators = {
        "text_classification": TextClassificationEvaluator(),
        "named_entity_recognition": NEREvaluator(),
        "document_qa": QAEvaluator(),
        "line_qa": QAEvaluator(),
        "retrieval": RetrievalEvaluator(),
    }
    
    evaluator = evaluators.get(task_type)
    if not evaluator:
        raise ValueError(f"Unknown task type: {task_type}")
    
    return evaluator

