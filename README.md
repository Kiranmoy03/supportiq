# SupportIQ

**Customer-support intent classification, powered by real supervised machine learning.**

SupportIQ analyzes a support request, predicts one of six likely intents, and proposes a simple next action. Built as a small, explainable ML portfolio project using **Python, scikit-learn, TF-IDF, Logistic Regression, and Streamlit**.

> **Status:** Packaged trained baseline model with passing ML tests; Streamlit UI supplied for local verification. Ready to deploy from GitHub to Streamlit Community Cloud after UI verification. Not connected to a real order or support system.

## What it does

- **Classifies six intents:** order tracking, cancellation, refund request, payment problem, account access, and shipping-address updates.
- Shows the **top prediction and class scores**, with a low-confidence manual-review recommendation.
- Provides **clearly labeled, rule-based response drafts**. No generative AI service or API key is involved.
- Includes an **evaluation dashboard** with accuracy, macro-F1, per-class F1, confusion matrix, and indicative feature weights.
- Exports a result as JSON for debugging or demonstration.

## Quick start

Requires Python **3.12** (recommended).

```bash
# From the supportiq project folder
python -m venv .venv
```

Activate the environment:

- Windows PowerShell: `.venv\Scripts\Activate.ps1`
- macOS / Linux: `source .venv/bin/activate`

```bash
pip install -r requirements.txt
streamlit run app.py
```

This launches the interface at the local URL printed by Streamlit (normally `http://localhost:8501`). A tested starter model and its held-out evaluation results are already included in `artifacts/`.

## Retraining

### Option A — Original small starter dataset (offline)

```bash
python -m scripts.train --source demo
```

The packaged demo model uses **216 originally authored illustrative requests** (36 per intent). It is intended for running the UI and understanding the pipeline—not claiming robust real-world generalization.

### Option B — Public Bitext customer-support data (recommended before placement submission)

```bash
python -m scripts.train --source bitext
```

This downloads the **[Bitext customer-support dataset](https://huggingface.co/datasets/bitext/Bitext-customer-support-llm-chatbot-training-dataset)** (~19 MB) and selects six of its 27 labeled intents. The dataset has 26,872 total rows, but **SupportIQ trains only on rows belonging to those six intents**, so do not claim all 26,872 rows were used. The CSV is cached locally under `data/` and ignored by Git. Commit the newly generated `artifacts/intent_classifier.joblib` and `artifacts/metrics.json` files to publish an updated trained model.

The dataset is **hybrid-generated/synthetic**, not a sample of real production support tickets. Its license is **CDLA-Sharing-1.0**; credit belongs to Bitext Innovations. This repository does not redistribute the dataset itself. Consult [the dataset license](https://github.com/bitext/customer-support-llm-chatbot-training-dataset/blob/main/LICENSE.txt) before republishing datasets or modifications.

### Evaluation method

1. Load examples and keep the six supported intents.
2. Normalize whitespace, remove exact duplicate pairs, reject contradictory labels.
3. Split **75% training / 25% hold-out**, stratified by intent (`random_state=42`).
4. Train a TF-IDF (word unigrams + bigrams) / Logistic Regression pipeline on the training split only.
5. Evaluate the untouched hold-out split using accuracy, per-class metrics, macro-F1 and a confusion matrix.
6. **Refit a separate deployment model on all labeled examples** after evaluation.

**Packaged demo results:** 83.3% accuracy and 83.1% macro-F1 on 54 hold-out examples (out of 216). These numbers should not be presented as performance on the Bitext data. A random hold-out of a synthetic dataset can overstate performance on real customers.

## Repository structure

```text
supportiq/
├── app.py                       # Streamlit presentation layer
├── supportiq/
│   ├── config.py                # Intent labels and static response templates
│   ├── model.py                 # ML pipeline + inference and feature insights
│   └── training.py              # Dataset validation + evaluation + artifacts
├── scripts/
│   ├── train.py                 # CLI retraining: demo or Bitext
│   └── build_demo_data.py       # Reproduce the offline illustrative dataset
├── data/
│   └── demo_tickets.csv         # 216 original labeled starter requests
├── artifacts/
│   ├── intent_classifier.joblib # Trained baseline model
│   └── metrics.json             # Actual hold-out results
├── tests/
│   └── test_model.py            # Unit and inference smoke tests
├── .streamlit/config.toml       # UI theme
├── requirements.txt
└── README.md
```

## Tests

```bash
pip install -r requirements-dev.txt
python -m pytest -q
```

The project checks that all six labels are present, classifier probabilities sum to one, common requests classify as expected, validation rejects bad text, and learned features are accessible.

## Deploy to Streamlit Community Cloud

1. Create a **public GitHub repository** called `supportiq` and upload this project, including the two files in `artifacts/`.
2. Visit **[share.streamlit.io](https://share.streamlit.io)**, sign in with GitHub, and choose **Create app**.
3. Select the repository's `main` branch and set the main file path to `app.py`.
4. Use Python **3.12** if asked, and deploy. No credentials or secrets are required.

Full guide: [Streamlit Community Cloud deployment](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy).

## Limitations and safe usage

- This is a **classification demo**, not a chatbot, logistics API, payment resolver, or automatic customer-support agent.
- Scores from Logistic Regression are **uncalibrated model estimates**, not reliable promises of correctness.
- Unrelated or multi-intent messages may be misclassified; low scores trigger a manual-review suggestion, not a guaranteed out-of-distribution detector.
- The starter data is small, curated and not independently representative; more diverse data and real-world validation are necessary for production use.
- `joblib` artifacts are based on Python pickling. **Only load artifacts you produced or explicitly trust.**
- Do not paste private payment details, passwords, or other sensitive personal information into a public demo.

## Portfolio one-liner

> Built SupportIQ, a customer-support intent classifier using Python, TF-IDF, and Logistic Regression, with a Streamlit interface, model confidence scores, reproducible training and evaluation, and unit tests.

## Credits

- Demo data in this repository: original illustrative example texts authored for SupportIQ.
- Optional training dataset: [Bitext customer-support intent dataset](https://huggingface.co/datasets/bitext/Bitext-customer-support-llm-chatbot-training-dataset) (CDLA-Sharing-1.0, © Bitext Innovations).
