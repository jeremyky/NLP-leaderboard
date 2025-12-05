"""
Evaluation metrics for different task types

Each evaluator computes metrics comparing predictions against ground truth.
Designed to prevent metric gaming by supporting diverse evaluation strategies.
"""
from typing import List, Dict, Any
from collections import Counter
import re
import numpy as np


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
        
        # Balanced Accuracy - accounts for class imbalance
        recalls_per_class = []
        for cls in all_classes:
            tp = class_correct.get(cls, 0)
            fn = class_total.get(cls, 0) - tp
            cls_recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            recalls_per_class.append(cls_recall)
        balanced_accuracy = sum(recalls_per_class) / len(recalls_per_class) if recalls_per_class else 0
        
        # Matthews Correlation Coefficient (MCC)
        # For binary classification, this is more informative than accuracy
        if len(all_classes) == 2:
            tp = total_tp
            tn = total - total_tp - total_fp - total_fn  # True negatives
            fp = total_fp
            fn = total_fn
            
            mcc_numerator = (tp * tn) - (fp * fn)
            mcc_denominator = np.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
            mcc = mcc_numerator / mcc_denominator if mcc_denominator > 0 else 0
        else:
            mcc = None
        
        # Cohen's Kappa - agreement beyond chance
        p_observed = accuracy
        # Expected accuracy if predictions were random but matched class distribution
        p_expected = sum((class_total[cls] / total) * (class_pred_total.get(cls, 0) / total) 
                        for cls in all_classes if total > 0) if total > 0 else 0
        kappa = (p_observed - p_expected) / (1 - p_expected) if (1 - p_expected) > 0 else 0
        
        result = {
            "accuracy": round(accuracy, 4),
            "precision": round(macro_precision, 4),
            "recall": round(macro_recall, 4),
            "f1": round(f1, 4),
            "micro_precision": round(micro_precision, 4),
            "micro_recall": round(micro_recall, 4),
            "micro_f1": round(micro_f1, 4),
            "balanced_accuracy": round(balanced_accuracy, 4),
            "cohens_kappa": round(kappa, 4),
            "num_classes": len(all_classes),
            "total_predictions": total
        }
        
        if mcc is not None:
            result["matthews_corr"] = round(mcc, 4)
        
        return result


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
        
        # Compute partial match scores (relaxed boundaries)
        # Consider an entity correct if its text overlaps with a ground truth entity,
        # even if boundaries don't match exactly. This logic must work for both
        # in-memory tuples and JSON-serialized lists.
        partial_tp = 0
        for gt in ground_truth:
            gt_id = gt["id"]
            true_entities = gt.get("answer", [])
            
            if gt_id not in pred_map:
                continue
            
            pred_entities = pred_map[gt_id]
            if not isinstance(pred_entities, list):
                pred_entities = [pred_entities]
            if not isinstance(true_entities, list):
                true_entities = [true_entities]
            
            # For simplicity, count overlapping entities by comparing their surface text
            for pred_ent in pred_entities:
                # Handle both tuple and list representations from JSON
                if isinstance(pred_ent, (list, tuple)) and len(pred_ent) >= 1:
                    pred_text = str(pred_ent[0]).lower()
                else:
                    pred_text = str(pred_ent).lower()
                
                for true_ent in true_entities:
                    if isinstance(true_ent, (list, tuple)) and len(true_ent) >= 1:
                        true_text = str(true_ent[0]).lower()
                    else:
                        true_text = str(true_ent).lower()
                    
                    # Simple overlap check on surface forms
                    if pred_text and true_text and (
                        pred_text in true_text or true_text in pred_text
                    ):
                                partial_tp += 1
                                break
        
        partial_precision = partial_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0
        partial_recall = partial_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0
        partial_f1 = (2 * partial_precision * partial_recall / (partial_precision + partial_recall)) if (partial_precision + partial_recall) > 0 else 0
        
        return {
            "f1": round(f1, 4),
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "partial_f1": round(partial_f1, 4),
            "partial_precision": round(partial_precision, 4),
            "partial_recall": round(partial_recall, 4),
            "true_positives": total_tp,
            "false_positives": total_fp,
            "false_negatives": total_fn
        }


class QAEvaluator(BaseEvaluator):
    """Evaluator for Question Answering tasks (both document and line level)"""
    
    @staticmethod
    def normalize_answer(answer: str) -> str:
        """Normalize answer for comparison.

        This is intentionally defensive because some seeders and user
        submissions may provide:
          - a single string answer
          - a list of possible answers
          - other JSON-serialised structures

        We coerce lists to their first element and everything else to str
        before applying text normalization.
        """
        # If we received a list (e.g. multiple-choice answers), pick first.
        if isinstance(answer, list):
            answer = answer[0] if answer else ""

        # Coerce non-string values to string representation
        if not isinstance(answer, str):
            answer = str(answer)

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
        
        # Compute BLEU-style score (n-gram overlap)
        bleu_scores = []
        for gt in ground_truth:
            gt_id = gt["id"]
            true_answer = gt["answer"]
            
            if gt_id not in pred_map:
                bleu_scores.append(0.0)
                continue
            
            pred_answer = pred_map[gt_id]
            
            # Simple unigram BLEU
            pred_tokens = self.normalize_answer(pred_answer).split()
            gt_tokens = self.normalize_answer(true_answer if not isinstance(true_answer, list) else true_answer[0]).split()
            
            if not pred_tokens or not gt_tokens:
                bleu_scores.append(0.0)
                continue
            
            # Count matching unigrams
            matches = len(set(pred_tokens) & set(gt_tokens))
            bleu = matches / len(pred_tokens) if pred_tokens else 0
            bleu_scores.append(bleu)
        
        avg_bleu = sum(bleu_scores) / len(bleu_scores) if bleu_scores else 0.0
        
        # Answer length ratio (checks if answers are too long/short)
        length_ratios = []
        for gt in ground_truth:
            gt_id = gt["id"]
            true_answer = gt["answer"]
            if isinstance(true_answer, list):
                true_answer = true_answer[0]
            
            if gt_id not in pred_map:
                continue
            
            pred_answer = pred_map[gt_id]

            # Normalise both prediction and ground truth into simple strings
            # before measuring length. This mirrors `normalize_answer`'s
            # handling of list / non-string values but keeps original casing.
            if isinstance(pred_answer, list):
                pred_answer = pred_answer[0] if pred_answer else ""
            if not isinstance(pred_answer, str):
                pred_answer = str(pred_answer)

            if isinstance(true_answer, list):
                true_answer = true_answer[0] if true_answer else ""
            if not isinstance(true_answer, str):
                true_answer = str(true_answer)

            pred_len = len(pred_answer.split())
            true_len = len(true_answer.split())
            
            if true_len > 0:
                ratio = pred_len / true_len
                length_ratios.append(ratio)
        
        avg_length_ratio = sum(length_ratios) / len(length_ratios) if length_ratios else 1.0
        
        return {
            "exact_match": round(avg_em, 4),
            "f1": round(avg_f1, 4),
            "token_f1": round(avg_f1, 4),  # Alias for clarity
            "bleu": round(avg_bleu, 4),
            "answer_length_ratio": round(avg_length_ratio, 4),
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
        
        # Mean Reciprocal Rank (MRR) - measures rank of first correct result
        reciprocal_ranks = []
        for gt in ground_truth:
            gt_id = gt["id"]
            true_doc_ids = gt.get("answer", [])
            
            if not isinstance(true_doc_ids, list):
                true_doc_ids = [true_doc_ids]
            
            if gt_id not in pred_map:
                reciprocal_ranks.append(0.0)
                continue
            
            pred_doc_ids = pred_map[gt_id]
            if not isinstance(pred_doc_ids, list):
                pred_doc_ids = [pred_doc_ids]
            
            # Find rank of first correct document
            for rank, pred_id in enumerate(pred_doc_ids, start=1):
                if pred_id in true_doc_ids:
                    reciprocal_ranks.append(1.0 / rank)
                    break
            else:
                reciprocal_ranks.append(0.0)
        
        mrr = sum(reciprocal_ranks) / len(reciprocal_ranks) if reciprocal_ranks else 0.0
        
        # Precision@K and Recall@K (K=1, 3, 5)
        def precision_at_k(k):
            prec_scores = []
            for gt in ground_truth:
                gt_id = gt["id"]
                true_doc_ids = set(gt.get("answer", []) if isinstance(gt.get("answer", []), list) else [gt.get("answer")])
                
                if gt_id not in pred_map:
                    prec_scores.append(0.0)
                    continue
                
                pred_doc_ids = pred_map[gt_id]
                if not isinstance(pred_doc_ids, list):
                    pred_doc_ids = [pred_doc_ids]
                
                top_k = pred_doc_ids[:k]
                relevant_in_k = sum(1 for doc in top_k if doc in true_doc_ids)
                prec_scores.append(relevant_in_k / k if k > 0 else 0)
            
            return sum(prec_scores) / len(prec_scores) if prec_scores else 0.0
        
        def recall_at_k(k):
            rec_scores = []
            for gt in ground_truth:
                gt_id = gt["id"]
                true_doc_ids = set(gt.get("answer", []) if isinstance(gt.get("answer", []), list) else [gt.get("answer")])
                
                if gt_id not in pred_map:
                    rec_scores.append(0.0)
                    continue
                
                pred_doc_ids = pred_map[gt_id]
                if not isinstance(pred_doc_ids, list):
                    pred_doc_ids = [pred_doc_ids]
                
                top_k = pred_doc_ids[:k]
                relevant_in_k = sum(1 for doc in top_k if doc in true_doc_ids)
                rec_scores.append(relevant_in_k / len(true_doc_ids) if len(true_doc_ids) > 0 else 0)
            
            return sum(rec_scores) / len(rec_scores) if rec_scores else 0.0
        
        return {
            "retrieval_accuracy": round(accuracy, 4),
            "mrr": round(mrr, 4),
            "precision_at_1": round(precision_at_k(1), 4),
            "precision_at_3": round(precision_at_k(3), 4),
            "precision_at_5": round(precision_at_k(5), 4),
            "recall_at_1": round(recall_at_k(1), 4),
            "recall_at_3": round(recall_at_k(3), 4),
            "recall_at_5": round(recall_at_k(5), 4),
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

