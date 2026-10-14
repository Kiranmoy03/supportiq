"""Model creation and inference helpers, independent of the UI."""

from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


def build_pipeline() -> Pipeline:
    """Use a reproducible, interpretable baseline for short text classification."""
    return Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    ngram_range=(1, 2),
                    sublinear_tf=True,
                    strip_accents="unicode",
                    max_features=20_000,
                ),
            ),
            ("classifier", LogisticRegression(max_iter=1_000, C=3.0, random_state=42)),
        ]
    )


def load_model(path: str | Path) -> Pipeline:
    """Load only the trusted model artifact shipped with this project."""
    return joblib.load(Path(path))  # noqa: S301 - trusted local artifact only


def predict(model: Pipeline, text: str) -> list[tuple[str, float]]:
    """Return all intents, ordered by decreasing estimated model probability."""
    if not isinstance(text, str) or len(text.strip()) < 8:
        raise ValueError("Please enter at least 8 characters to classify a request.")
    if len(text) > 2_000:
        raise ValueError("Please keep the message under 2,000 characters.")
    probabilities = model.predict_proba([text])[0]
    labels = model.classes_
    order = np.argsort(probabilities)[::-1]
    return [(str(labels[i]), float(probabilities[i])) for i in order]


def top_terms(model: Pipeline, intent: str, limit: int = 8) -> list[str]:
    """Return features with the highest positive class weights."""
    tfidf = model.named_steps["tfidf"]
    classifier = model.named_steps["classifier"]
    class_index = list(classifier.classes_).index(intent)
    terms = tfidf.get_feature_names_out()
    weights = classifier.coef_[class_index]
    indices = np.argsort(weights)[-limit:][::-1]
    return [str(terms[index]) for index in indices]
