#!/usr/bin/env python3
"""
Evaluate the trained student retention prediction model on synthetic data.

Usage:
    python scripts/evaluate_model.py --model simple_model.pkl --n-samples 2000
"""
import argparse
import pickle
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score

from scripts.synthetic_data_generator import generate_synthetic_data


def evaluate_model(model_path: str, n_samples: int, random_state: int):
    """Load model and evaluate on synthetic data"""
    print(f"🔎 Generating {n_samples} synthetic samples...")
    df = generate_synthetic_data(n_samples=n_samples, random_state=random_state)
    X = df.drop(columns=['dropout'])
    y_true = df['dropout']

    print(f"📂 Loading model from {model_path}...")
    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    print("🚀 Running predictions...")
    y_pred = model.predict(X)
    y_proba = None
    if hasattr(model, 'predict_proba'):
        try:
            y_proba = model.predict_proba(X)[:, 1]
        except Exception:
            pass

    # Metrics
    acc = accuracy_score(y_true, y_pred)
    print(f"✅ Accuracy: {acc:.4f}")
    
    print("\n📈 Classification Report:")
    print(classification_report(y_true, y_pred))

    if y_proba is not None:
        auc = roc_auc_score(y_true, y_proba)
        print(f"✅ ROC AUC Score: {auc:.4f}")
    else:
        print("⚠️  Model does not support probability estimates; skipping ROC AUC.")


def main():
    parser = argparse.ArgumentParser(description="Evaluate student retention model")
    parser.add_argument('-m', '--model', type=str, default='simple_model.pkl', help='Path to trained model pickle')
    parser.add_argument('-n', '--n-samples', type=int, default=1000, help='Number of synthetic samples')
    parser.add_argument('-r', '--random-state', type=int, default=42, help='Random state for data generation')

    args = parser.parse_args()
    evaluate_model(args.model, args.n_samples, args.random_state)


if __name__ == '__main__':
    main()
