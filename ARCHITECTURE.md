# MLOps Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         WINE QUALITY MLOPS PIPELINE                          │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────┐
│   UCI Wine Quality   │
│   Dataset (Public)   │
└──────────┬───────────┘
           │
           │ Download
           ▼
┌──────────────────────┐      ┌────────────────────────────────────────┐
│  Training Pipeline   │─────▶│     Weights & Biases (W&B)            │
│   (src/train.py)     │      │  ┌──────────────────────────────────┐ │
│                      │      │  │  Experiment Tracking             │ │
│  • Load Data         │      │  │  • Metrics (MSE, R²)             │ │
│  • Train RF Model    │      │  │  • Hyperparameters               │ │
│  • Evaluate          │      │  │  • Training Logs                 │ │
│  • Save Model        │      │  └──────────────────────────────────┘ │
└──────────┬───────────┘      │  ┌──────────────────────────────────┐ │
           │                  │  │  Model Registry                  │ │
           │                  │  │  • Model Artifacts               │ │
           │                  │  │  • Version Control               │ │
           │                  │  │  • Model Lineage                 │ │
           │                  │  └──────────────────────────────────┘ │
           │                  └────────────────────────────────────────┘
           │
           │ Trigger
           ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                         GITHUB ACTIONS (CI/CD)                                │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────────────────┐ │
│  │   Train    │─▶│    Test    │─▶│   Build    │─▶│       Deploy           │ │
│  │   Model    │  │   (pytest) │  │   Docker   │  │   (Cloud Run)          │ │
│  └────────────┘  └────────────┘  └────────────┘  └────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────┘
           │
           │ Build & Push
           ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                        DOCKER CONTAINERS                                      │
│  ┌─────────────────────────────────┐  ┌─────────────────────────────────┐   │
│  │      API Container              │  │    Frontend Container           │   │
│  │  ┌───────────────────────────┐  │  │  ┌───────────────────────────┐  │   │
│  │  │  FastAPI Application      │  │  │  │  Streamlit Application    │  │   │
│  │  │  • Load Model from W&B    │  │  │  │  • User Input Form        │  │   │
│  │  │  • /health endpoint       │  │  │  │  • API Client             │  │   │
│  │  │  • /predict endpoint      │  │  │  │  • Result Display         │  │   │
│  │  │  • Pydantic Validation    │  │  │  │  • Styled UI              │  │   │
│  │  └───────────────────────────┘  │  │  └───────────────────────────┘  │   │
│  │         Port: 8000               │  │         Port: 8501              │   │
│  └─────────────────────────────────┘  └─────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────────┘
           │                                          │
           │ Deploy                                   │ Deploy
           ▼                                          ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                      GOOGLE CLOUD RUN (Production)                            │
│  ┌─────────────────────────────────┐  ┌─────────────────────────────────┐   │
│  │   wine-quality-api              │  │   wine-quality-frontend         │   │
│  │   • Auto-scaling (0-10)         │  │   • Auto-scaling (0-10)         │   │
│  │   • HTTPS enabled               │  │   • HTTPS enabled               │   │
│  │   • Health monitoring           │  │   • Connected to API            │   │
│  │   • 512 MB RAM                  │  │   • 512 MB RAM                  │   │
│  └─────────────────────────────────┘  └─────────────────────────────────┘   │
│         https://api-xxx.run.app            https://frontend-xxx.run.app      │
└──────────────────────────────────────────────────────────────────────────────┘
                                           │
                                           │ Access
                                           ▼
                                    ┌──────────────┐
                                    │  End Users   │
                                    │  (Browser)   │
                                    └──────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                            DATA FLOW                                         │
└─────────────────────────────────────────────────────────────────────────────┘

Training Flow:
  Data → Train → W&B → GitHub Actions → Docker → Cloud Run

Inference Flow:
  User → Frontend → API → Model → Prediction → Frontend → User

Version Control:
  Code: GitHub
  Data: UCI (public URL)
  Models: W&B Artifacts
  Experiments: W&B Tracking

Automation:
  Trigger: Git push to main
  Actions: Train → Test → Build → Deploy
  Result: Updated production deployment
```

## Key Components

### 1. Data Layer
- **Source**: UCI Wine Quality Dataset
- **Storage**: Downloaded on-demand
- **Versioning**: Logged as W&B artifact

### 2. Training Layer
- **Framework**: scikit-learn
- **Orchestration**: GitHub Actions
- **Tracking**: Weights & Biases
- **Output**: Trained model artifact

### 3. Model Registry
- **Platform**: W&B Artifacts
- **Versioning**: Automatic (v0, v1, v2...)
- **Metadata**: Metrics, hyperparameters, lineage

### 4. Serving Layer
- **Backend**: FastAPI (REST API)
- **Frontend**: Streamlit (Web UI)
- **Protocol**: HTTP/JSON

### 5. Deployment Layer
- **Platform**: Google Cloud Run
- **Containerization**: Docker
- **Scaling**: Automatic (0-10 instances)
- **CI/CD**: GitHub Actions

## Workflow Sequence

1. **Developer pushes code** → GitHub
2. **GitHub Actions triggers** → Automated pipeline
3. **Model trains** → Logs to W&B
4. **Tests run** → Validates functionality
5. **Docker images build** → API + Frontend
6. **Images push** → Google Container Registry
7. **Services deploy** → Cloud Run
8. **Health checks pass** → Production ready
9. **Users access** → Public URL

## Technology Choices

| Layer | Technology | Why? |
|-------|-----------|------|
| ML | scikit-learn | CPU-friendly, fast training |
| Tracking | W&B | Best-in-class experiment tracking |
| API | FastAPI | High performance, auto docs |
| Frontend | Streamlit | Rapid prototyping |
| CI/CD | GitHub Actions | Native GitHub integration |
| Deployment | Cloud Run | Serverless, auto-scaling |
| Containers | Docker | Reproducibility |

---

For detailed documentation, see [README.md](README.md)
