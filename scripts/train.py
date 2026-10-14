"""Train: python -m scripts.train --source demo|bitext"""

from __future__ import annotations

import argparse
from pathlib import Path
from urllib.request import urlretrieve

from supportiq.training import train_and_evaluate

ROOT = Path(__file__).resolve().parents[1]
BITEXT_URL = (
    "https://huggingface.co/datasets/bitext/"
    "Bitext-customer-support-llm-chatbot-training-dataset/resolve/main/"
    "Bitext_Sample_Customer_Support_Training_Dataset_27K_responses-v11.csv"
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Train SupportIQ intent classifier")
    parser.add_argument("--source", choices=["demo", "bitext"], default="demo")
    args = parser.parse_args()

    if args.source == "bitext":
        dataset = ROOT / "data" / "bitext_download.csv"
        if not dataset.exists():
            print("Downloading original Bitext dataset (~19 MB)...")
            dataset.parent.mkdir(parents=True, exist_ok=True)
            try:
                urlretrieve(BITEXT_URL, dataset)
            except Exception:
                dataset.unlink(missing_ok=True)
                raise
        source = "Bitext customer-support dataset (synthetic, CDLA-Sharing-1.0); six selected intents"
    else:
        dataset = ROOT / "data" / "demo_tickets.csv"
        source = "Original small illustrative training set, authored for SupportIQ"

    metrics = train_and_evaluate(
        path=dataset,
        artifact=ROOT / "artifacts" / "intent_classifier.joblib",
        metrics_path=ROOT / "artifacts" / "metrics.json",
        source=source,
    )
    print(f"Model trained on {metrics['rows']:,} labeled examples")
    print(f"Held-out accuracy: {metrics['accuracy']:.1%}; macro F1: {metrics['macro_f1']:.1%}")
    print("Saved model and evaluation report to artifacts/")


if __name__ == "__main__":
    main()
