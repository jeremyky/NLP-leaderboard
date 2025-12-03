"""
Science & reasoning benchmarks from HuggingFace

These are small, curated samples suitable for seeding and demos.
"""

SCIENCE_DATASETS = [
    {
        "name": "Science QA - Multiple Choice",
        "description": "Basic science multiple-choice questions for reasoning over grade-school science.",
        "url": "https://huggingface.co/datasets/allenai/ai2_arc",
        "task_type": "text_classification",
        "test_set_public": False,
        "labels_public": False,
        "primary_metric": "accuracy",
        "additional_metrics": ["f1", "precision", "recall"],
        "ground_truth": [
            {
                "id": "1",
                "question": "What gas do plants absorb from the atmosphere for photosynthesis?",
                "answer": "carbon dioxide",
            },
            {
                "id": "2",
                "question": "Water changes from a liquid to a gas during which process?",
                "answer": "evaporation",
            },
            {
                "id": "3",
                "question": "Which force pulls objects toward the center of the Earth?",
                "answer": "gravity",
            },
            {
                "id": "4",
                "question": "What is the main source of energy for the Earth?",
                "answer": "the sun",
            },
        ],
        "baseline_models": [
            {"model": "GPT-4o", "score": 0.9, "version": "2024-11-01", "organization": "OpenAI"},
            {"model": "Claude 3.5 Sonnet", "score": 0.85, "version": "2024-10-22", "organization": "Anthropic"},
            {"model": "Llama 3.1 70B", "score": 0.8, "version": "instruct", "organization": "Meta"},
        ],
    },
    {
        "name": "Code Reasoning - Small Functions",
        "description": "Simple code generation / reasoning problems inspired by HumanEval-style tasks.",
        "url": "https://huggingface.co/datasets/openai/humaneval",
        "task_type": "document_qa",
        "test_set_public": False,
        "labels_public": False,
        "primary_metric": "exact_match",
        "additional_metrics": ["f1"],
        "ground_truth": [
            {
                "id": "1",
                "question": "Write a Python function that returns True if a number is even, otherwise False.",
                "context": "The function should be called is_even and take a single integer argument.",
                "answer": "def is_even(n):\n    return n % 2 == 0",
            },
            {
                "id": "2",
                "question": "Write a Python function that returns the factorial of a non-negative integer.",
                "context": "The function should be called factorial and use recursion.",
                "answer": "def factorial(n):\n    return 1 if n == 0 else n * factorial(n-1)",
            },
        ],
        "baseline_models": [
            {"model": "GPT-4o", "score": 0.75, "version": "2024-11-01", "organization": "OpenAI"},
            {"model": "CodeLlama", "score": 0.65, "version": "34B", "organization": "Meta"},
        ],
    },
]


def seed_science_datasets():
    """Load science / code benchmarks into the database."""
    from database import SessionLocal, init_db
    from models import Dataset, Submission, TaskType, SubmissionStatus
    from evaluators import get_evaluator
    from datetime import datetime
    import uuid

    init_db()
    db = SessionLocal()

    try:
        print("\n" + "=" * 60)
        print("🧪 SEEDING SCIENCE & CODE DATASETS")
        print("=" * 60 + "\n")

        for dataset_config in SCIENCE_DATASETS:
            # Check if exists
            existing = db.query(Dataset).filter(Dataset.name == dataset_config["name"]).first()
            if existing:
                print(f"⏭️  Skipping '{dataset_config['name']}' (already exists)")
                continue

            print(f"🔬 Creating dataset: {dataset_config['name']}")

            dataset_id = str(uuid.uuid4())
            dataset = Dataset(
                id=dataset_id,
                name=dataset_config["name"],
                description=dataset_config["description"],
                url=dataset_config["url"],
                task_type=TaskType(dataset_config["task_type"]),
                test_set_public=dataset_config["test_set_public"],
                labels_public=dataset_config["labels_public"],
                primary_metric=dataset_config["primary_metric"],
                additional_metrics=dataset_config["additional_metrics"],
                num_examples=len(dataset_config["ground_truth"]),
                ground_truth=dataset_config["ground_truth"],
            )
            db.add(dataset)
            db.flush()

            # Create baseline submissions using evaluator
            baseline_models = dataset_config.get("baseline_models", [])
            print(f"   Adding {len(baseline_models)} baseline models...")

            evaluator = get_evaluator(dataset_config["task_type"])

            from seed_data import create_baseline_predictions

            for baseline in baseline_models:
                submission_id = str(uuid.uuid4())
                predictions = create_baseline_predictions(
                    dataset_config["ground_truth"],
                    baseline["score"],
                )

                scores = evaluator.evaluate(dataset_config["ground_truth"], predictions)
                primary_score = scores.get(dataset_config["primary_metric"], baseline["score"])

                submission = Submission(
                    id=submission_id,
                    dataset_id=dataset_id,
                    model_name=baseline["model"],
                    model_version=baseline.get("version"),
                    organization=baseline.get("organization"),
                    predictions=predictions,
                    status=SubmissionStatus.COMPLETED,
                    primary_score=primary_score,
                    detailed_scores=scores,
                    confidence_interval=f"{primary_score-0.02:.2f} - {primary_score+0.02:.2f}",
                    is_internal=True,
                    created_at=datetime.now(),
                    evaluated_at=datetime.now(),
                )
                db.add(submission)
                print(f"      ✓ {baseline['model']}: {primary_score:.4f} (evaluated)")

            db.commit()
            print(f"   ✅ Dataset loaded successfully\n")

        print("=" * 60)
        print("✅ SCIENCE & CODE DATASETS LOADED!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_science_datasets()


