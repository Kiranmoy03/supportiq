"""Streamlit interface for SupportIQ's supervised NLP classifier."""

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

st.markdown(
    """
    <style>
      .block-container { padding-top: 2rem; max-width: 1180px; padding-bottom: 4rem; }
      [data-testid="stSidebar"] { background: #101827; }
      h1, h2, h3 { letter-spacing: -.035em; }
      div[data-testid="stMetric"] { background: #151E2D; border: 1px solid #273247;
        padding: 17px 18px; border-radius: 15px; }
      div[data-testid="stMetricLabel"] { color: #9DADC4; }
      .hero-eyebrow { font-size: .78rem; letter-spacing: .17em; font-weight: 750;
        color: #B79CFF; text-transform: uppercase; margin-bottom: .75rem; }
      .hero-title { font-size: clamp(2.7rem, 5vw, 4.5rem); font-weight: 790;
        line-height: 1.09; letter-spacing: -.07em; color: #F4F6FC; margin-bottom: .8rem; }
      .hero-title span { color: #BAA7FF; }
      .hero-description { font-size: 1rem; color: #A3B1C5; line-height: 1.7;
        max-width: 690px; margin-bottom: 1.4rem; }
      .pill { display: inline-block; border: 1px solid #394962; border-radius: 50px;
        padding: 5px 11px; color: #C0CBE1; font-size: .78rem; margin: 0 6px 6px 0; }
      .result-card { background: linear-gradient(120deg,#1D2340,#1A2939);
        border: 1px solid #404973; border-radius: 18px; padding: 22px 24px; margin: 8px 0 16px; }
      .result-caption { color: #A3B0CD; text-transform: uppercase; font-size: .71rem;
        letter-spacing: .12em; font-weight: 750; margin-bottom: 8px; }
      .result-title { color: #F7F8FF; font-size: 1.6rem; font-weight: 750;
        letter-spacing: -.035em; margin-bottom: 7px; }
      .muted-note { color: #9CAAC1; font-size: .81rem; line-height: 1.55; }
      .section-spacer { height: 16px; }
      .stButton>button[kind="primary"] { border-radius: 11px; font-weight: 720; }
      .stDownloadButton button { border-radius: 11px; }
      @media(max-width: 700px) { .block-container {padding-top: 1rem;} }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource(show_spinner="Loading classification model…")
def get_model():
    return load_model(MODEL_FILE)


@st.cache_data
def get_metrics():
    return json.loads(METRICS_FILE.read_text(encoding="utf-8"))


with st.sidebar:
    st.markdown("### 🧠 SupportIQ")
    st.caption("INTELLIGENT SUPPORT TRIAGE")
    st.divider()
    st.markdown("**Try an example**")
    selected = st.selectbox(
        "Example intent", options=list(SAMPLES),
        format_func=lambda key: INTENTS[key]["label"],
        label_visibility="collapsed",
    )
    if st.button("Use example", use_container_width=True):
        st.session_state["ticket_text"] = SAMPLES[selected]
    st.divider()
    st.caption("ENGINE")
    st.markdown("**TF-IDF + Logistic Regression**")
    st.caption("6 intents · Supervised machine learning")
    st.caption("Runs locally · No paid API key")
    st.divider()
    st.caption("Demo model — not connected to a live customer-support system.")

try:
    model = get_model()
    metrics = get_metrics()
except (FileNotFoundError, OSError, ValueError) as exc:
    st.error("The trained model or evaluation file is missing or unreadable.")
    st.code("python -m scripts.train --source demo", language="bash")
    st.caption(str(exc))
    st.stop()

st.markdown('<div class="hero-eyebrow">NLP · CLASSIFICATION · EXPLAINABILITY</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Support, <span>decoded.</span></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-description">Classify customer messages instantly, surface the most likely '
    'intent, and give support teams a useful first step. Built with classical machine learning—'
    'not a black-box chatbot API.</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<span class="pill">✦ Real trained model</span>'
    '<span class="pill">◈ 6 support intents</span>'
    '<span class="pill">⌁ Transparent predictions</span>',
    unsafe_allow_html=True,
)

st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)

analyze_tab, insights_tab, about_tab = st.tabs(["✦  Analyze", "▦  Model insights", "ⓘ  About"])

with analyze_tab:
    left, right = st.columns([1.12, 1], gap="large")
    with left:
        st.subheader("New support request")
        st.caption("Paste a message below to see how the classifier categorizes it.")
        if "ticket_text" not in st.session_state:
            st.session_state["ticket_text"] = SAMPLES["track_order"]
        st.text_area(
            "Customer message",
            key="ticket_text",
            height=190,
            max_chars=2_000,
            placeholder="e.g. I placed an order but entered the wrong delivery address…",
        )
        submitted = st.button("Analyze request  →", type="primary", use_container_width=True)
        st.caption("Your text is processed inside the running app. It isn't saved to a database.")

    with right:
        st.subheader("Classification result")
        if submitted:
            try:
                st.session_state["prediction"] = {
                    "text": st.session_state["ticket_text"],
                    "ranked": predict(model, st.session_state["ticket_text"]),
                }
            except ValueError as exc:
                st.warning(str(exc))
                st.session_state.pop("prediction", None)

        result = st.session_state.get("prediction")
        if result:
            label, probability = result["ranked"][0]
            info = INTENTS[label]
            st.markdown(
                '<div class="result-card">'
                '<div class="result-caption">Predicted intent</div>'
                f'<div class="result-title">{info["icon"]} {info["label"]}</div>'
                f'<div class="muted-note">Model score: {probability:.1%} · Not a calibrated guarantee</div>'
                '</div>',
                unsafe_allow_html=True,
            )
            if probability < 0.45:
                st.warning("Low-confidence prediction. A human should review this request.")
            st.markdown("**Suggested next step**")
            st.write(info["action"])
            st.markdown("**Draft reply (rule-based template)**")
            st.info(info["template"])
            with st.expander("View all prediction scores"):
                for intent, score in result["ranked"]:
                    st.caption(f"{INTENTS[intent]['label']} · {score:.1%}")
                    st.progress(score)
            report = {
                "message": result["text"],
                "predicted_intent": label,
                "model_score": round(probability, 4),
                "model": "TF-IDF + Logistic Regression",
                "created_at_utc": datetime.now(timezone.utc).isoformat(),
                "note": "Automated suggestion only; no support action was performed.",
            }
            st.download_button(
                "↓  Export prediction (JSON)",
                json.dumps(report, indent=2),
                file_name="supportiq_prediction.json",
                mime="application/json",
                use_container_width=True,
            )
        else:
            st.info("Your analysis will appear here. Choose a sample and click **Analyze request** to begin.")
            st.caption("You will see the top category, its model score, and suggested triage guidance.")

with insights_tab:
    st.subheader("Inside the model")
    st.caption("Performance is measured on a held-out split, not on training examples.")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Accuracy", f"{metrics['accuracy']:.1%}")
    m2.metric("Macro F1", f"{metrics['macro_f1']:.1%}")
    m3.metric("Labeled requests", f"{metrics['rows']:,}")
    m4.metric("Held-out requests", f"{metrics['test_rows']:,}")
    st.caption(f"Dataset: {metrics['source']}. {metrics['note']}")
    st.divider()
    c1, c2 = st.columns([1, 1], gap="large")
    with c1:
        st.markdown("#### Per-class F1")
        scores = pd.DataFrame(
            [{"Intent": INTENTS[key]["label"], "F1": metrics["class_report"][key]["f1-score"]}
             for key in metrics["labels"]]
        ).set_index("Intent")
        st.bar_chart(scores, y="F1", color="#B79CFF", horizontal=True)
    with c2:
        st.markdown("#### What the model learned")
        explain = st.selectbox(
            "Inspect an intent", list(INTENTS),
            format_func=lambda key: INTENTS[key]["label"],
        )
        st.write("Most influential TF-IDF features for this intent:")
        st.write(" · ".join(f"`{word}`" for word in top_terms(model, explain, 8)))
        st.caption("Feature weights show correlations learned during training, not a causal explanation.")
    with st.expander("Confusion matrix (held-out examples)"):
        cm = pd.DataFrame(
            metrics["confusion_matrix"],
            index=[INTENTS[k]["label"] for k in metrics["labels"]],
            columns=[INTENTS[k]["label"] for k in metrics["labels"]],
        )
        st.caption("Rows = actual class · Columns = predicted class")
        st.dataframe(cm, use_container_width=True)

with about_tab:
    st.subheader("Built to demonstrate practical ML")
    st.write(
        "SupportIQ is a portfolio project for customer-support intent classification. "
        "It trains a TF-IDF text representation and a Logistic Regression classifier, "
        "evaluates unseen examples, and serves predictions through Streamlit."
    )
    st.markdown("**Pipeline:** Labeled text → train/test split → TF-IDF → classifier → evaluation → inference")
    st.markdown("**Supported intents:**")
    st.write(" · ".join(INTENTS[k]["label"] for k in INTENTS))
    st.markdown("**Important limitations**")
    st.write(
        "The bundled starter dataset is small and manually authored; its score isn't evidence "
        "of production performance. The larger Bitext dataset can be used for retraining. "
        "Model scores are not calibrated probabilities; unrelated messages can receive incorrect labels. "
        "Suggested replies are static templates—not AI-generated responses."
    )
    st.markdown(
        "[Dataset source (Bitext)](https://huggingface.co/datasets/bitext/"
        "Bitext-customer-support-llm-chatbot-training-dataset) · "
        "[Project setup](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy)"
    )
