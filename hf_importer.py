"""
HuggingFace Dataset Importer

Import datasets directly from HuggingFace Hub and convert them to our format.
"""
from typing import Dict, List, Optional
import requests
import json

from datasets import load_dataset


class HuggingFaceImporter:
    """Import datasets from HuggingFace Hub"""
    
    # Mapping of HF dataset names to our task types
    DATASET_TASK_MAPPING = {
        "ag_news": "text_classification",
        "sst2": "text_classification",
        "imdb": "text_classification",
        "squad": "document_qa",
        "squad_v2": "document_qa",
        "conll2003": "named_entity_recognition",
        "wikitext": "document_qa",
        "truthful_qa": "document_qa",
        "financial_phrasebank": "text_classification",
    }
    
    DATASET_METRICS = {
        "text_classification": {"primary": "accuracy", "additional": ["f1", "precision", "recall"]},
        "named_entity_recognition": {"primary": "f1", "additional": ["precision", "recall"]},
        "document_qa": {"primary": "exact_match", "additional": ["f1"]},
        "line_qa": {"primary": "exact_match", "additional": ["f1"]},
        "retrieval": {"primary": "retrieval_accuracy", "additional": []},
    }
    
    @staticmethod
    def get_dataset_info(dataset_name: str) -> Optional[Dict]:
        """
        Fetch dataset information from HuggingFace Hub
        
        Args:
            dataset_name: HuggingFace dataset identifier (e.g., "ag_news")
            
        Returns:
            Dictionary with dataset metadata
        """
        try:
            url = f"https://datasets-server.huggingface.co/info?dataset={dataset_name}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to fetch dataset info: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error fetching dataset info: {e}")
            return None
    
    @staticmethod
    def sample_dataset(
        dataset_name: str,
        config: str = "default",
        split: str = "test",
        num_samples: int = 100,
    ) -> Optional[List[Dict]]:
        """
        Get sample rows from a HuggingFace dataset using the `datasets` library.

        This avoids relying on the older `datasets-server` HTTP API (which can
        return 4xx/5xx for some configurations) and instead works the same way
        users typically load datasets locally.
        
        Args:
            dataset_name: HuggingFace dataset identifier (e.g. "ag_news").
            config: Dataset configuration/subset.
            split: Dataset split (train/validation/test).
            num_samples: Number of samples to fetch (capped by split size).
            
        Returns:
            List of rows in the same shape as the former HTTP-based helper
            returned, i.e. each element is a dict with a single `"row"` key.
        """
        try:
            ds = load_dataset(dataset_name, config, split=split)
        except Exception as e:
            print(f"Error loading dataset '{dataset_name}' (config={config}, split={split}): {e}")
            return None

        try:
            n = min(num_samples, len(ds))
            subset = ds.select(range(n))
            # Match the shape expected by `convert_to_leaderboard_format`, which
            # previously read from the datasets-server `"rows"` field.
            return [{"row": dict(row)} for row in subset]
        except Exception as e:
            print(f"Error sampling rows from dataset '{dataset_name}': {e}")
            return None
    
    @classmethod
    def convert_to_leaderboard_format(cls, dataset_name: str, rows: List[Dict], task_type: str = None) -> Dict:
        """
        Convert HuggingFace dataset rows to our leaderboard format
        
        Args:
            dataset_name: Name of the dataset
            rows: Raw rows from HF dataset
            task_type: Task type (auto-detected if None)
            
        Returns:
            Dataset in leaderboard format
        """
        if task_type is None:
            task_type = cls.DATASET_TASK_MAPPING.get(dataset_name, "text_classification")
        
        metrics = cls.DATASET_METRICS.get(task_type, {"primary": "accuracy", "additional": []})
        
        # Convert rows to ground truth format
        ground_truth = []
        
        for i, row in enumerate(rows):
            row_data = row.get("row", {})
            
            # Try to extract question and answer based on common field names
            question = (
                row_data.get("text") or 
                row_data.get("sentence") or 
                row_data.get("question") or
                row_data.get("context") or
                str(row_data)
            )
            
            answer = (
                row_data.get("label") or
                row_data.get("answer") or
                row_data.get("label_text") or
                row_data.get("answers", {}).get("text", [""])[0] if isinstance(row_data.get("answers"), dict) else None
            )
            
            # Convert numeric labels to text if possible
            if isinstance(answer, int) and "label" in row_data:
                # Try to find label names
                label_names = row_data.get("label_text") or dataset_name
                answer = str(answer)
            
            ground_truth.append({
                "id": str(i + 1),
                "question": str(question)[:500],  # Truncate long questions
                "answer": str(answer) if answer is not None else "unknown"
            })
        
        return {
            "name": f"{dataset_name.replace('_', ' ').title()} (HuggingFace)",
            "description": f"Imported from HuggingFace dataset: {dataset_name}",
            "url": f"https://huggingface.co/datasets/{dataset_name}",
            "task_type": task_type,
            "test_set_public": False,
            "labels_public": False,
            "primary_metric": metrics["primary"],
            "additional_metrics": metrics["additional"],
            "ground_truth": ground_truth
        }
    
    @classmethod
    def import_dataset(cls, dataset_name: str, config: str = "default", split: str = "test", num_samples: int = 100) -> Optional[Dict]:
        """
        Import a dataset from HuggingFace
        
        Args:
            dataset_name: HuggingFace dataset identifier
            config: Dataset configuration
            split: Dataset split
            num_samples: Number of samples to import
            
        Returns:
            Dataset in leaderboard format
        """
        print(f"📥 Importing {dataset_name} from HuggingFace...")
        
        # Fetch dataset info
        info = cls.get_dataset_info(dataset_name)
        if info:
            print(f"   Found dataset: {info.get('dataset_info', {}).get('description', 'No description')[:100]}")
        
        # Sample dataset rows
        rows = cls.sample_dataset(dataset_name, config, split, num_samples)
        
        if not rows:
            print(f"   ❌ Failed to fetch dataset samples")
            return None
        
        print(f"   ✓ Fetched {len(rows)} samples")
        
        # Convert to our format
        dataset = cls.convert_to_leaderboard_format(dataset_name, rows)
        print(f"   ✓ Converted to {dataset['task_type']} format")
        
        return dataset


def test_importer():
    """Test the HuggingFace importer"""
    importer = HuggingFaceImporter()
    
    test_datasets = ["ag_news", "sst2", "imdb"]
    
    for dataset_name in test_datasets:
        print(f"\n{'='*60}")
        result = importer.import_dataset(dataset_name, num_samples=10)
        
        if result:
            print(f"✅ Successfully imported {dataset_name}")
            print(f"   Task: {result['task_type']}")
            print(f"   Samples: {len(result['ground_truth'])}")
            print(f"   First sample: {result['ground_truth'][0]}")
        else:
            print(f"❌ Failed to import {dataset_name}")


if __name__ == "__main__":
    test_importer()

