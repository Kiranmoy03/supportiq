"""Reproducible training and honest hold-out evaluation."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split

from supportiq.config import INTENTS
from supportiq.model import build_pipeline


def read_examples(path: Path) -> pd.DataFrame:
    """Read either our starter CSV or the original Bitext CSV."""
    frame = pd.read_csv(path, dtype=str).fillna("")
    if "text" not in frame.columns and "instruction" in frame.columns:
        frame = frame.rename(columns={"instruction": "text"})
    if not {"text", "intent"}.issubset(frame.columns):
        raise ValueError("Dataset must contain text/intent or instruction/intent columns")

    frame = frame.loc[:, ["text", "intent"]].copy()
    frame["text"] = frame["text"].str.strip()
    frame["intent"] = frame["intent"].str.strip()
    frame = frame[frame["intent"].isin(INTENTS)]
    frame = frame[frame["text"].str.len().ge(8)]
    # Avoid the same sentence appearing in train and test; fail if a text has conflicting labels.
    conflicts = frame.groupby(frame["text"].str.casefold())["intent"].nunique()
    if (conflicts > 1).any():
        raise ValueError("Identical text has contradictory intent labels")
    frame["_normalized"] = frame["text"].str.casefold()
    frame = frame.drop_duplicates(subset=["_normalized"]).drop(columns=["_normalized"]).reset_index(drop=True)
    counts = frame["intent"].value_counts()
    missing = set(INTENTS) - set(counts.index)
    if missing or (counts < 5).any():
        raise ValueError(f"Need at least 5 examples per intent; missing: {sorted(missing)}")
    return frame


def train_and_evaluate(path: Path, artifact: Path, metrics_path: Path, source: str) -> dict:
    """Evaluate using a stratified split, then refit the shipping model on all examples."""
    dataset = read_examples(path)
    x_train, x_test, y_train, y_test = train_test_split(
        dataset["text"], dataset["intent"], test_size=0.25,
        stratify=dataset["intent"], random_state=42,
    )
    evaluated = build_pipeline()
    evaluated.fit(x_train, y_train)
    predictions = evaluated.predict(x_test)
    label_order = list(INTENTS)
    details = classification_report(
        y_test, predictions, labels=label_order, output_dict=True, zero_division=0
    )
    metrics = {
        "source": source,
        "note": "Single stratified random 25% hold-out on labeled examples; not a real-world benchmark.",
        "rows": int(len(dataset)),
        "train_rows": int(len(x_train)),
        "test_rows": int(len(x_test)),
        "accuracy": round(float(accuracy_score(y_test, predictions)), 4),
        "macro_f1": round(float(f1_score(y_test, predictions, average="macro")), 4),
        "class_report": details,
        "labels": label_order,
        "confusion_matrix": confusion_matrix(y_test, predictions, labels=label_order).tolist(),
    }

    deployed = build_pipeline()
    deployed.fit(dataset["text"], dataset["intent"])
    artifact.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    import joblib

    joblib.dump(deployed, artifact, compress=3)
    metrics_path.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    return metrics
