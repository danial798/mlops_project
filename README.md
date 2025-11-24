# Wine Quality Prediction - End-to-End MLOps Pipeline

[![MLOps Pipeline](https://github.com/danial798/mlops_project/actions/workflows/mlops-pipeline.yml/badge.svg)](https://github.com/danial798/mlops_project/actions)

An end-to-end MLOps pipeline for predicting wine quality using machine learning. This project demonstrates best practices in ML deployment, including version control, experiment tracking, CI/CD automation, and production deployment.

## 🎯 Project Overview

This project predicts wine quality (0-10 scale) based on physicochemical properties using a Random Forest regression model. The focus is on building a **reproducible, automated, and production-ready** ML system.

### Key Features

- ✅ **Automated Training Pipeline** with experiment tracking
- ✅ **Model Versioning** using Weights & Biases
- ✅ **CI/CD Automation** with GitHub Actions
- ✅ **RESTful API** built with FastAPI
- ✅ **Interactive Frontend** using Streamlit
- ✅ **Containerized Deployment** with Docker
- ✅ **Cloud Deployment** on Google Cloud Run

## 🏗️ Architecture

```
┌─────────────────┐
│  Data Source    │
│  (UCI Wine)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│  Training       │─────▶│  Weights & Biases│
│  Pipeline       │      │  (Experiment     │
│  (train.py)     │      │   Tracking)      │
└────────┬────────┘      └──────────────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│  Model Registry │─────▶│  GitHub Actions  │
│  (W&B Artifacts)│      │  (CI/CD)         │
└────────┬────────┘      └─────────┬────────┘
         │                         │
         ▼                         ▼
┌─────────────────┐      ┌──────────────────┐
│  FastAPI        │      │  Google Cloud    │
│  Backend        │─────▶│  Run Deployment  │
└────────┬────────┘      └──────────────────┘
         │
         ▼
┌─────────────────┐
│  Streamlit      │
│  Frontend       │
└─────────────────┘
```

## 📁 Project Structure

```
.
├── .github/
│   └── workflows/
│       └── mlops-pipeline.yml    # CI/CD workflow
├── src/
│   ├── train.py                  # Training script
│   ├── api/
│   │   ├── main.py              # FastAPI application
│   │   └── schemas.py           # Pydantic models
│   └── frontend/
│       └── app.py               # Streamlit app
├── tests/
│   └── test_api.py              # API tests
├── Dockerfile.api               # API container
├── Dockerfile.frontend          # Frontend container
├── docker-compose.yml           # Local development
├── requirements.txt             # Python dependencies
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Docker & Docker Compose
- Weights & Biases account (free tier works)
- Google Cloud account (for deployment)

### 1. Clone the Repository

```bash
git clone https://github.com/danial798/mlops_project.git
cd mlops_project
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Train the Model

```bash
# Login to W&B first
wandb login

# Train the model
python src/train.py --project_name wine-quality-mlops --n_estimators 100 --max_depth 10
```

This will:
- Download the wine quality dataset
- Train a Random Forest model
- Log metrics to W&B
- Save the model to `models/` and W&B Artifacts

### 4. Run Locally with Docker Compose

```bash
# Set your W&B API key
export WANDB_API_KEY=your_wandb_api_key

# Start services
docker-compose up --build
```

Access the application:
- **Frontend**: http://localhost:8501
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 5. Run Tests

```bash
pytest tests/ -v
```

## 🔧 Configuration

### Environment Variables

- `WANDB_API_KEY`: Your Weights & Biases API key
- `API_URL`: Backend API URL (for frontend)
- `GCP_PROJECT_ID`: Google Cloud project ID (for deployment)
- `GCP_SA_KEY`: Google Cloud service account key (for deployment)

### GitHub Secrets

For CI/CD to work, add these secrets to your GitHub repository:

1. `WANDB_API_KEY`: Your W&B API key
2. `GCP_PROJECT_ID`: Your GCP project ID
3. `GCP_SA_KEY`: Your GCP service account JSON key

## 📊 Experiment Tracking

All experiments are tracked in Weights & Biases:

- **Metrics**: MSE, R² score
- **Hyperparameters**: n_estimators, max_depth, test_size
- **Artifacts**: Trained models with versioning

View your experiments at: https://wandb.ai/your-username/wine-quality-mlops

## 🚢 Deployment

### Google Cloud Run

The GitHub Actions workflow automatically deploys to Cloud Run on push to `main`:

1. **Train**: Trains model and logs to W&B
2. **Test**: Runs unit tests
3. **Build**: Builds Docker images
4. **Deploy**: Deploys to Cloud Run

Manual deployment:

```bash
# Build and push API
gcloud builds submit --tag gcr.io/PROJECT_ID/wine-quality-api -f Dockerfile.api

# Deploy API
gcloud run deploy wine-quality-api \
  --image gcr.io/PROJECT_ID/wine-quality-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# Build and push Frontend
gcloud builds submit --tag gcr.io/PROJECT_ID/wine-quality-frontend -f Dockerfile.frontend

# Deploy Frontend
gcloud run deploy wine-quality-frontend \
  --image gcr.io/PROJECT_ID/wine-quality-frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars API_URL=https://your-api-url.run.app
```

## 🧪 API Endpoints

### Health Check
```bash
GET /health
```

### Predict Wine Quality
```bash
POST /predict
Content-Type: application/json

{
  "fixed_acidity": 7.4,
  "volatile_acidity": 0.7,
  "citric_acid": 0.0,
  "residual_sugar": 1.9,
  "chlorides": 0.076,
  "free_sulfur_dioxide": 11.0,
  "total_sulfur_dioxide": 34.0,
  "density": 0.9978,
  "pH": 3.51,
  "sulphates": 0.56,
  "alcohol": 9.4
}
```

## 🛠️ Technology Stack

| Component | Technology | Justification |
|-----------|-----------|---------------|
| **ML Framework** | scikit-learn | Lightweight, CPU-friendly, perfect for tabular data |
| **Experiment Tracking** | Weights & Biases | Comprehensive tracking, model registry, artifact versioning |
| **Backend API** | FastAPI | High performance, automatic API docs, type validation |
| **Frontend** | Streamlit | Rapid prototyping, Python-native, easy deployment |
| **Containerization** | Docker | Reproducibility, environment isolation |
| **Orchestration** | GitHub Actions | Native GitHub integration, free for public repos |
| **Deployment** | Google Cloud Run | Serverless, auto-scaling, pay-per-use |
| **Version Control** | Git/GitHub | Industry standard, integrates with CI/CD |

## 📈 Model Performance

The Random Forest model achieves:
- **MSE**: ~0.4-0.5 (on test set)
- **R² Score**: ~0.35-0.45

*Note: Wine quality prediction is inherently challenging due to subjective ratings.*

## 🔄 CI/CD Pipeline

The automated pipeline triggers on every push to `main`:

1. **Code Checkout**: Pulls latest code
2. **Environment Setup**: Installs Python and dependencies
3. **Model Training**: Trains model and logs to W&B
4. **Testing**: Runs unit tests
5. **Build**: Creates Docker images
6. **Deploy**: Deploys to Cloud Run
7. **Notification**: Updates deployment status

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👥 Authors

- Your Name - [GitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- Dataset: [UCI Machine Learning Repository - Wine Quality](https://archive.ics.uci.edu/ml/datasets/wine+quality)
- MLOps Course: Atomcamp MLOps Training

## 📞 Support

For questions or issues, please open an issue on GitHub.

---

**Live Demo**: [Your Cloud Run URL]

**W&B Project**: [Your W&B Project URL]
