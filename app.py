"""Streamlit interface for the SupportIQ support ticket classifier.

Model inference and training are implemented in separate modules.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import streamlit as st

from supportiq.config import INTENTS, SAMPLES
from supportiq.model import load_model, predict, top_terms

ROOT = Path(__file__).resolve().parent
MODEL_FILE = ROOT / "artifacts" / "intent_classifier.joblib"
METRICS_FILE = ROOT / "artifacts" / "metrics.json"

st.set_page_config(
    page_title="SupportIQ | Intelligent Ticket Triage",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_resource(show_spinner="Loading the SupportIQ model…")
def get_model():
    """Load the existing, validated scikit-learn pipeline just once."""
    return load_model(MODEL_FILE)


@st.cache_data(show_spinner=False)
def get_metrics() -> dict:
    """Read evaluation results produced by the separate training script."""
    return json.loads(METRICS_FILE.read_text(encoding="utf-8"))


def select_example() -> None:
    """Update the input before the text-area widget is created on this run."""
    st.session_state["ticket_text"] = SAMPLES[st.session_state["sample_intent"]]
    st.session_state.pop("prediction", None)


def render_sidebar() -> None:
    with st.sidebar:
        st.markdown("### 🧠 SupportIQ")
        st.caption("INTELLIGENT SUPPORT TRIAGE")
        st.divider()
        st.markdown("**Explore an example**")
        st.selectbox(
            "Example category",
            options=list(SAMPLES),
            format_func=lambda key: INTENTS[key]["label"],
            key="sample_intent",
        )
        st.button(
            "Use selected example",
            on_click=select_example,
            use_container_width=True,
            key="load_sample_button",
        )
        st.divider()
        st.markdown("**Model**")
        st.caption("TF-IDF + Logistic Regression")
        st.caption("6 intents · Supervised learning")
        st.divider()
        st.caption("Demo app. Do not enter sensitive personal or payment information.")


def render_prediction(result: dict | None) -> None:
    st.subheader("Classification result")
    if result is None:
        with st.container(border=True):
            st.markdown("**Ready to analyze**")
            st.caption("Enter a support request and choose Analyze to see the predicted intent.")
        return

    label, score = result["ranked"][0]
    metadata = INTENTS[label]
    with st.container(border=True):
        st.caption("PREDICTED INTENT")
        st.subheader(f"{metadata['icon']} {metadata['label']}")
        st.metric("Model score", f"{score:.1%}")
        st.progress(score)
        st.caption("Model scores are not calibrated probabilities.")

    if score < 0.45:
        st.warning("Low-confidence classification — human review is recommended.")

    st.markdown("**Suggested next step**")
    st.write(metadata["action"])
    st.markdown("**Draft response · rule-based template**")
    st.info(metadata["template"])

    with st.expander("All predicted category scores"):
        for intent, probability in result["ranked"]:
            st.caption(f"{INTENTS[intent]['label']} — {probability:.1%}")
            st.progress(probability)

    export_data = {
        "message": result["text"],
        "predicted_intent": label,
        "model_score": round(score, 4),
        "model": "TF-IDF + Logistic Regression",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "disclaimer": "Demo only. No real customer-service action was performed.",
    }
    st.download_button(
        "Download prediction (JSON)",
        json.dumps(export_data, indent=2),
        file_name="supportiq_prediction.json",
        mime="application/json",
        use_container_width=True,
        key="prediction_download",
    )


def render_analyze(model) -> None:
    left, right = st.columns([1.1, 1], gap="large")
    with left:
        st.subheader("New support request")
        st.caption("Describe a customer's problem in your own words.")
        if "ticket_text" not in st.session_state:
            st.session_state["ticket_text"] = SAMPLES["track_order"]

        # A form avoids rerendering all of the page while the user edits text.
        with st.form("ticket_analysis", border=True):
            st.text_area(
                "Customer message",
                key="ticket_text",
                height=180,
                max_chars=2_000,
                placeholder="e.g. My parcel has not arrived yet…",
            )
            submitted = st.form_submit_button(
                "Analyze request →",
                type="primary",
                use_container_width=True,
            )
        st.caption("Messages are processed in the app and aren't stored in a database.")

        if submitted:
            try:
                st.session_state["prediction"] = {
                    "text": st.session_state["ticket_text"],
                    "ranked": predict(model, st.session_state["ticket_text"]),
                }
            except ValueError as exc:
                st.session_state.pop("prediction", None)
                st.warning(str(exc))

    with right:
        render_prediction(st.session_state.get("prediction"))


def render_insights(model, metrics: dict) -> None:
    st.subheader("Model insights")
    st.caption("Evaluation is based on a stratified, held-out 25% split.")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Accuracy", f"{metrics['accuracy']:.1%}")
    col2.metric("Macro F1", f"{metrics['macro_f1']:.1%}")
    col3.metric("Labeled examples", f"{metrics['rows']:,}")
    col4.metric("Test examples", f"{metrics['test_rows']:,}")
    st.caption(f"Dataset: {metrics['source']}. {metrics['note']}")
    st.divider()

    left, right = st.columns(2, gap="large")
    with left:
        st.markdown("#### F1 by intent")
        table = pd.DataFrame(
            [
                {
                    "Intent": INTENTS[key]["label"],
                    "F1": metrics["class_report"][key]["f1-score"],
                }
                for key in metrics["labels"]
            ]
        ).set_index("Intent")
        st.bar_chart(table, y="F1", horizontal=True)
    with right:
        st.markdown("#### What the model learned")
        intent = st.selectbox(
            "Inspect category",
            options=list(INTENTS),
            format_func=lambda key: INTENTS[key]["label"],
            key="inspect_intent",
        )
        st.write(" · ".join(f"`{word}`" for word in top_terms(model, intent, 8)))
        st.caption("Learned feature weights are not causal explanations.")

    with st.expander("Confusion matrix"):
        classes = [INTENTS[k]["label"] for k in metrics["labels"]]
        matrix = pd.DataFrame(
            metrics["confusion_matrix"], index=classes, columns=classes
        )
        st.caption("Rows show actual categories; columns show model predictions.")
        st.dataframe(matrix, use_container_width=True)


def render_about() -> None:
    st.subheader("About SupportIQ")
    st.write(
        "SupportIQ categorizes customer support messages using TF-IDF text "
        "features and a Logistic Regression classifier."
    )
    st.markdown(
        "**Workflow:** labeled examples → train/test split → TF-IDF → "
        "Logistic Regression → evaluation → prediction"
    )
    st.markdown("**Supported categories:** " + " · ".join(
        INTENTS[category]["label"] for category in INTENTS
    ))
    st.warning(
        "The dataset is small and manually authored. Results are not a real-world "
        "benchmark. Scores may be misleading on unrelated inputs. Reply drafts "
        "are predefined templates, not responses generated by an LLM."
    )
    st.caption("No payments, orders, accounts, or external APIs are accessed.")


def main() -> None:
    render_sidebar()
    try:
        model = get_model()
        metrics = get_metrics()
    except (FileNotFoundError, OSError, ValueError) as exc:
        st.error("Model or evaluation artifact could not be loaded.")
        st.code("python -m scripts.train --source demo", language="bash")
        st.caption(str(exc))
        st.stop()

    # Use native Streamlit markup for stable layout across frontend updates.
    st.caption("SUPPORT TICKET CLASSIFICATION")
    st.title("Support, :violet[decoded.]")
    st.write(
        "Classify customer support messages by intent and get a suggested next step."
    )
    st.caption("TF-IDF   ·   Logistic Regression   ·   Six support intents")
    st.divider()

    analyze, insights, about = st.tabs(
        ["Analyze", "Model insights", "About"]
    )
    with analyze:
        render_analyze(model)
    with insights:
        render_insights(model, metrics)
    with about:
        render_about()


if __name__ == "__main__":
    main()
