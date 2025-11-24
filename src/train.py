import argparse
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import wandb
import joblib
import os

# Set random seed for reproducibility
SEED = 42

def load_data():
    # Using the Wine Quality dataset from UCI Machine Learning Repository
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
    print(f"Downloading data from {url}...")
    df = pd.read_csv(url, sep=';')
    return df

def train(args):
    # Initialize W&B run
    wandb.init(project=args.project_name, job_type="train")
    
    # Load data
    df = load_data()
    
    # Split data
    X = df.drop('quality', axis=1)
    y = df['quality']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=SEED)
    
    # Log data config
    wandb.config.update({
        "test_size": 0.2,
        "seed": SEED,
        "features": list(X.columns)
    })

    # Train model
    print("Training model...")
    model = RandomForestRegressor(
        n_estimators=args.n_estimators, 
        max_depth=args.max_depth, 
        random_state=SEED
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    preds = model.predict(X_test)
    mse = mean_squared_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    
    print(f"MSE: {mse}")
    print(f"R2: {r2}")
    
    # Log metrics
    wandb.log({"mse": mse, "r2": r2})
    
    # Save model locally
    os.makedirs("models", exist_ok=True)
    model_path = "models/wine_quality_model.pkl"
    joblib.dump(model, model_path)
    
    # Log model artifact to W&B
    artifact = wandb.Artifact(
        name="wine-quality-model",
        type="model",
        description="Random Forest model for wine quality prediction"
    )
    artifact.add_file(model_path)
    wandb.log_artifact(artifact)
    
    wandb.finish()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_name", type=str, default="wine-quality-mlops", help="W&B project name")
    parser.add_argument("--n_estimators", type=int, default=100, help="Number of trees in RF")
    parser.add_argument("--max_depth", type=int, default=10, help="Max depth of trees")
    
    args = parser.parse_args()
    train(args)
