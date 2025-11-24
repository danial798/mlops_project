from fastapi import FastAPI, HTTPException
from .schemas import WineInput, PredictionOutput
import joblib
import pandas as pd
import wandb
import os

app = FastAPI(title="Wine Quality Prediction API")

model = None

def load_model():
    global model
    model_path = "models/wine_quality_model.pkl"
    
    # Try to load from W&B if API key is available and file doesn't exist or we want latest
    if os.getenv("WANDB_API_KEY"):
        try:
            print("Attempting to download model from W&B...")
            run = wandb.init(project="wine-quality-mlops", job_type="inference", resume="allow", anonymous="allow")
            artifact = run.use_artifact('wine-quality-model:latest', type='model')
            artifact_dir = artifact.download()
            model_path = os.path.join(artifact_dir, "wine_quality_model.pkl")
            print(f"Model downloaded to {model_path}")
            wandb.finish()
        except Exception as e:
            print(f"Failed to download from W&B: {e}. Falling back to local.")
    
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        print("Model loaded successfully.")
    else:
        print("Model file not found. API will not work correctly until model is trained.")

@app.on_event("startup")
async def startup_event():
    load_model()

@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/predict", response_model=PredictionOutput)
def predict(input_data: WineInput):
    if not model:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Convert input to DataFrame (to match training format)
    # Note: Pydantic fields match the column names expected by the model (snake_case)
    data = pd.DataFrame([input_data.dict()])
    
    prediction = model.predict(data)
    return {"quality_prediction": float(prediction[0])}
