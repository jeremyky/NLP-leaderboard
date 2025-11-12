# Anote Leaderboard API

## Overview
A **production-ready API** for the Anote Model Leaderboard, enabling:
1. **Adding new datasets** to the leaderboard across **all task types**
2. **Submitting model predictions** for automated evaluation
3. **Querying leaderboard rankings** with real-time updates

The API serves as a transparent, scalable, and **game-resistant** benchmarking platform for AI models, supporting **text classification, named entity recognition, document-level Q&A (chatbot), and line-level Q&A (prompting)**.

---

## ✨ Key Features

### 🛡️ Anti-Gaming Architecture
- **Mixed dataset visibility** (public/private test sets)
- **Server-side evaluation** (no user-computed scores)
- **Evaluation queue** (prevents real-time feedback loops)
- **Confidence intervals** (statistical significance)

### 📊 Multiple Task Types
- **Text Classification**: Multi-class and binary classification
- **Named Entity Recognition**: Entity extraction with span matching
- **Question Answering**: Both document and line-level QA
- **Retrieval**: Document/passage retrieval accuracy

### 🚀 Production Ready
- **FastAPI** with automatic OpenAPI docs
- **SQLAlchemy** ORM with SQLite/PostgreSQL support
- **Async evaluation** via background tasks
- **Complete test coverage** with example scripts

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
cd anoteleaderboard

# Install dependencies
pip install -r requirements.txt

# Start the API server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Or use the startup script:

```bash
./run.sh
```

### Access API Documentation

Once running, visit:
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## 📚 API Endpoints

### Datasets
- `POST /api/datasets` - Create a new dataset
- `GET /api/datasets` - List all datasets
- `GET /api/datasets/{id}` - Get dataset details

### Submissions
- `POST /api/submissions` - Submit model predictions
- `GET /api/submissions/{id}` - Check submission status
- `GET /api/submissions` - List all submissions

### Leaderboard
- `GET /api/leaderboard` - Get all leaderboards
- `GET /api/leaderboard/{dataset_id}` - Get specific leaderboard

---

## 💡 Example Usage

### 1. Create a Dataset

```python
import requests

dataset = {
    "name": "Financial Sentiment Analysis",
    "task_type": "text_classification",
    "test_set_public": False,  # Prevent gaming
    "labels_public": False,
    "primary_metric": "accuracy",
    "ground_truth": [
        {"id": "1", "question": "Stock prices soared", "answer": "positive"},
        {"id": "2", "question": "Company reports losses", "answer": "negative"}
    ]
}

response = requests.post("http://localhost:8000/api/datasets", json=dataset)
print(response.json())
```

### 2. Submit Predictions

```python
submission = {
    "dataset_id": "your-dataset-id",
    "model_name": "GPT-4o",
    "predictions": [
        {"id": "1", "prediction": "positive"},
        {"id": "2", "prediction": "negative"}
    ]
}

response = requests.post("http://localhost:8000/api/submissions", json=submission)
submission_id = response.json()['data']['submission_id']
```

### 3. Check Results

```python
response = requests.get(f"http://localhost:8000/api/submissions/{submission_id}")
result = response.json()
print(f"Status: {result['status']}")
print(f"Score: {result['primary_score']}")
```

### 4. View Leaderboard

```python
response = requests.get(f"http://localhost:8000/api/leaderboard/{dataset_id}")
leaderboard = response.json()

for entry in leaderboard['entries']:
    print(f"{entry['rank']}. {entry['model_name']}: {entry['score']}")
```

### Complete Example

Run the provided example script to see the full workflow:

```bash
python example_usage.py
```

---

## 📖 Documentation

- **[SETUP.md](SETUP.md)** - Detailed setup and deployment guide
- **[API_DESIGN.md](API_DESIGN.md)** - Architecture and design decisions
- **[example_usage.py](example_usage.py)** - Complete working example

---

## 🏗️ Architecture

```
Client → FastAPI Endpoints → Database (SQLite/PostgreSQL)
              ↓
        Evaluation Queue
              ↓
    Task-Specific Evaluators
              ↓
    Update Scores & Rankings
```

**Key Components:**
- **models.py** - Database schema (SQLAlchemy ORM)
- **schemas.py** - API request/response validation (Pydantic)
- **main.py** - FastAPI application and endpoints
- **evaluators.py** - Task-specific evaluation metrics
- **evaluation_service.py** - Background evaluation processing
- **database.py** - Database connection and session management

---

## 🔒 Anti-Gaming Features

### 1. Dataset Visibility Control
- Control whether test questions are public
- Ground truth labels are NEVER exposed
- Prevents overfitting to test data

### 2. Server-Side Evaluation
- Users submit predictions, not scores
- All metrics computed server-side
- Consistent evaluation across submissions

### 3. Evaluation Queue
- Async processing prevents real-time feedback
- Can add rate limiting per organization
- Scalable to distributed workers (Celery)

---

## 📊 Supported Metrics

### Text Classification
- Accuracy, Precision, Recall, F1 (macro-averaged)

### Named Entity Recognition
- Precision, Recall, F1 (exact span matching)

### Question Answering
- Exact Match, Token F1 (normalized comparison)

### Retrieval
- Retrieval Accuracy (correct document found)

---

## 🌐 Production Deployment

### Recommended Stack
- **Database**: PostgreSQL (better concurrency than SQLite)
- **Task Queue**: Celery + Redis (distributed evaluation)
- **Web Server**: Gunicorn + Nginx
- **Monitoring**: Prometheus + Grafana

### Docker Deployment

```bash
docker build -t leaderboard-api .
docker run -p 8000:8000 leaderboard-api
```

See [SETUP.md](SETUP.md) for detailed production deployment guide.

---

## 🎯 Goals & Roadmap

### Current Status ✅
- ✅ Core API implementation
- ✅ Multiple task type support
- ✅ Anti-gaming architecture
- ✅ Background evaluation queue
- ✅ Complete documentation

### Phase 2 (Future)
- [ ] API authentication and rate limiting
- [ ] Celery for distributed evaluation
- [ ] Bootstrap confidence intervals
- [ ] Webhook notifications
- [ ] Detailed per-example analysis
- [ ] Multi-language support

### Phase 3 (Vision)
- [ ] Slack/LinkedIn integration
- [ ] CI/CD hooks for auto-submission
- [ ] Human-in-the-loop evaluation
- [ ] Model cards and metadata
- [ ] Ensemble benchmarking

---

## 📹 Reference Materials

Learn more about the vision:
- **Languages and Model Leaderboard**: [Watch](https://www.youtube.com/watch?v=JZ8foxMtct8)
- **Model Leaderboard**: [Watch](https://www.youtube.com/watch?v=e8V6MfPqAaE)
- **AI Day Summit Talk**: [Watch (min 20)](https://www.youtube.com/watch?v=eR_fnV0DyHE)

---

## 🤝 Integration

This API is designed to integrate with:
- **Leaderboard Page**: [anote.ai/leaderboard](https://anote.ai/leaderboard)
- **Submit Page**: [anote.ai/submittoleaderboard](https://anote.ai/submittoleaderboard)
- **Autonomous Intelligence**: [GitHub](https://github.com/nv78/Autonomous-Intelligence/)

The existing `Leaderboard.js` React component can be updated to fetch data from these API endpoints.

## Contact
**Project Lead**: Natan Vidra – nvidra@anote.ai
**Leaderboard**: [https://anote.ai/leaderboard](https://anote.ai/leaderboard)
