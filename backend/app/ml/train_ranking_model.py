"""
Trains a logistic regression model on manually-labeled match feedback
to learn feature weights, replacing the hardcoded 0.35/0.45/0.20 formula.

Run this after collecting at least ~15-20 labeled examples via /feedback.
Re-run any time you add more labels to re-tune the weights.
"""
import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

from app.core.database import SessionLocal
from app.models.feedback import MatchFeedback
from app.services.feature_engineering import FEATURE_ORDER

MODEL_PATH = "app/ml/ranking_model.joblib"


def load_training_data():
    db = SessionLocal()
    rows = db.query(MatchFeedback).all()
    db.close()

    X, y = [], []
    for row in rows:
        X.append([row.semantic_similarity, row.skill_overlap, row.experience_alignment])
        y.append(row.label)

    return np.array(X), np.array(y)


def train_model():
    X, y = load_training_data()

    if len(X) < 10:
        print(f"Only {len(X)} labeled examples found. Collect at least 10-15 via /feedback before training.")
        return

    if len(set(y.tolist())) < 2:
        print("Need both positive (1) and negative (0) labels to train. Currently only one class present.")
        return

    if len(X) >= 20:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    else:
        X_train, y_train = X, y
        X_test, y_test = X, y

    model = LogisticRegression()
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    print(f"Trained on {len(X_train)} examples.")
    print(f"Accuracy on {'held-out' if len(X) >= 20 else 'training'} set: {acc:.3f}")
    print(classification_report(y_test, preds, zero_division=0))

    coefficients = dict(zip(FEATURE_ORDER, model.coef_[0]))
    print("\nLearned feature weights (coefficients):")
    for feat, coef in coefficients.items():
        print(f"  {feat}: {coef:.4f}")

    import os
    os.makedirs("app/ml", exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"\nModel saved to {MODEL_PATH}")


if __name__ == "__main__":
    train_model()
