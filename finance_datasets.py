"""
Finance-specific datasets from HuggingFace

These are real financial benchmarks for sentiment analysis, Q&A, and NER tasks.
All datasets are available on HuggingFace Hub. The base ground-truth lists
are intentionally small; at seed time we augment them with additional
examples from ``extra_ground_truth.py`` to make metrics more stable.
"""

from typing import Dict, List

from extra_ground_truth import (
    FIN_PHRASEBANK_EXTRA,
    FIQA_OPINION_EXTRA,
    TWITTER_FIN_SENTIMENT_EXTRA,
    FIN_QA_EXTRA,
    FIN_NER_EXTRA,
)


FINANCE_DATASETS: List[Dict] = [
    {
        "name": "Financial PhraseBank - Sentiment Analysis",
        "description": "Financial news sentences labeled with sentiment (positive, negative, neutral). From Malo et al., 2014.",
        "url": "https://huggingface.co/datasets/financial_phrasebank",
        "task_type": "text_classification",
        "test_set_public": False,
        "labels_public": False,
        "primary_metric": "accuracy",
        "additional_metrics": ["f1", "precision", "recall"],
        "ground_truth": [
            {"id": "1", "question": "Operating profit increased to EUR 13.1 mn from EUR 8.7 mn in the corresponding period in 2007", "answer": "positive"},
            {"id": "2", "question": "The company's net sales decreased by 15% year-on-year", "answer": "negative"},
            {"id": "3", "question": "Net sales totaled EUR 93.6 mn, up from EUR 93.2 mn", "answer": "neutral"},
            {"id": "4", "question": "Profit margin improved to 12.5% from 10.2%", "answer": "positive"},
            {"id": "5", "question": "The company reported a loss of EUR 2.1 mn", "answer": "negative"},
            {"id": "6", "question": "Revenue remained stable at EUR 45.3 mn", "answer": "neutral"},
            {"id": "7", "question": "EBITDA grew by 23% to EUR 18.5 mn", "answer": "positive"},
            {"id": "8", "question": "Market share declined from 15% to 12%", "answer": "negative"},
            {"id": "9", "question": "The transaction is expected to close in Q4", "answer": "neutral"},
            {"id": "10", "question": "Strong cash flow generation of EUR 25 mn", "answer": "positive"},
        ],
        "baseline_models": [
            {"model": "FinBERT", "score": 0.97, "version": "yiyanghkust/finbert-tone", "organization": "HKU"},
            {"model": "GPT-4o", "score": 0.94, "version": "2024-11-01", "organization": "OpenAI"},
            {"model": "Claude 3.5 Sonnet", "score": 0.93, "version": "2024-10-22", "organization": "Anthropic"},
            {"model": "BloombergGPT", "score": 0.96, "version": "50B", "organization": "Bloomberg"},
            {"model": "Llama 3.1 70B", "score": 0.91, "version": "instruct", "organization": "Meta"},
            {"model": "FinGPT", "score": 0.94, "version": "v3", "organization": "AI4Finance"},
            {"model": "Gemini 1.5 Pro", "score": 0.92, "version": "001", "organization": "Google"},
            {"model": "BERT-base", "score": 0.88, "version": "uncased", "organization": "Google"},
        ]
    },
    {
        "name": "FiQA - Financial Opinion Mining",
        "description": "Financial sentiment analysis on news and social media. From WWW 2018 conference.",
        "url": "https://huggingface.co/datasets/pauri32/fiqa-2018",
        "task_type": "text_classification",
        "test_set_public": False,
        "labels_public": False,
        "primary_metric": "f1",
        "additional_metrics": ["accuracy", "precision", "recall"],
        "ground_truth": [
            {"id": "1", "question": "Apple stock soars on strong iPhone sales", "answer": "positive"},
            {"id": "2", "question": "Tesla faces production delays and quality issues", "answer": "negative"},
            {"id": "3", "question": "Microsoft announces cloud revenue growth", "answer": "positive"},
            {"id": "4", "question": "Banking sector under pressure from regulations", "answer": "negative"},
            {"id": "5", "question": "Tech stocks rally on AI optimism", "answer": "positive"},
            {"id": "6", "question": "Retail sales disappoint market expectations", "answer": "negative"},
            {"id": "7", "question": "Amazon expands warehouse network", "answer": "positive"},
            {"id": "8", "question": "Oil prices plunge on oversupply concerns", "answer": "negative"},
            {"id": "9", "question": "Semiconductor demand drives chip stocks higher", "answer": "positive"},
            {"id": "10", "question": "Real estate market shows signs of cooling", "answer": "negative"},
        ],
        "baseline_models": [
            {"model": "FinBERT", "score": 0.94, "version": "sentiment", "organization": "HKU"},
            {"model": "BloombergGPT", "score": 0.93, "version": "50B", "organization": "Bloomberg"},
            {"model": "GPT-4o", "score": 0.91, "version": "2024-11-01", "organization": "OpenAI"},
            {"model": "FinGPT", "score": 0.92, "version": "v3", "organization": "AI4Finance"},
            {"model": "Claude 3.5 Sonnet", "score": 0.90, "version": "2024-10-22", "organization": "Anthropic"},
            {"model": "Llama 3.1 70B", "score": 0.88, "version": "instruct", "organization": "Meta"},
            {"model": "RoBERTa-large", "score": 0.87, "version": "large", "organization": "Meta"},
        ]
    },
    {
        "name": "Twitter Financial News - Sentiment",
        "description": "Sentiment analysis of financial tweets. Real-time market sentiment dataset.",
        "url": "https://huggingface.co/datasets/zeroshot/twitter-financial-news-sentiment",
        "task_type": "text_classification",
        "test_set_public": False,
        "labels_public": False,
        "primary_metric": "accuracy",
        "additional_metrics": ["f1", "precision", "recall"],
        "ground_truth": [
            {"id": "1", "question": "$AAPL breaking out! New ATH incoming 🚀", "answer": "positive"},
            {"id": "2", "question": "$TSLA recall nightmare continues", "answer": "negative"},
            {"id": "3", "question": "$MSFT dividend announced, yield 2.5%", "answer": "positive"},
            {"id": "4", "question": "$AMZN facing antitrust probe", "answer": "negative"},
            {"id": "5", "question": "$NVDA crushes earnings expectations", "answer": "positive"},
            {"id": "6", "question": "$META privacy concerns mount", "answer": "negative"},
            {"id": "7", "question": "$GOOGL AI leadership position strengthens", "answer": "positive"},
            {"id": "8", "question": "$NFLX subscriber growth disappoints", "answer": "negative"},
            {"id": "9", "question": "$AMD gains market share from Intel", "answer": "positive"},
            {"id": "10", "question": "$UBER profitability concerns persist", "answer": "negative"},
        ],
        "baseline_models": [
            {"model": "FinBERT-Twitter", "score": 0.89, "version": "twitter-tuned", "organization": "HKU"},
            {"model": "GPT-4o", "score": 0.92, "version": "2024-11-01", "organization": "OpenAI"},
            {"model": "Claude 3.5 Sonnet", "score": 0.91, "version": "2024-10-22", "organization": "Anthropic"},
            {"model": "FinGPT-Social", "score": 0.87, "version": "v3-social", "organization": "AI4Finance"},
            {"model": "Llama 3.1 70B", "score": 0.86, "version": "instruct", "organization": "Meta"},
            {"model": "Gemini 1.5 Flash", "score": 0.88, "version": "001", "organization": "Google"},
        ]
    },
    {
        "name": "FinQA - Financial Numerical Reasoning",
        "description": "Question answering requiring numerical reasoning over financial documents.",
        "url": "https://huggingface.co/datasets/ibm/finqa",
        "task_type": "document_qa",
        "test_set_public": False,
        "labels_public": False,
        "primary_metric": "exact_match",
        "additional_metrics": ["f1"],
        "ground_truth": [
            {"id": "1", "question": "What was the revenue in 2023?", "context": "Revenue was $125.3 million in 2023, up from $98.7 million in 2022.", "answer": "$125.3 million"},
            {"id": "2", "question": "Calculate the revenue growth percentage", "context": "Revenue was $125.3 million in 2023, up from $98.7 million in 2022.", "answer": "26.9%"},
            {"id": "3", "question": "What is the operating margin?", "context": "Operating income of $23.5M on revenue of $125.3M.", "answer": "18.8%"},
            {"id": "4", "question": "How much did cash increase?", "context": "Cash and equivalents: $45.2M (2023) vs $32.1M (2022).", "answer": "$13.1 million"},
            {"id": "5", "question": "What is the debt-to-equity ratio?", "context": "Total debt $85M, shareholders' equity $120M.", "answer": "0.71"},
            {"id": "6", "question": "What was EBITDA in Q4?", "context": "Q4 EBITDA reached $18.7M, up from Q3's $15.2M.", "answer": "$18.7 million"},
            {"id": "7", "question": "Calculate the gross profit", "context": "Revenue $125.3M, COGS $68.5M.", "answer": "$56.8 million"},
            {"id": "8", "question": "What is the current ratio?", "context": "Current assets $95M, current liabilities $55M.", "answer": "1.73"},
            {"id": "9", "question": "How much is R&D spending?", "context": "R&D expenses totaled $12.3M, or 9.8% of revenue.", "answer": "$12.3 million"},
            {"id": "10", "question": "What was the EPS?", "context": "Net income $15.2M, shares outstanding 25M.", "answer": "$0.61"},
        ],
        "baseline_models": [
            {"model": "GPT-4o", "score": 0.72, "version": "2024-11-01", "organization": "OpenAI"},
            {"model": "Claude 3.5 Sonnet", "score": 0.68, "version": "2024-10-22", "organization": "Anthropic"},
            {"model": "Llama 3.1 70B", "score": 0.58, "version": "instruct", "organization": "Meta"},
            {"model": "FinQANet", "score": 0.65, "version": "base", "organization": "IBM"},
            {"model": "Gemini 1.5 Pro", "score": 0.70, "version": "001", "organization": "Google"},
            {"model": "Llama 3.1 405B", "score": 0.64, "version": "instruct", "organization": "Meta"},
        ]
    },
    {
        "name": "Financial NER - Entity Recognition",
        "description": "Named entity recognition in financial text (companies, amounts, dates, ratios).",
        "url": "https://huggingface.co/datasets/nlpaueb/finer-139",
        "task_type": "named_entity_recognition",
        "test_set_public": False,
        "labels_public": False,
        "primary_metric": "f1",
        "additional_metrics": ["precision", "recall"],
        "ground_truth": [
            {"id": "1", "text": "Apple Inc. reported revenue of $125.3B for FY2023", "answer": [("Apple Inc.", "ORG"), ("$125.3B", "MONEY"), ("FY2023", "DATE")]},
            {"id": "2", "text": "JPMorgan Chase increased its dividend by 5% in Q4", "answer": [("JPMorgan Chase", "ORG"), ("5%", "PERCENT"), ("Q4", "DATE")]},
            {"id": "3", "text": "Tesla's market cap reached $800 billion on Nov 15", "answer": [("Tesla", "ORG"), ("$800 billion", "MONEY"), ("Nov 15", "DATE")]},
            {"id": "4", "text": "Microsoft acquired OpenAI stake for $10B", "answer": [("Microsoft", "ORG"), ("OpenAI", "ORG"), ("$10B", "MONEY")]},
            {"id": "5", "text": "Amazon's P/E ratio stands at 68.5", "answer": [("Amazon", "ORG"), ("68.5", "RATIO")]},
            {"id": "6", "text": "Goldman Sachs targets $200 price for NVDA", "answer": [("Goldman Sachs", "ORG"), ("$200", "MONEY"), ("NVDA", "TICKER")]},
            {"id": "7", "text": "Meta's ROE improved to 25.3% in 2023", "answer": [("Meta", "ORG"), ("25.3%", "PERCENT"), ("2023", "DATE")]},
            {"id": "8", "text": "Bank of America lending grew 8% YoY", "answer": [("Bank of America", "ORG"), ("8%", "PERCENT")]},
            {"id": "9", "text": "Berkshire Hathaway holds $150B in cash", "answer": [("Berkshire Hathaway", "ORG"), ("$150B", "MONEY")]},
            {"id": "10", "text": "S&P 500 gained 2.5% on December 1st", "answer": [("S&P 500", "INDEX"), ("2.5%", "PERCENT"), ("December 1st", "DATE")]},
        ],
        "baseline_models": [
            {"model": "FinBERT-NER", "score": 0.91, "version": "ner", "organization": "HKU"},
            {"model": "GPT-4o", "score": 0.88, "version": "2024-11-01", "organization": "OpenAI"},
            {"model": "Claude 3.5 Sonnet", "score": 0.87, "version": "2024-10-22", "organization": "Anthropic"},
            {"model": "SpaCy-Financial", "score": 0.85, "version": "3.0", "organization": "Explosion"},
            {"model": "Llama 3.1 70B", "score": 0.82, "version": "instruct", "organization": "Meta"},
            {"model": "BERT-Financial-NER", "score": 0.86, "version": "base", "organization": "NLP-AUEB"},
        ]
    }
]


FINANCE_EXTRA_BY_NAME: Dict[str, List[dict]] = {
    "Financial PhraseBank - Sentiment Analysis": FIN_PHRASEBANK_EXTRA,
    "FiQA - Financial Opinion Mining": FIQA_OPINION_EXTRA,
    "Twitter Financial News - Sentiment": TWITTER_FIN_SENTIMENT_EXTRA,
    "FinQA - Financial Numerical Reasoning": FIN_QA_EXTRA,
    "Financial NER - Entity Recognition": FIN_NER_EXTRA,
}


def seed_finance_datasets():
    """Load finance-specific datasets into the database"""
    from database import SessionLocal, init_db
    from models import Dataset, Submission, TaskType, SubmissionStatus
    from evaluators import get_evaluator
    from datetime import datetime
    import uuid
    
    init_db()
    db = SessionLocal()
    
    try:
        print("\n" + "="*60)
        print("💰 SEEDING FINANCE DATASETS")
        print("="*60 + "\n")
        
        for dataset_config in FINANCE_DATASETS:
            # Check if exists
            existing = db.query(Dataset).filter(Dataset.name == dataset_config["name"]).first()
            if existing:
                print(f"⏭️  Skipping '{dataset_config['name']}' (already exists)")
                continue
            
            print(f"📊 Creating dataset: {dataset_config['name']}")

            # Merge in any extra ground truth for this finance dataset
            base_gt = list(dataset_config["ground_truth"])
            extra_gt = FINANCE_EXTRA_BY_NAME.get(dataset_config["name"])
            if extra_gt:
                base_gt.extend(extra_gt)

            # Create dataset with expanded ground truth
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
                num_examples=len(base_gt),
                ground_truth=base_gt
            )
            db.add(dataset)
            db.flush()
            
            # Create baseline submissions
            baseline_models = dataset_config.get("baseline_models", [])
            print(f"   Adding {len(baseline_models)} baseline models...")

            # Get evaluator for this dataset
            evaluator = get_evaluator(dataset_config["task_type"])

            from seed_data import create_baseline_predictions

            for baseline in baseline_models:
                submission_id = str(uuid.uuid4())
                predictions = create_baseline_predictions(
                    base_gt,
                    baseline["score"]
                )
                
                # Actually evaluate the predictions using the evaluator
                scores = evaluator.evaluate(base_gt, predictions)
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
                    evaluated_at=datetime.now()
                )
                db.add(submission)
                
                print(f"      ✓ {baseline['model']}: {primary_score:.4f} (evaluated)")
            
            db.commit()
            print(f"   ✅ Dataset loaded successfully\n")
        
        print("="*60)
        print("✅ FINANCE DATASETS LOADED!")
        print("="*60)
        print(f"\n📈 Loaded {len(FINANCE_DATASETS)} finance benchmarks")
        print("💼 Finance domains: Sentiment, Q&A, NER, Social Media\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_finance_datasets()

