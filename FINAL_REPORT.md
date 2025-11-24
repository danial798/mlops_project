# MLOps Pipeline - Final Report

**Project**: Wine Quality Prediction System  
**Author**: [Your Name]  
**Date**: November 2025  
**Course**: Atomcamp MLOps Capstone Project

---

## Executive Summary

This project implements a complete end-to-end MLOps pipeline for wine quality prediction. The system demonstrates industry best practices in machine learning deployment, including automated training, experiment tracking, model versioning, CI/CD automation, and production deployment on Google Cloud Run.

The pipeline successfully achieves:
- ✅ Fully automated training and deployment
- ✅ Reproducible experiments with version control
- ✅ Production-ready API with health monitoring
- ✅ User-friendly frontend interface
- ✅ Continuous integration and deployment

---

## 1. Problem Statement & Dataset

### Problem
Predict wine quality (0-10 scale) based on 11 physicochemical properties including acidity, pH, alcohol content, and sulfur dioxide levels.

### Dataset
- **Source**: UCI Machine Learning Repository - Wine Quality Dataset
- **Size**: ~1,600 samples
- **Type**: Tabular data (regression problem)
- **Features**: 11 numerical features
- **Target**: Quality score (0-10)

### Why This Dataset?
1. **CPU-Friendly**: Small dataset suitable for training without GPU
2. **Well-Structured**: Clean tabular data, minimal preprocessing needed
3. **Real-World Application**: Demonstrates practical ML use case
4. **Public Availability**: No authentication required, easy to reproduce

---

## 2. Pipeline Architecture & Design Decisions

### 2.1 Model Selection: Random Forest Regressor

**Choice**: scikit-learn Random Forest

**Justification**:
- ✅ **CPU Efficiency**: Trains in seconds on standard hardware
- ✅ **No Hyperparameter Tuning Required**: Works well with default parameters
- ✅ **Interpretability**: Feature importance available
- ✅ **Robustness**: Handles non-linear relationships well
- ✅ **Small Model Size**: ~1-5 MB, fast to load and serve

**Alternatives Considered**:
- ❌ **Deep Learning**: Overkill for tabular data, requires GPU
- ❌ **XGBoost**: Similar performance, but adds dependency complexity
- ❌ **Linear Regression**: Too simple, poor performance on this dataset

**Trade-offs**:
- ➕ Fast training and inference
- ➕ Easy to version and deploy
- ➖ Less accurate than ensemble of multiple models
- ➖ Limited scalability for very large datasets

---

### 2.2 Experiment Tracking: Weights & Biases

**Choice**: W&B for experiment tracking and model registry

**Justification**:
- ✅ **Unified Platform**: Combines experiment tracking, artifact storage, and model registry
- ✅ **Easy Integration**: Simple Python API, minimal code changes
- ✅ **Visualization**: Beautiful dashboards for metrics and comparisons
- ✅ **Model Versioning**: Automatic versioning with artifact system
- ✅ **Free Tier**: Sufficient for academic/personal projects

**Alternatives Considered**:
- ❌ **MLflow**: More complex setup, requires separate server
- ❌ **TensorBoard**: Limited to TensorFlow/PyTorch ecosystems
- ❌ **Manual Logging**: Not scalable, error-prone

**Trade-offs**:
- ➕ Comprehensive tracking with minimal setup
- ➕ Cloud-hosted, no infrastructure management
- ➖ Vendor lock-in (mitigated by export capabilities)
- ➖ Requires internet connection during training

---

### 2.3 Backend API: FastAPI

**Choice**: FastAPI for inference service

**Justification**:
- ✅ **Performance**: Async support, one of the fastest Python frameworks
- ✅ **Automatic Documentation**: OpenAPI/Swagger docs generated automatically
- ✅ **Type Safety**: Pydantic models for request/response validation
- ✅ **Modern Python**: Uses type hints, Python 3.9+ features
- ✅ **Easy Testing**: Built-in test client

**Alternatives Considered**:
- ❌ **Flask**: Slower, no async support, manual validation
- ❌ **Django**: Too heavy for simple API
- ❌ **Hugging Face Inference**: Limited to HF models

**Trade-offs**:
- ➕ Production-ready with minimal code
- ➕ Excellent developer experience
- ➖ Smaller ecosystem than Flask
- ➖ Learning curve for async programming

---

### 2.4 Frontend: Streamlit

**Choice**: Streamlit for user interface

**Justification**:
- ✅ **Rapid Development**: Build UI in pure Python, no HTML/CSS/JS
- ✅ **Interactive Widgets**: Built-in sliders, inputs, buttons
- ✅ **Easy Deployment**: Single command to run
- ✅ **Python-Native**: No context switching for ML engineers
- ✅ **Good for Demos**: Perfect for prototypes and MVPs

**Alternatives Considered**:
- ❌ **Gradio**: Similar to Streamlit, but less flexible
- ❌ **React/Next.js**: Requires frontend expertise, slower development
- ❌ **Dash**: More complex, steeper learning curve

**Trade-offs**:
- ➕ Fastest time-to-demo
- ➕ No frontend skills required
- ➖ Limited customization compared to React
- ➖ Full page reloads on interaction (mitigated with caching)

---

### 2.5 Orchestration: GitHub Actions

**Choice**: GitHub Actions for CI/CD

**Justification**:
- ✅ **Native Integration**: Built into GitHub, no external service
- ✅ **Free for Public Repos**: Generous free tier
- ✅ **YAML Configuration**: Easy to version control
- ✅ **Rich Ecosystem**: Thousands of pre-built actions
- ✅ **Secrets Management**: Secure environment variables

**Alternatives Considered**:
- ❌ **Jenkins**: Requires self-hosting, complex setup
- ❌ **CircleCI**: External service, limited free tier
- ❌ **Airflow**: Overkill for simple pipelines, requires infrastructure

**Trade-offs**:
- ➕ Zero infrastructure management
- ➕ Tight GitHub integration
- ➖ Limited to 2,000 minutes/month on free tier
- ➖ Less flexible than self-hosted solutions

---

### 2.6 Deployment: Google Cloud Run

**Choice**: Cloud Run for production deployment

**Justification**:
- ✅ **Serverless**: No server management, auto-scaling
- ✅ **Pay-Per-Use**: Only charged for actual requests
- ✅ **Container-Based**: Deploy any Dockerized app
- ✅ **Fast Cold Starts**: ~1-2 seconds for Python apps
- ✅ **HTTPS by Default**: Automatic SSL certificates
- ✅ **Generous Free Tier**: 2 million requests/month free

**Alternatives Considered**:
- ❌ **AWS Lambda**: 15-minute timeout limit, complex packaging
- ❌ **Heroku**: More expensive, less flexible
- ❌ **Kubernetes**: Overkill for simple app, high complexity
- ❌ **VM Instances**: Requires management, always-on costs

**Trade-offs**:
- ➕ Minimal operational overhead
- ➕ Automatic scaling (0 to N instances)
- ➖ Cold start latency (mitigated with min instances)
- ➖ Vendor lock-in (mitigated by Docker portability)

---

### 2.7 Containerization: Docker

**Choice**: Docker for containerization

**Justification**:
- ✅ **Reproducibility**: Identical environment everywhere
- ✅ **Isolation**: Dependencies don't conflict with host
- ✅ **Portability**: Run anywhere Docker is supported
- ✅ **Industry Standard**: Universal adoption
- ✅ **Cloud Native**: Required for Cloud Run, Kubernetes, etc.

**Alternatives Considered**:
- ❌ **Virtual Environments**: Not portable across OS
- ❌ **Conda**: Heavier, slower builds
- ❌ **Podman**: Less mature ecosystem

**Trade-offs**:
- ➕ Perfect reproducibility
- ➕ Easy local testing
- ➖ Image size overhead (~500 MB for Python apps)
- ➖ Build time overhead

---

## 3. Pipeline Workflow

### 3.1 Development Workflow

```
1. Developer pushes code to GitHub
2. GitHub Actions triggers
3. Environment setup (Python, dependencies)
4. Model training with W&B logging
5. Model saved to W&B Artifacts
6. Unit tests run
7. Docker images built
8. Images pushed to Google Container Registry
9. Services deployed to Cloud Run
10. Health checks verify deployment
```

### 3.2 Inference Workflow

```
1. User opens Streamlit frontend
2. User inputs wine properties
3. Frontend sends POST request to FastAPI
4. API loads model from W&B or local cache
5. Model makes prediction
6. API returns prediction
7. Frontend displays result
```

---

## 4. Reproducibility Strategy

### 4.1 Code Reproducibility
- **Git**: All code versioned in GitHub
- **Requirements.txt**: Pinned dependencies
- **Dockerfiles**: Exact environment specification
- **Seed Values**: Fixed random seeds (SEED=42)

### 4.2 Data Reproducibility
- **Public Dataset**: UCI repository (permanent URL)
- **No Preprocessing**: Raw data used directly
- **W&B Artifacts**: Dataset logged for each run

### 4.3 Model Reproducibility
- **W&B Model Registry**: All models versioned
- **Hyperparameters Logged**: Full config in W&B
- **Artifact Lineage**: Track which data produced which model

---

## 5. Scalability Considerations

### Current Scale
- **Dataset**: ~1,600 samples
- **Training Time**: ~5 seconds
- **Model Size**: ~2 MB
- **Inference Latency**: ~50 ms

### Scaling Strategy

**If Dataset Grows (10x - 100x)**:
- ✅ Random Forest still viable up to ~1M samples
- ✅ Consider XGBoost for better performance
- ✅ Add data versioning with DVC or W&B Artifacts

**If Traffic Grows (1000x requests)**:
- ✅ Cloud Run auto-scales to handle load
- ✅ Add caching layer (Redis) for frequent predictions
- ✅ Consider batch prediction API

**If Model Complexity Grows**:
- ✅ Switch to GPU-based training (Cloud AI Platform)
- ✅ Add model optimization (quantization, pruning)
- ✅ Consider model serving platforms (TensorFlow Serving, Triton)

---

## 6. Cost Analysis

### Development Costs
- **W&B**: Free tier (100 GB storage)
- **GitHub Actions**: Free for public repos (2,000 min/month)
- **Development Time**: ~8-12 hours

### Production Costs (Monthly)
- **Cloud Run API**: $0 (within free tier for low traffic)
- **Cloud Run Frontend**: $0 (within free tier)
- **Container Registry**: ~$0.10/GB/month
- **Total**: **~$1-5/month** for low-traffic demo

### Cost Optimization
- ✅ Use Cloud Run min instances = 0 (scale to zero)
- ✅ Optimize Docker images (multi-stage builds)
- ✅ Cache W&B artifacts to reduce downloads

---

## 7. Security Considerations

### Implemented
- ✅ **Secrets Management**: GitHub Secrets for API keys
- ✅ **HTTPS**: Automatic SSL on Cloud Run
- ✅ **Input Validation**: Pydantic schemas prevent injection
- ✅ **Dependency Scanning**: GitHub Dependabot enabled

### Future Improvements
- 🔲 Add authentication (API keys, OAuth)
- 🔲 Rate limiting to prevent abuse
- 🔲 Input sanitization for XSS prevention
- 🔲 Model access control (private W&B projects)

---

## 8. Monitoring & Observability

### Current Monitoring
- ✅ **Health Checks**: `/health` endpoint
- ✅ **Cloud Run Metrics**: Request count, latency, errors
- ✅ **W&B Logging**: Training metrics, model versions

### Future Improvements
- 🔲 **Prediction Logging**: Log all predictions for analysis
- 🔲 **Model Drift Detection**: Monitor input distribution
- 🔲 **Performance Alerts**: Slack/email on errors
- 🔲 **A/B Testing**: Compare model versions in production

---

## 9. Lessons Learned

### What Went Well
1. **FastAPI + Streamlit**: Excellent combo for rapid prototyping
2. **W&B Integration**: Seamless experiment tracking
3. **Docker Compose**: Made local testing trivial
4. **GitHub Actions**: Automated everything with minimal config

### Challenges Faced
1. **Cold Starts**: Cloud Run cold starts add latency (solved with min instances)
2. **Model Download**: W&B artifact download slow on first run (solved with caching)
3. **Docker Image Size**: Initial images were 1+ GB (solved with slim base images)

### What I'd Do Differently
1. **Add Model Monitoring**: Should have included drift detection from start
2. **Use DVC**: For larger datasets, DVC might be better than W&B Artifacts
3. **Add A/B Testing**: Would allow safe model rollouts

---

## 10. Future Enhancements

### Short-Term (1-2 weeks)
- [ ] Add model performance monitoring dashboard
- [ ] Implement prediction caching
- [ ] Add more comprehensive tests (integration, load testing)
- [ ] Create Postman collection for API

### Medium-Term (1-2 months)
- [ ] Add model retraining schedule (weekly/monthly)
- [ ] Implement A/B testing framework
- [ ] Add user authentication
- [ ] Create mobile-responsive frontend

### Long-Term (3-6 months)
- [ ] Multi-model ensemble
- [ ] Real-time model updates
- [ ] Advanced feature engineering pipeline
- [ ] Kubernetes deployment for high-scale

---

## 11. Conclusion

This project successfully demonstrates a production-ready MLOps pipeline with:

✅ **Reproducibility**: All code, data, and models versioned  
✅ **Automation**: Full CI/CD from commit to deployment  
✅ **Scalability**: Cloud-native architecture ready to scale  
✅ **Maintainability**: Clear structure, comprehensive docs  
✅ **Cost-Efficiency**: Runs on free/low-cost infrastructure  

The pipeline design prioritizes **simplicity and pragmatism** over complexity. Every tool choice was made to minimize operational overhead while maintaining production-quality standards.

### Key Takeaways

1. **Start Simple**: Don't over-engineer. A simple pipeline that works is better than a complex one that doesn't.
2. **Automate Early**: CI/CD from day one prevents technical debt.
3. **Use Managed Services**: Serverless platforms eliminate 90% of DevOps work.
4. **Track Everything**: Experiment tracking pays dividends in debugging and reproducibility.
5. **Think in Systems**: ML is not just models—it's data, code, infrastructure, and monitoring.

---

## 12. References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Weights & Biases Documentation](https://docs.wandb.ai/)
- [Google Cloud Run Documentation](https://cloud.google.com/run/docs)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [UCI Wine Quality Dataset](https://archive.ics.uci.edu/ml/datasets/wine+quality)

---

**Author**: [Your Name]  
**Contact**: [your.email@example.com]  
**GitHub**: [github.com/yourusername/wine-quality-mlops]  
**W&B Project**: [wandb.ai/yourusername/wine-quality-mlops]
