# Anote Leaderboard

A **production-ready** leaderboard platform for benchmarking AI models across multiple domains and task types.

## Overview

The Anote Leaderboard is a comprehensive evaluation platform featuring:
- **30+ benchmark datasets** across general, finance, multilingual, science, code, and safety domains
- **5 task types** (text classification, NER, QA, line QA, retrieval)
- **20+ evaluation metrics** with detailed explanations
- **Premium React UI** with multiple view modes, model comparison, and submission history
- **FastAPI backend** with caching, rate limiting, and structured logging
- **HuggingFace integration** for easy dataset imports
- **Complete test suite** and CI/CD pipelines

---

## ✨ Key Features

### 📊 Comprehensive Benchmarks
- **30+ datasets** with 50-2000 examples each
- **Multiple domains**: General NLP, Finance, Multilingual, Science, Code, Safety
- **Popular benchmarks**: AG News, SST-2, SQuAD, MNLI, GSM8K, Financial PhraseBank, XNLI, AI2 ARC, TruthfulQA, and more
- **HuggingFace integration** for bulk imports

### 🎯 Advanced Evaluation
- **5 task types**: Text classification, NER, Document QA, Line QA, Retrieval
- **20+ metrics**: Accuracy, F1, Precision, Recall, Exact Match, Token F1, MRR, NDCG, Cohen's Kappa, Matthews Correlation, Per-Language metrics, and more
- **Detailed metric explanations** with formulas, use cases, and interpretation guides
- **Per-language breakdowns** for multilingual datasets

### 🎨 Premium UI/UX
- **Multiple view modes**: List, 3×3 grid, single-card carousel
- **Model comparison**: Side-by-side metric comparison (up to 3 models)
- **Submission workflow**: JSON upload/paste, auto-filled dates, format examples
- **Loading skeletons** and error handling throughout
- **Responsive design** with dark theme

### 🚀 Production Infrastructure
- **Caching layer**: 5-minute TTL for leaderboard queries
- **Rate limiting**: Per-IP limits (10/min submissions, 200/min leaderboards)
- **Structured logging**: JSON logs for monitoring and debugging
- **Cache invalidation**: Automatic on new submissions
- **Monitoring endpoints**: Cache stats and health checks

### 🛡️ Anti-Gaming Architecture
- **Server-side evaluation** (no user-computed scores)
- **Background task queue** (async processing)
- **Private test sets** option
- **Confidence intervals** for statistical significance

---

## 🚀 Quick Start

### 1. Clone and Install

```bash
git clone https://github.com/yourusername/anoteleaderboard.git
cd anoteleaderboard

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
cd frontend
npm install
cd ..
```

### 2. Seed the Database

```bash
# Load general benchmarks (AG News, SST-2, SQuAD, IMDB, TruthfulQA)
python seed_data.py

# Load finance datasets (Financial PhraseBank, Twitter sentiment, FinNER)
python finance_datasets.py

# Load multilingual datasets (XNLI, MGSM, XCOPA, XQUAD)
python multilingual_datasets.py

# Load science/code datasets (AI2 ARC, Science QA, Code Reasoning)
python science_datasets.py

# (Optional) Populate empty datasets with baseline models
python seed_missing_baselines.py
```

### 3. Start Backend

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API will be available at `http://localhost:8000`
- **Swagger UI**: http://localhost:8000/docs
- **Health check**: http://localhost:8000/health

### 4. Start Frontend

In a separate terminal:

```bash
cd frontend
npm run dev
```

Frontend will be available at `http://localhost:3000`

---

## 📚 Documentation

### In-App Documentation
Visit `/docs` in the frontend (e.g., `http://localhost:3000/docs`) for:
- API quick reference
- Architecture overview
- Contributing guide
- Links to interactive API docs (Swagger UI)

### Full Documentation Files
- **[API Reference](docs/API.md)** - Complete API endpoint documentation with examples
- **[Architecture Overview](docs/ARCHITECTURE.md)** - System design, data flow, and technical decisions
- **[Contributing Guide](docs/CONTRIBUTING.md)** - Development setup and contribution guidelines

### Interactive API Documentation
When the backend is running, visit:
- **Swagger UI**: `http://localhost:8000/docs` (or port 8001)
- **ReDoc**: `http://localhost:8000/redoc`

These provide interactive documentation where you can test all API endpoints directly in your browser.

## 🧪 Running Tests

From the project root:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_evaluators_by_task.py

# Run with coverage
pytest --cov=. --cov-report=html
```

**Test Coverage:**
- Evaluator unit tests for all task types
- End-to-end submission pipeline tests
- Internal baseline consistency checks
- HuggingFace import tests
- Metrics API tests
- Dataset seeding tests

## 🔧 Configuration

### Backend Environment Variables

Create `.env` in the project root (optional):

```bash
# Database (defaults to SQLite)
DATABASE_URL=sqlite:///./leaderboard.db
# For PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost:5432/leaderboard

# Logging
LOG_LEVEL=INFO

# Redis (optional, for distributed caching)
# REDIS_URL=redis://localhost:6379/0
```

### Frontend Environment Variables

Create `frontend/.env` (optional):

```bash
# Backend API URL (defaults to http://localhost:8000)
VITE_API_URL=http://localhost:8000
```

## 📦 Available Scripts

### Backend Scripts

```bash
# Seed general datasets
python seed_data.py

# Seed domain-specific datasets
python finance_datasets.py
python multilingual_datasets.py
python science_datasets.py

# Import HuggingFace datasets in bulk
python hf_seed_from_proposals.py

# Populate empty datasets with baselines
python seed_missing_baselines.py

# Run tests
pytest
```

### Frontend Scripts

```bash
cd frontend

# Development server
npm run dev

# Production build
npm run build

# Preview production build
npm run preview

# Linting
npm run lint
```

---

## 📚 API Endpoints

### Datasets
- `POST /api/datasets` - Create a new dataset
- `GET /api/datasets` - List all datasets (public metadata only)
- `GET /api/datasets/{id}` - Get dataset details
- `GET /api/datasets/{id}/questions` - Get test questions (without answers)

### Submissions
- `POST /api/submissions` - Submit model predictions for evaluation
- `GET /api/submissions/{id}` - Check submission status and results
- `GET /api/submissions` - List all submissions with filters

### Leaderboards
- `GET /api/leaderboard` - Get all leaderboards (cached, 5 min TTL)
- `GET /api/leaderboard/{dataset_id}` - Get specific leaderboard

### Metrics
- `GET /api/metrics` - Get all available metrics with documentation
- `GET /api/metrics/{metric_name}` - Get detailed metric information
- `GET /api/metrics/task/{task_type}` - Get metrics for a task type

### Admin
- `POST /api/admin/seed-data` - Load sample datasets
- `POST /api/admin/import-huggingface` - Import dataset from HuggingFace
- `GET /api/admin/cache-stats` - Get cache performance statistics
- `POST /api/admin/clear-cache` - Clear cached leaderboards

### Health
- `GET /health` - Health check endpoint

**Rate Limits:**
- General API: 100/minute
- Submissions: 10/minute
- Admin: 5/minute
- Leaderboards: 200/minute

See [docs/API.md](docs/API.md) for complete API reference.

---

## 💡 Using the Platform

### Via Web UI

1. **View Leaderboards**: Navigate to `http://localhost:3000`
   - Switch between list, grid (3×3), or single-card views
   - Filter by task type
   - Click on datasets to see full rankings

2. **Submit Predictions**: Go to "Submit Model"
   - Select a dataset
   - Download questions JSON or use "Get Questions & IDs"
   - Upload predictions JSON or paste directly
   - View example format and available classes
   - Track evaluation status in real-time

3. **View Submission History**: Check all past submissions with filters

4. **Explore Domains**: Browse domain-specific benchmarks (Finance, Multilingual, etc.)

5. **View Documentation**: Click "Documentation" in the footer for guides

### Via API

#### 1. Get Available Datasets

```bash
curl http://localhost:8000/api/datasets
```

#### 2. Get Questions for a Dataset

```bash
curl http://localhost:8000/api/datasets/{dataset_id}/questions > questions.json
```

#### 3. Submit Predictions

```bash
curl -X POST http://localhost:8000/api/submissions \
  -H "Content-Type: application/json" \
  -d '{
    "dataset_id": "uuid",
    "model_name": "My Model",
    "model_version": "2024-12-04",
    "predictions": [
      {"id": "1", "prediction": "business"},
      {"id": "2", "prediction": "sports"}
    ]
  }'
```

#### 4. Check Submission Status

```bash
curl http://localhost:8000/api/submissions/{submission_id}
```

#### 5. View Leaderboard

```bash
curl http://localhost:8000/api/leaderboard/{dataset_id}
```

### Python Example

```python
import requests

# Get datasets
datasets = requests.get("http://localhost:8000/api/datasets").json()
dataset_id = datasets[0]['id']

# Get questions
questions = requests.get(f"http://localhost:8000/api/datasets/{dataset_id}/questions").json()

# Prepare predictions (replace with your model's outputs)
predictions = [
    {"id": q["id"], "prediction": "your_model_output"}
    for q in questions["questions"]
]

# Submit
response = requests.post("http://localhost:8000/api/submissions", json={
    "dataset_id": dataset_id,
    "model_name": "My Model",
    "predictions": predictions
})

submission_id = response.json()["data"]["submission_id"]

# Poll for results
import time
while True:
    result = requests.get(f"http://localhost:8000/api/submissions/{submission_id}").json()
    if result["status"] == "completed":
        print(f"Score: {result['primary_score']}")
        print(f"All metrics: {result['detailed_scores']}")
        break
    time.sleep(2)
```

See [example_usage.py](example_usage.py) for a complete working example.

---

## 📊 Available Datasets

### General NLP
- AG News (text classification, 50 examples + 1000 HF)
- SST-2 (sentiment analysis, 50 examples + 872 HF)
- IMDB (movie reviews, 50 examples)
- SQuAD (extractive QA, 50 examples + 1000 HF)
- TruthfulQA (truthfulness, 50 examples + 400 HF)
- MNLI (NLI, 2000 examples)
- QQP (paraphrase detection, 2000 examples)

### Finance
- Financial PhraseBank (sentiment, 50 examples + 800 HF)
- FiQA Opinion Mining (sentiment, 50 examples)
- Twitter Financial Sentiment (50 examples + 1000 HF)
- FinQA (numerical reasoning, 50 examples)
- Financial NER (entity recognition, 50 examples)
- WNUT17 (emerging entities, 1000 examples)

### Multilingual
- XNLI (cross-lingual NLI, 50 examples across 10 languages)
- MGSM (multilingual math, 50 examples across 10 languages)
- XCOPA (causal reasoning, 50 examples across 12 languages)
- XQUAD (multilingual QA, 50 examples across 11 languages)
- MultiNLI Cross-Lingual (50 examples across 6 languages)

### Science & Code
- Science QA (50 examples)
- Code Reasoning (50 examples)
- AI2 ARC Easy (778 examples)
- AI2 ARC Challenge (1172 examples)
- GSM8K (math word problems, 1319 examples)
- MBPP (Python problems, 257 examples)

### Safety & Alignment
- TruthfulQA (400 examples)
- RealToxicityPrompts (1000 examples)
- Civil Comments (toxicity classification, 1000 examples)

---

## 🏗️ Architecture

```
┌─────────────────┐
│  React Frontend │  (Vite + React + TailwindCSS)
│   Port 3000     │
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────┐
│ FastAPI Backend │  (Python 3.12)
│   Port 8000     │
│                 │
│ • Caching (TTL) │
│ • Rate Limiting │
│ • Structured    │
│   Logging       │
└────────┬────────┘
         │
    ┌────┴────┬──────────┬──────────┐
    ▼         ▼          ▼          ▼
┌────────┐ ┌──────┐ ┌────────┐ ┌──────────┐
│ SQLite │ │Cache │ │Task    │ │HuggingFace│
│   DB   │ │(5min)│ │Evaluators│ │ Importer │
└────────┘ └──────┘ └────────┘ └──────────┘
```

**Key Components:**
- **main.py** - FastAPI app with endpoints, caching, rate limiting
- **evaluators.py** - Task-specific evaluation logic (5 task types, 20+ metrics)
- **evaluation_service.py** - Async background evaluation
- **models.py** - SQLAlchemy database schema
- **schemas.py** - Pydantic validation
- **cache.py** - TTL caching layer
- **rate_limiter.py** - Per-IP rate limiting
- **logger.py** - Structured JSON logging
- **hf_importer.py** - HuggingFace dataset importer
- **metrics_info.py** - Comprehensive metrics catalog

**Frontend Structure:**
- **pages/** - Home, Submit, Docs, DomainBenchmarks, SubmissionHistory, DatasetLeaderboard
- **components/** - LeaderboardCard, SubmissionForm, DetailedMetrics, MetricInfoModal, ModelInsights, LanguageBreakdown
- **services/api.js** - Backend API client

---

## 🎯 Frontend Features

### Multiple View Modes
- **List View**: Full-width stacked leaderboards
- **3×3 Grid View**: Compact cards showing top 3 models
- **Single-Card View**: One leaderboard at a time with navigation

### Rich Leaderboard Display
- Medal badges for top 3 ranks (🥇🥈🥉)
- Score visualization bars
- Domain-specific icons and gradient headers
- Model comparison (select up to 3 models for side-by-side metrics)
- Click any model to see detailed insights and per-language breakdowns

### Submission Workflow
- Dataset selector with task type and metric info
- **Format examples** showing input/output structure
- **Available classes** displayed for classification tasks
- JSON upload or paste for batch predictions
- Auto-filled dates (editable)
- Real-time evaluation status with detailed metrics
- Spam prevention (button disabled until form changes)

### Navigation
- Submission history with filters
- Full leaderboard pages for each dataset
- Domain-specific views (Finance, Multilingual, Science, etc.)
- In-app documentation with tabs

---

## 📊 Evaluation Metrics

### Text Classification
- Accuracy, Precision (macro), Recall (macro), F1 (macro)
- Micro Precision, Micro Recall, Micro F1
- Balanced Accuracy, Cohen's Kappa, Matthews Correlation Coefficient

### Named Entity Recognition
- Strict: Precision, Recall, F1 (exact span + type match)
- Partial: Precision, Recall, F1 (overlapping span + correct type)
- True Positives, False Positives, False Negatives counts

### Question Answering (Document & Line)
- Exact Match, Token F1, BLEU
- Answer Length Ratio

### Retrieval
- Retrieval Accuracy, Mean Reciprocal Rank (MRR)
- Precision@1/3/5, Recall@1/3/5
- NDCG (Normalized Discounted Cumulative Gain)

### Multilingual (cross-lingual tasks)
- Per-Language Accuracy / F1
- Cross-Lingual Transfer Score
- Language Variance

**All metrics include:**
- Mathematical formulas
- Interpretation guides
- Use cases and limitations
- Interactive explanations in the UI

See [metrics_info.py](metrics_info.py) for complete metric catalog.

---

## 🌐 Production Deployment

### Recommended Stack
- **Backend**: Railway, Render, Fly.io, AWS Elastic Beanstalk
- **Frontend**: Vercel, Netlify, Cloudflare Pages
- **Database**: PostgreSQL (Supabase, Neon, AWS RDS)
- **Caching**: Redis (for distributed caching across instances)
- **Monitoring**: Datadog, CloudWatch, Prometheus + Grafana

### Environment Variables (Production)

**Backend:**
```bash
DATABASE_URL=postgresql://user:password@host:5432/leaderboard
LOG_LEVEL=INFO
REDIS_URL=redis://localhost:6379/0
```

**Frontend:**
```bash
VITE_API_URL=https://api.yourleaderboard.com
```

### Production Checklist
- [ ] Switch to PostgreSQL database
- [ ] Set up Redis for distributed caching
- [ ] Configure CORS to specific origins
- [ ] Add authentication/API keys
- [ ] Enable HTTPS
- [ ] Set up monitoring and alerting
- [ ] Configure backup strategy
- [ ] Set up CDN for frontend assets

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed deployment guide.

---

## 🎯 Project Status

### ✅ Complete Features

**Backend:**
- ✅ 5 task types with comprehensive evaluators
- ✅ 20+ evaluation metrics with full documentation
- ✅ 30+ benchmark datasets across 6 domains
- ✅ HuggingFace bulk import system
- ✅ Caching layer (5-minute TTL)
- ✅ Rate limiting (per-IP)
- ✅ Structured JSON logging
- ✅ Complete test suite (>80% coverage)
- ✅ GitHub Actions CI/CD
- ✅ Admin endpoints for cache management

**Frontend:**
- ✅ Premium UI with dark theme
- ✅ Multiple layout modes (list/grid/single)
- ✅ Model comparison (up to 3 models)
- ✅ Submission form with JSON upload/paste
- ✅ Format examples and available classes
- ✅ Real-time evaluation tracking
- ✅ Submission history with filters
- ✅ Per-language metric breakdowns
- ✅ Model insights and tuning suggestions
- ✅ Metric explanation modals
- ✅ In-app documentation
- ✅ Responsive design

**Documentation:**
- ✅ Complete API reference
- ✅ Architecture overview
- ✅ Contributing guidelines
- ✅ README with usage examples

### 🔮 Future Enhancements

**Infrastructure:**
- [ ] Authentication and API keys
- [ ] PostgreSQL migration
- [ ] Redis for distributed caching
- [ ] Celery for distributed evaluation workers
- [ ] WebSocket for real-time updates

**Features:**
- [ ] Custom metric definitions
- [ ] Ensemble evaluation
- [ ] Model versioning and history
- [ ] Leaderboard snapshots (historical rankings)
- [ ] Webhook notifications
- [ ] A/B testing framework

**Datasets:**
- [ ] More summarization benchmarks
- [ ] Dialogue evaluation tasks
- [ ] Additional multilingual datasets
- [ ] Domain-specific reasoning tasks

---

## 📹 Reference Materials

Learn more about the vision:
- **Languages and Model Leaderboard**: [Watch](https://www.youtube.com/watch?v=JZ8foxMtct8)
- **Model Leaderboard**: [Watch](https://www.youtube.com/watch?v=e8V6MfPqAaE)
- **AI Day Summit Talk**: [Watch (min 20)](https://www.youtube.com/watch?v=eR_fnV0DyHE)

---

## 🧪 Testing

The project includes comprehensive test coverage:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=. --cov-report=html

# Run specific test suites
pytest tests/test_evaluators_by_task.py      # Unit tests for evaluators
pytest tests/test_submission_pipeline.py     # End-to-end submission tests
pytest tests/test_internal_evaluations.py    # Baseline consistency
pytest tests/test_hf_import.py               # HuggingFace import
pytest tests/test_metrics_api.py             # Metrics endpoints
```

**GitHub Actions CI/CD:**
- Runs on every push and PR
- Backend tests + frontend build
- Nightly full test suite
- Deployment workflow (on version tags)

## 🤝 Contributing

We welcome contributions! Please see [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for:
- Development setup
- Code style guidelines
- Testing requirements
- Pull request process

**Ways to Contribute:**
- Add new datasets or domains
- Implement additional metrics
- Improve documentation
- Fix bugs and improve performance
- Enhance UI/UX

## 📄 License

[Add your license here]

## 📞 Contact

**Project Lead**: Natan Vidra – nvidra@anote.ai
**Website**: [https://anote.ai](https://anote.ai)
**GitHub**: [github.com/nv78/Autonomous-Intelligence](https://github.com/nv78/Autonomous-Intelligence/)

## 🙏 Acknowledgments

Built with:
- FastAPI, SQLAlchemy, Pydantic
- React, Vite, TailwindCSS
- HuggingFace Datasets
- pytest, GitHub Actions

Inspired by:
- [Papers with Code](https://paperswithcode.com/)
- [HuggingFace Open LLM Leaderboard](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard)
- [HELM](https://crfm.stanford.edu/helm/)

---

**⭐ Star this repo if you find it useful!**
