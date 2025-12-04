"""
Structured logging configuration for the leaderboard API

Provides JSON-formatted logs for production monitoring and debugging.
"""
import logging
import sys
from pythonjsonlogger import jsonlogger


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """
    Configure structured JSON logging
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("leaderboard")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove existing handlers
    logger.handlers = []
    
    # JSON formatter for structured logs
    formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(name)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger


# Global logger instance
logger = setup_logging()


def log_api_request(endpoint: str, method: str, user_id: str = None, **kwargs):
    """Log an API request with metadata"""
    logger.info(
        "API request",
        extra={
            "endpoint": endpoint,
            "method": method,
            "user_id": user_id,
            **kwargs
        }
    )


def log_evaluation(submission_id: str, dataset_id: str, model_name: str, score: float, **kwargs):
    """Log a model evaluation"""
    logger.info(
        "Evaluation completed",
        extra={
            "submission_id": submission_id,
            "dataset_id": dataset_id,
            "model_name": model_name,
            "score": score,
            **kwargs
        }
    )


def log_error(error_type: str, message: str, **kwargs):
    """Log an error with context"""
    logger.error(
        message,
        extra={
            "error_type": error_type,
            **kwargs
        }
    )


def log_cache_hit(cache_key: str, endpoint: str):
    """Log a cache hit for monitoring"""
    logger.debug(
        "Cache hit",
        extra={
            "cache_key": cache_key,
            "endpoint": endpoint
        }
    )


def log_cache_miss(cache_key: str, endpoint: str):
    """Log a cache miss for monitoring"""
    logger.debug(
        "Cache miss",
        extra={
            "cache_key": cache_key,
            "endpoint": endpoint
        }
    )

