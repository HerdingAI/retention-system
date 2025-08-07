"""
Train and serialize the student retention prediction model.
Usage:
    python scripts/train_model.py --output simple_model.pkl
"""
import argparse
import pickle
from synthetic_data_generator import generate_synthetic_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

def train_and_save(output_path, random_state=42):
    # Generate synthetic data
    df = generate_synthetic_data(n_samples=5000, random_state=random_state)
    X = df.drop(columns=['dropout'])
    y = df['dropout']

    # Split into train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=random_state
    )

    # Define and train model
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=8,
        random_state=random_state
    )
    model.fit(X_train, y_train)

    # Evaluate
    preds = model.predict(X_test)
    probas = model.predict_proba(X_test)[:,1]
    print("Model Evaluation:")
    print(f"Accuracy: {accuracy_score(y_test, preds):.4f}")
    print(classification_report(y_test, preds))

    # Save model
    with open(output_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"Model saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train retention prediction model")
    parser.add_argument(
        '--output', '-o', type=str, default='simple_model.pkl',
        help='Output path for the trained model pickle'
    )
    args = parser.parse_args()
    train_and_save(args.output)
