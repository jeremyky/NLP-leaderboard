"""
Database models for the Leaderboard API
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, JSON, ForeignKey, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()


class TaskType(enum.Enum):
    """Supported task types for evaluation"""
    TEXT_CLASSIFICATION = "text_classification"
    NER = "named_entity_recognition"
    DOCUMENT_QA = "document_qa"
    LINE_QA = "line_qa"
    RETRIEVAL = "retrieval"


class SubmissionStatus(enum.Enum):
    """Status of a submission through the evaluation pipeline"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Dataset(Base):
    """
    Represents a benchmark dataset in the leaderboard
    """
    __tablename__ = "datasets"
    
    id = Column(String, primary_key=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(Text)
    url = Column(String)  # Link to dataset source
    task_type = Column(Enum(TaskType), nullable=False)
    
    # Dataset visibility - mix of public/private to prevent gaming
    test_set_public = Column(Boolean, default=False)  # Are test questions public?
    labels_public = Column(Boolean, default=False)    # Are ground truth labels public?
    
    # Evaluation configuration
    primary_metric = Column(String, nullable=False)  # e.g., "accuracy", "f1", "exact_match"
    additional_metrics = Column(JSON, default=list)  # e.g., ["precision", "recall"]
    
    # Metadata
    num_examples = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Ground truth data stored as JSON
    # Format: [{"id": "q1", "question": "...", "context": "...", "answer": "..."}]
    ground_truth = Column(JSON, nullable=False)
    
    # Relationships
    submissions = relationship("Submission", back_populates="dataset", cascade="all, delete-orphan")


class Submission(Base):
    """
    Represents a model submission to a dataset
    """
    __tablename__ = "submissions"
    
    id = Column(String, primary_key=True)
    dataset_id = Column(String, ForeignKey("datasets.id"), nullable=False)
    
    # Model information
    model_name = Column(String, nullable=False, index=True)
    model_version = Column(String)
    organization = Column(String)  # Who submitted it
    
    # Submission data
    # Format: [{"id": "q1", "prediction": "..."}]
    predictions = Column(JSON, nullable=False)
    
    # Evaluation results
    status = Column(Enum(SubmissionStatus), default=SubmissionStatus.PENDING, index=True)
    primary_score = Column(Float)  # Main score for ranking
    detailed_scores = Column(JSON)  # All computed metrics
    confidence_interval = Column(String)  # e.g., "0.93 - 0.97"
    
    # Metadata
    submission_metadata = Column(JSON)  # Any additional info (model params, etc.)
    is_internal = Column(Boolean, default=False)  # Internal vs external submission
    created_at = Column(DateTime, default=datetime.utcnow)
    evaluated_at = Column(DateTime)
    error_message = Column(Text)  # If evaluation failed
    
    # Relationships
    dataset = relationship("Dataset", back_populates="submissions")


class LeaderboardEntry(Base):
    """
    Cached leaderboard rankings for fast queries
    This is regenerated when new submissions are evaluated
    """
    __tablename__ = "leaderboard_entries"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    dataset_id = Column(String, ForeignKey("datasets.id"), nullable=False)
    submission_id = Column(String, ForeignKey("submissions.id"), nullable=False)
    
    rank = Column(Integer, nullable=False)
    model_name = Column(String, nullable=False)
    score = Column(Float, nullable=False)
    confidence_interval = Column(String)
    updated_at = Column(String)  # Human-readable date like "Nov 2024"
    
    # For filtering/sorting
    is_internal = Column(Boolean, default=False)
    task_type = Column(Enum(TaskType))
    
    created_at = Column(DateTime, default=datetime.utcnow)

