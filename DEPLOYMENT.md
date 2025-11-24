# Deployment Guide - Google Cloud Run

This guide walks you through deploying the Wine Quality MLOps application to Google Cloud Run.

## Prerequisites

1. **Google Cloud Account** with billing enabled
2. **gcloud CLI** installed ([Install Guide](https://cloud.google.com/sdk/docs/install))
3. **Docker** installed locally
4. **Weights & Biases** account and API key

## Step 1: Setup Google Cloud Project

```bash
# Login to Google Cloud
gcloud auth login

# Create a new project (or use existing)
gcloud projects create wine-quality-mlops --name="Wine Quality MLOps"

# Set the project
gcloud config set project wine-quality-mlops

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

## Step 2: Train and Save Model

```bash
# Login to W&B
wandb login

# Train the model
python src/train.py --project_name wine-quality-mlops
```

This will save the model to `models/` and log it to W&B.

## Step 3: Build and Push Docker Images

### Build API Image
```bash
# Build the API image
gcloud builds submit --tag gcr.io/wine-quality-mlops/wine-quality-api -f Dockerfile.api

# Or build locally and push
docker build -f Dockerfile.api -t gcr.io/wine-quality-mlops/wine-quality-api .
docker push gcr.io/wine-quality-mlops/wine-quality-api
```

### Build Frontend Image
```bash
# Build the frontend image
gcloud builds submit --tag gcr.io/wine-quality-mlops/wine-quality-frontend -f Dockerfile.frontend

# Or build locally and push
docker build -f Dockerfile.frontend -t gcr.io/wine-quality-mlops/wine-quality-frontend .
docker push gcr.io/wine-quality-mlops/wine-quality-frontend
```

## Step 4: Deploy API to Cloud Run

```bash
# Deploy the API
gcloud run deploy wine-quality-api \
  --image gcr.io/wine-quality-mlops/wine-quality-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 10 \
  --set-env-vars WANDB_API_KEY=your_wandb_api_key_here

# Get the API URL
API_URL=$(gcloud run services describe wine-quality-api --region us-central1 --format 'value(status.url)')
echo "API URL: $API_URL"
```

## Step 5: Deploy Frontend to Cloud Run

```bash
# Deploy the frontend with API URL
gcloud run deploy wine-quality-frontend \
  --image gcr.io/wine-quality-mlops/wine-quality-frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 10 \
  --set-env-vars API_URL=$API_URL

# Get the Frontend URL
FRONTEND_URL=$(gcloud run services describe wine-quality-frontend --region us-central1 --format 'value(status.url)')
echo "Frontend URL: $FRONTEND_URL"
```

## Step 6: Test Deployment

```bash
# Test API health
curl $API_URL/health

# Test prediction
curl -X POST $API_URL/predict \
  -H "Content-Type: application/json" \
  -d '{
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
  }'

# Open frontend in browser
echo "Visit: $FRONTEND_URL"
```

## Step 7: Setup GitHub Actions (CI/CD)

### Create Service Account

```bash
# Create service account
gcloud iam service-accounts create github-actions \
  --display-name "GitHub Actions"

# Grant permissions
gcloud projects add-iam-policy-binding wine-quality-mlops \
  --member serviceAccount:github-actions@wine-quality-mlops.iam.gserviceaccount.com \
  --role roles/run.admin

gcloud projects add-iam-policy-binding wine-quality-mlops \
  --member serviceAccount:github-actions@wine-quality-mlops.iam.gserviceaccount.com \
  --role roles/storage.admin

gcloud projects add-iam-policy-binding wine-quality-mlops \
  --member serviceAccount:github-actions@wine-quality-mlops.iam.gserviceaccount.com \
  --role roles/iam.serviceAccountUser

# Create key
gcloud iam service-accounts keys create key.json \
  --iam-account github-actions@wine-quality-mlops.iam.gserviceaccount.com
```

### Add GitHub Secrets

Go to your GitHub repository → Settings → Secrets and add:

1. **WANDB_API_KEY**: Your W&B API key
2. **GCP_PROJECT_ID**: `wine-quality-mlops`
3. **GCP_SA_KEY**: Contents of `key.json` file

### Push to GitHub

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

GitHub Actions will automatically:
1. Train the model
2. Run tests
3. Build Docker images
4. Deploy to Cloud Run

## Monitoring

### View Logs
```bash
# API logs
gcloud run services logs read wine-quality-api --region us-central1

# Frontend logs
gcloud run services logs read wine-quality-frontend --region us-central1
```

### View Metrics
```bash
# Open Cloud Console
gcloud run services describe wine-quality-api --region us-central1
```

Or visit: https://console.cloud.google.com/run

## Cost Optimization

### Set Budget Alerts
```bash
# Create budget alert
gcloud billing budgets create \
  --billing-account=YOUR_BILLING_ACCOUNT_ID \
  --display-name="Wine Quality MLOps Budget" \
  --budget-amount=10USD
```

### Reduce Costs
- Set `--min-instances 0` to scale to zero when idle
- Use `--memory 256Mi` if model is small
- Delete unused container images
- Use Cloud Run free tier (2M requests/month)

## Troubleshooting

### Cold Start Issues
```bash
# Set minimum instances to 1
gcloud run services update wine-quality-api \
  --region us-central1 \
  --min-instances 1
```

### Memory Issues
```bash
# Increase memory
gcloud run services update wine-quality-api \
  --region us-central1 \
  --memory 1Gi
```

### Model Not Loading
- Check W&B API key is set correctly
- Verify model exists in W&B project
- Check logs for errors

## Cleanup

```bash
# Delete services
gcloud run services delete wine-quality-api --region us-central1
gcloud run services delete wine-quality-frontend --region us-central1

# Delete images
gcloud container images delete gcr.io/wine-quality-mlops/wine-quality-api
gcloud container images delete gcr.io/wine-quality-mlops/wine-quality-frontend

# Delete project (optional)
gcloud projects delete wine-quality-mlops
```

## Next Steps

- Setup custom domain
- Add authentication
- Configure CDN
- Add monitoring alerts
- Implement A/B testing

---

For more information, see the [main README](README.md).
