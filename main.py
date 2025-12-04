"""
Main FastAPI application for the Leaderboard API
"""
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from datetime import datetime

from database import get_db, init_db
from models import Dataset, Submission, LeaderboardEntry, TaskType, SubmissionStatus
from schemas import (
    DatasetCreate, DatasetResponse, DatasetPublic,
    SubmissionCreate, SubmissionResponse,
    LeaderboardResponse, LeaderboardEntryResponse,
    SuccessResponse, ErrorResponse
)
from evaluators import get_evaluator
from evaluation_service import evaluate_submission

# Initialize FastAPI app
app = FastAPI(
    title="Anote Leaderboard API",
    description="API for managing benchmark datasets and model submissions",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print("Leaderboard API started successfully")


# ==================== Dataset Endpoints ====================

@app.post("/api/datasets", response_model=SuccessResponse, status_code=201)
async def create_dataset(
    dataset: DatasetCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new benchmark dataset
    
    This endpoint allows you to add a new dataset to the leaderboard.
    You can control visibility (public/private test sets) to prevent metric gaming.
    """
    # Check if dataset name already exists
    existing = db.query(Dataset).filter(Dataset.name == dataset.name).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Dataset '{dataset.name}' already exists")
    
    # Create new dataset
    dataset_id = str(uuid.uuid4())
    db_dataset = Dataset(
        id=dataset_id,
        name=dataset.name,
        description=dataset.description,
        url=dataset.url,
        task_type=TaskType(dataset.task_type),
        test_set_public=dataset.test_set_public,
        labels_public=dataset.labels_public,
        primary_metric=dataset.primary_metric,
        additional_metrics=dataset.additional_metrics,
        num_examples=dataset.num_examples or len(dataset.ground_truth),
        ground_truth=dataset.ground_truth
    )
    
    db.add(db_dataset)
    db.commit()
    db.refresh(db_dataset)
    
    return SuccessResponse(
        message="Dataset created successfully",
        data={"dataset_id": dataset_id, "name": dataset.name}
    )


@app.get("/api/datasets", response_model=List[DatasetPublic])
async def list_datasets(
    task_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    List all available datasets (public info only)
    
    Optionally filter by task_type.
    Ground truth labels are never exposed through this endpoint.
    """
    query = db.query(Dataset)
    
    if task_type:
        try:
            query = query.filter(Dataset.task_type == TaskType(task_type))
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid task_type: {task_type}")
    
    datasets = query.all()
    
    # Prepare public response
    result = []
    for ds in datasets:
        questions = None
        if ds.test_set_public:
            # Provide questions without answers
            questions = [
                {k: v for k, v in item.items() if k != 'answer'}
                for item in ds.ground_truth
            ]
        
        result.append(DatasetPublic(
            id=ds.id,
            name=ds.name,
            description=ds.description,
            url=ds.url,
            task_type=ds.task_type.value,
            test_set_public=ds.test_set_public,
            primary_metric=ds.primary_metric,
            num_examples=ds.num_examples,
            questions=questions
        ))
    
    return result


@app.get("/api/datasets/{dataset_id}", response_model=DatasetPublic)
async def get_dataset(
    dataset_id: str,
    db: Session = Depends(get_db)
):
    """Get details of a specific dataset"""
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    questions = None
    if dataset.test_set_public:
        questions = [
            {k: v for k, v in item.items() if k != 'answer'}
            for item in dataset.ground_truth
        ]
    
    return DatasetPublic(
        id=dataset.id,
        name=dataset.name,
        description=dataset.description,
        url=dataset.url,
        task_type=dataset.task_type.value,
        test_set_public=dataset.test_set_public,
        primary_metric=dataset.primary_metric,
        num_examples=dataset.num_examples,
        questions=questions
    )


@app.get("/api/datasets/{dataset_id}/questions")
async def get_dataset_questions(
    dataset_id: str,
    db: Session = Depends(get_db)
):
    """
    Get test questions for a dataset (without answers)
    
    This endpoint provides the questions and their IDs so users can prepare predictions.
    Ground truth answers are never exposed.
    """
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # Return questions without answers
    questions = [
        {k: v for k, v in item.items() if k != 'answer'}
        for item in dataset.ground_truth
    ]
    
    return {
        "dataset_id": dataset.id,
        "dataset_name": dataset.name,
        "task_type": dataset.task_type.value,
        "num_questions": len(questions),
        "questions": questions
    }


# ==================== Submission Endpoints ====================

@app.post("/api/submissions", response_model=SuccessResponse, status_code=202)
async def submit_predictions(
    submission: SubmissionCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Submit model predictions for evaluation
    
    Predictions are queued for evaluation. You'll receive a submission_id
    to check the status and results later.
    """
    # Verify dataset exists
    dataset = db.query(Dataset).filter(Dataset.id == submission.dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # Create submission
    submission_id = str(uuid.uuid4())
    db_submission = Submission(
        id=submission_id,
        dataset_id=submission.dataset_id,
        model_name=submission.model_name,
        model_version=submission.model_version,
        organization=submission.organization,
        predictions=submission.predictions,
        is_internal=submission.is_internal,
        submission_metadata=submission.submission_metadata,
        status=SubmissionStatus.PENDING
    )
    
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    
    # Queue evaluation as background task
    background_tasks.add_task(evaluate_submission, submission_id)
    
    return SuccessResponse(
        message="Submission received and queued for evaluation",
        data={
            "submission_id": submission_id,
            "status": "pending",
            "check_status_url": f"/api/submissions/{submission_id}"
        }
    )


@app.get("/api/submissions/{submission_id}", response_model=SubmissionResponse)
async def get_submission_status(
    submission_id: str,
    db: Session = Depends(get_db)
):
    """
    Check the status and results of a submission
    
    Returns evaluation results if completed, or status if still processing.
    """
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    return SubmissionResponse(
        id=submission.id,
        dataset_id=submission.dataset_id,
        model_name=submission.model_name,
        model_version=submission.model_version,
        organization=submission.organization,
        status=submission.status.value,
        primary_score=submission.primary_score,
        detailed_scores=submission.detailed_scores,
        confidence_interval=submission.confidence_interval,
        is_internal=submission.is_internal,
        created_at=submission.created_at,
        evaluated_at=submission.evaluated_at,
        error_message=submission.error_message
    )


@app.get("/api/submissions", response_model=List[SubmissionResponse])
async def list_submissions(
    dataset_id: Optional[str] = None,
    model_name: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all submissions with optional filters"""
    query = db.query(Submission)
    
    if dataset_id:
        query = query.filter(Submission.dataset_id == dataset_id)
    if model_name:
        query = query.filter(Submission.model_name == model_name)
    if status:
        try:
            query = query.filter(Submission.status == SubmissionStatus(status))
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid status: {status}")
    
    submissions = query.order_by(Submission.created_at.desc()).all()
    
    return [
        SubmissionResponse(
            id=sub.id,
            dataset_id=sub.dataset_id,
            model_name=sub.model_name,
            model_version=sub.model_version,
            organization=sub.organization,
            status=sub.status.value,
            primary_score=sub.primary_score,
            detailed_scores=sub.detailed_scores,
            confidence_interval=sub.confidence_interval,
            is_internal=sub.is_internal,
            created_at=sub.created_at,
            evaluated_at=sub.evaluated_at,
            error_message=sub.error_message
        )
        for sub in submissions
    ]


# ==================== Leaderboard Endpoints ====================

@app.get("/api/leaderboard", response_model=List[LeaderboardResponse])
async def get_all_leaderboards(
    task_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get leaderboard for all datasets
    
    Returns ranked model submissions for each dataset.
    Optionally filter by task_type.
    """
    query = db.query(Dataset)
    
    if task_type:
        try:
            query = query.filter(Dataset.task_type == TaskType(task_type))
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid task_type: {task_type}")
    
    datasets = query.all()
    leaderboards: List[LeaderboardResponse] = []
    
    for dataset in datasets:
        # Get completed submissions sorted by score
        submissions = (
            db.query(Submission)
            .filter(
                Submission.dataset_id == dataset.id,
                Submission.status == SubmissionStatus.COMPLETED
            )
            .order_by(Submission.primary_score.desc())
            .all()
        )
        
        entries = []
        for rank, sub in enumerate(submissions, start=1):
            # Format date
            updated_month = sub.evaluated_at.strftime("%b %Y") if sub.evaluated_at else "N/A"
            
            # Create entry dict with detailed scores
            entry_data = {
                "rank": rank,
                "model_name": sub.model_name,
                "score": sub.primary_score,
                "confidence_interval": sub.confidence_interval,
                "updated_at": updated_month,
                "is_internal": sub.is_internal,
                "submission_id": sub.id,
                "detailed_scores": sub.detailed_scores,  # Add detailed scores
            }
            entries.append(entry_data)
        
        # Always include the dataset, even if there are no submissions yet.
        # This ensures that newly imported benchmarks (e.g., from HuggingFace)
        # are visible in the frontend and can show "0 models" instead of
        # being entirely hidden.
        leaderboards.append(LeaderboardResponse(
            dataset_id=dataset.id,
            dataset_name=dataset.name,
            task_type=dataset.task_type.value,
            url=dataset.url,
            primary_metric=dataset.primary_metric,
            entries=entries,
        ))
    
    return leaderboards


@app.get("/api/leaderboard/{dataset_id}", response_model=LeaderboardResponse)
async def get_dataset_leaderboard(
    dataset_id: str,
    include_internal: bool = True,
    db: Session = Depends(get_db)
):
    """
    Get leaderboard for a specific dataset
    
    Optionally filter out internal submissions with include_internal=false
    """
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    query = db.query(Submission).filter(
        Submission.dataset_id == dataset_id,
        Submission.status == SubmissionStatus.COMPLETED
    )
    
    if not include_internal:
        query = query.filter(Submission.is_internal == False)
    
    submissions = query.order_by(Submission.primary_score.desc()).all()
    
    entries = []
    for rank, sub in enumerate(submissions, start=1):
        updated_month = sub.evaluated_at.strftime("%b %Y") if sub.evaluated_at else "N/A"
        
        entries.append({
            "rank": rank,
            "model_name": sub.model_name,
            "score": sub.primary_score,
            "confidence_interval": sub.confidence_interval,
            "updated_at": updated_month,
            "is_internal": sub.is_internal,
            "submission_id": sub.id,
            "detailed_scores": sub.detailed_scores
        })
    
    return LeaderboardResponse(
        dataset_id=dataset.id,
        dataset_name=dataset.name,
        task_type=dataset.task_type.value,
        url=dataset.url,
        primary_metric=dataset.primary_metric,
        entries=entries
    )


# ==================== Data Management ====================

@app.post("/api/admin/seed-data", response_model=SuccessResponse)
async def seed_sample_data(db: Session = Depends(get_db)):
    """
    Load sample datasets and baseline models
    
    This populates the leaderboard with popular benchmarks.
    """
    try:
        from seed_data import SAMPLE_DATASETS, create_baseline_predictions
        from datetime import datetime as dt
        
        datasets_added = 0
        submissions_added = 0
        
        for dataset_config in SAMPLE_DATASETS:
            # Check if dataset already exists
            existing = db.query(Dataset).filter(Dataset.name == dataset_config["name"]).first()
            if existing:
                continue
            
            # Create dataset
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
                ground_truth=dataset_config["ground_truth"]
            )
            db.add(dataset)
            db.flush()
            datasets_added += 1
            
            # Create baseline submissions
            for baseline in dataset_config.get("baseline_models", []):
                submission_id = str(uuid.uuid4())
                predictions = create_baseline_predictions(
                    dataset_config["ground_truth"],
                    baseline["score"]
                )
                
                submission = Submission(
                    id=submission_id,
                    dataset_id=dataset_id,
                    model_name=baseline["model"],
                    model_version=baseline.get("version"),
                    organization=baseline.get("organization"),
                    predictions=predictions,
                    status=SubmissionStatus.COMPLETED,
                    primary_score=baseline["score"],
                    detailed_scores={dataset_config["primary_metric"]: baseline["score"]},
                    confidence_interval=f"{baseline['score']-0.02:.2f} - {baseline['score']+0.02:.2f}",
                    is_internal=True,
                    created_at=dt.now(),
                    evaluated_at=dt.now()
                )
                db.add(submission)
                submissions_added += 1
            
            db.commit()
        
        return SuccessResponse(
            message="Sample data loaded successfully",
            data={
                "datasets_added": datasets_added,
                "submissions_added": submissions_added
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/admin/import-huggingface", response_model=SuccessResponse)
async def import_from_huggingface(
    dataset_name: str,
    config: str = "default",
    split: str = "test",
    num_samples: int = 100,
    db: Session = Depends(get_db)
):
    """
    Import a dataset from HuggingFace Hub
    
    Args:
        dataset_name: HuggingFace dataset identifier (e.g., "ag_news")
        config: Dataset configuration/subset
        split: Dataset split (train/validation/test)
        num_samples: Number of samples to import
    """
    try:
        from hf_importer import HuggingFaceImporter
        
        # Import from HuggingFace
        importer = HuggingFaceImporter()
        dataset_data = importer.import_dataset(dataset_name, config, split, num_samples)
        
        if not dataset_data:
            raise HTTPException(status_code=400, detail="Failed to import dataset from HuggingFace")
        
        # Check if dataset already exists
        existing = db.query(Dataset).filter(Dataset.name == dataset_data["name"]).first()
        if existing:
            raise HTTPException(status_code=400, detail="Dataset already exists")
        
        # Create dataset
        dataset_id = str(uuid.uuid4())
        # Avoid passing task_type/name/num_examples twice (from **dataset_data and explicit args)
        filtered_data = {
            k: v
            for k, v in dataset_data.items()
            if k not in {"name", "task_type", "num_examples"}
        }
        dataset = Dataset(
            id=dataset_id,
            **filtered_data,
            name=dataset_data["name"],
            task_type=TaskType(dataset_data["task_type"]),
            num_examples=len(dataset_data["ground_truth"])
        )
        
        db.add(dataset)
        db.commit()
        db.refresh(dataset)
        
        return SuccessResponse(
            message=f"Successfully imported {dataset_name} from HuggingFace",
            data={
                "dataset_id": dataset_id,
                "name": dataset_data["name"],
                "num_examples": len(dataset_data["ground_truth"])
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Metrics Information ====================

@app.get("/api/metrics")
async def get_all_metrics():
    """Get information about all available metrics"""
    from metrics_info import METRICS_CATALOG
    return METRICS_CATALOG


@app.get("/api/metrics/{metric_name}")
async def get_metric_info(metric_name: str):
    """Get detailed information about a specific metric"""
    from metrics_info import get_metric_info as get_info
    info = get_info(metric_name)
    if not info.get("description"):
        raise HTTPException(status_code=404, detail="Metric not found")
    return info


@app.get("/api/metrics/task/{task_type}")
async def get_task_metrics(task_type: str):
    """Get all relevant metrics for a specific task type"""
    from metrics_info import get_metrics_for_task, get_metric_info as get_info
    
    metric_names = get_metrics_for_task(task_type)
    metrics = {name: get_info(name) for name in metric_names}
    return metrics


# ==================== Health Check ====================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "leaderboard-api"}

