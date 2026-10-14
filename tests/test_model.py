"""Quick checks for the saved model and dataset pipeline."""

from pathlib import Path

import pytest

from supportiq.config import INTENTS
from supportiq.model import load_model, predict, top_terms
from supportiq.training import read_examples

ROOT = Path(__file__).resolve().parents[1]


def test_data_has_all_classes() -> None:
    data = read_examples(ROOT / "data" / "demo_tickets.csv")
    assert set(data["intent"]) == set(INTENTS)
    assert data["text"].nunique() == len(data)


def test_inference_probabilities() -> None:
    model = load_model(ROOT / "artifacts" / "intent_classifier.joblib")
    results = predict(model, "My order is running late and I need to track my parcel.")
    assert results[0][0] == "track_order"
    assert len(results) == 6
    assert sum(probability for _, probability in results) == pytest.approx(1.0)


def test_refund_and_account_examples() -> None:
    model = load_model(ROOT / "artifacts" / "intent_classifier.joblib")
    assert predict(model, "I want a refund for the broken product I received")[0][0] == "get_refund"
    assert predict(model, "I forgot my password and cannot log into my account")[0][0] == "recover_password"


def test_inputs_are_validated() -> None:
    model = load_model(ROOT / "artifacts" / "intent_classifier.joblib")
    with pytest.raises(ValueError):
        predict(model, "hi")
    with pytest.raises(ValueError):
        predict(model, "x" * 2_001)


def test_explainable_terms() -> None:
    model = load_model(ROOT / "artifacts" / "intent_classifier.joblib")
    assert len(top_terms(model, "track_order", limit=6)) == 6
