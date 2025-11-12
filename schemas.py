"""
Pydantic schemas for API request/response validation
"""
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional
from datetime import datetime
from models import TaskType, SubmissionStatus


# Dataset schemas
class DatasetCreate(BaseModel):
    """Schema for creating a new dataset"""
    name: str = Field(..., description="Unique name for the dataset")
    description: Optional[str] = Field(None, description="Description of the dataset")
    url: Optional[str] = Field(None, description="Link to dataset source")
    task_type: str = Field(..., description="Type of task (text_classification, ner, document_qa, line_qa, retrieval)")
    test_set_public: bool = Field(False, description="Whether test questions are publicly accessible")
    labels_public: bool = Field(False, description="Whether ground truth labels are public")
    primary_metric: str = Field(..., description="Primary metric for ranking (e.g., accuracy, f1)")
    additional_metrics: List[str] = Field(default_factory=list, description="Additional metrics to compute")
    num_examples: Optional[int] = Field(None, description="Number of examples in dataset")
    ground_truth: List[Dict[str, Any]] = Field(..., description="Ground truth data")
    
    @validator('task_type')
    def validate_task_type(cls, v):
        valid_types = [t.value for t in TaskType]
        if v not in valid_types:
            raise ValueError(f"task_type must be one of {valid_types}")
        return v


class DatasetResponse(BaseModel):
    """Schema for dataset response"""
    id: str
    name: str
    description: Optional[str]
    url: Optional[str]
    task_type: str
    test_set_public: bool
    labels_public: bool
    primary_metric: str
    additional_metrics: List[str]
    num_examples: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DatasetPublic(BaseModel):
    """Public dataset info (without ground truth)"""
    id: str
    name: str
    description: Optional[str]
    url: Optional[str]
    task_type: str
    test_set_public: bool
    primary_metric: str
    num_examples: Optional[int]
    # Ground truth questions without answers (if test_set_public)
    questions: Optional[List[Dict[str, Any]]] = None
    
    class Config:
        from_attributes = True


# Submission schemas
class SubmissionCreate(BaseModel):
    """Schema for creating a new submission"""
    dataset_id: str = Field(..., description="ID of the dataset")
    model_name: str = Field(..., description="Name of the model")
    model_version: Optional[str] = Field(None, description="Version of the model")
    organization: Optional[str] = Field(None, description="Organization submitting the model")
    predictions: List[Dict[str, Any]] = Field(..., description="Model predictions")
    is_internal: bool = Field(False, description="Whether this is an internal submission")
    submission_metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    
    @validator('predictions')
    def validate_predictions(cls, v):
        if not v:
            raise ValueError("predictions cannot be empty")
        for pred in v:
            if 'id' not in pred or 'prediction' not in pred:
                raise ValueError("Each prediction must have 'id' and 'prediction' fields")
        return v


class SubmissionResponse(BaseModel):
    """Schema for submission response"""
    id: str
    dataset_id: str
    model_name: str
    model_version: Optional[str]
    organization: Optional[str]
    status: str
    primary_score: Optional[float]
    detailed_scores: Optional[Dict[str, float]]
    confidence_interval: Optional[str]
    is_internal: bool
    created_at: datetime
    evaluated_at: Optional[datetime]
    error_message: Optional[str]
    
    class Config:
        from_attributes = True


# Leaderboard schemas
class LeaderboardEntryResponse(BaseModel):
    """Schema for a leaderboard entry"""
    rank: int
    model_name: str
    score: float
    confidence_interval: Optional[str]
    updated_at: str
    is_internal: bool
    submission_id: str
    
    class Config:
        from_attributes = True


class LeaderboardResponse(BaseModel):
    """Schema for full leaderboard response"""
    dataset_id: str
    dataset_name: str
    task_type: str
    url: Optional[str]
    primary_metric: str
    entries: List[LeaderboardEntryResponse]


# General response schemas
class SuccessResponse(BaseModel):
    """Generic success response"""
    status: str = "success"
    message: str
    data: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """Generic error response"""
    status: str = "error"
    message: str
    details: Optional[Dict[str, Any]] = None

