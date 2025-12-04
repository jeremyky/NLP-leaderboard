"""
Bulk-import benchmarks from HuggingFace using `hf_datasets_proposals.json`.

This script reads the JSON proposals file (auto-generated from a ChatGPT prompt),
uses the existing `HuggingFaceImporter` to fetch samples, converts them into
our internal leaderboard format, and then writes them into the database as
`Dataset` rows.

Unlike the small hand-crafted seeds in `seed_data.py` and the domain-specific
seeders, these imports can be much larger (hundreds or thousands of examples)
and are meant to provide more realistic, statistically stable benchmarks.

Usage (from project root):

    python hf_seed_from_proposals.py

You can optionally limit how many proposals to import via the `MAX_DATASETS`
constant below.
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

from database import SessionLocal, init_db
from models import Dataset, TaskType
from hf_importer import HuggingFaceImporter


# Path to the proposals JSON (relative to this file)
HF_PROPOSALS_PATH = Path(__file__).with_name("hf_datasets_proposals.json")

# Safety valve so we don't accidentally import hundreds of datasets on first run.
# Set to None to import all proposals.
MAX_DATASETS: Optional[int] = None


def load_proposals(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"HF proposals file not found at: {path}")
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("hf_datasets_proposals.json must contain a JSON list")
    return data


def build_dataset_from_proposal(
    proposal: Dict[str, Any],
    rows: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Use HuggingFaceImporter to convert rows, then override with proposal metadata.
    """
    hf_name: str = proposal["hf_dataset"]
    task_type: str = proposal["task_type"]

    # Convert using our standard logic but force task_type so metrics catalog aligns.
    dataset = HuggingFaceImporter.convert_to_leaderboard_format(
        dataset_name=hf_name,
        rows=rows,
        task_type=task_type,
    )

    # Override / enrich with proposal fields
    dataset["name"] = proposal.get("name", dataset["name"])
    dataset["url"] = f"https://huggingface.co/datasets/{hf_name}"
    dataset["task_type"] = task_type

    # Respect proposal's metric choices when provided
    dataset["primary_metric"] = proposal.get(
        "primary_metric",
        dataset.get("primary_metric", "accuracy"),
    )
    dataset["additional_metrics"] = proposal.get(
        "additional_metrics",
        dataset.get("additional_metrics", []),
    )

    return dataset


def seed_hf_from_proposals(max_datasets: Optional[int] = MAX_DATASETS) -> None:
    """
    Read `hf_datasets_proposals.json` and import each dataset into the DB.
    """
    init_db()
    db = SessionLocal()

    try:
        proposals = load_proposals(HF_PROPOSALS_PATH)
        if max_datasets is not None:
            proposals = proposals[:max_datasets]

        print("\n" + "=" * 60)
        print("📥 SEEDING HUGGINGFACE DATASETS FROM PROPOSALS")
        print("=" * 60 + "\n")

        for idx, proposal in enumerate(proposals, start=1):
            hf_name = proposal["hf_dataset"]
            config = proposal.get("config", "default")
            split = proposal.get("split", "test")
            num_samples = proposal.get("suggested_num_samples", 100)
            display_name = proposal.get("name", hf_name)

            print(f"[{idx}/{len(proposals)}] 📊 Importing '{display_name}'")
            print(f"    HF dataset: {hf_name} | config={config} | split={split} | n={num_samples}")

            # Skip if dataset with this display name already exists
            existing = db.query(Dataset).filter(Dataset.name == display_name).first()
            if existing:
                print(f"    ⏭️  Skipping (dataset with name '{display_name}' already exists)")
                continue

            # Fetch rows from HF
            rows = HuggingFaceImporter.sample_dataset(
                dataset_name=hf_name,
                config=config,
                split=split,
                num_samples=num_samples,
            )
            if not rows:
                print("    ❌ Failed to fetch rows from HuggingFace; skipping.\n")
                continue

            print(f"    ✓ Retrieved {len(rows)} sample rows")

            # Build leaderboard-style dataset dict
            dataset_data = build_dataset_from_proposal(proposal, rows)

            # Create DB object
            try:
                dataset_id = str(uuid.uuid4())
                db_dataset = Dataset(
                    id=dataset_id,
                    name=dataset_data["name"],
                    description=dataset_data.get("description") or dataset_data["name"],
                    url=dataset_data["url"],
                    task_type=TaskType(dataset_data["task_type"]),
                    test_set_public=dataset_data.get("test_set_public", False),
                    labels_public=dataset_data.get("labels_public", False),
                    primary_metric=dataset_data["primary_metric"],
                    additional_metrics=dataset_data.get("additional_metrics", []),
                    num_examples=len(dataset_data["ground_truth"]),
                    ground_truth=dataset_data["ground_truth"],
                )
                db.add(db_dataset)
                db.commit()

                print(
                    f"    ✅ Imported as '{dataset_data['name']}' "
                    f"({len(dataset_data['ground_truth'])} examples, task={dataset_data['task_type']})\n"
                )
            except Exception as e:
                db.rollback()
                print(f"    ❌ Error importing '{display_name}': {e}\n")

        print("=" * 60)
        print("✅ COMPLETED HUGGINGFACE PROPOSAL IMPORT")
        print("=" * 60 + "\n")

    finally:
        db.close()


if __name__ == "__main__":
    seed_hf_from_proposals()


