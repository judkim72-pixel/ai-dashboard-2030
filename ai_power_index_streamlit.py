# ai_power_index_streamlit.py
# 2030 AI Power Index Dashboard (Streamlit version)
# AEON Communications / MASSAMASS

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="AI Power Index Dashboard 2030", layout="wide")

st.title("2030 AI Power Index Dashboard")
st.subheader("AEON Communications")

# ────────────────────────────────
# 데이터셋
# ────────────────────────────────
df = pd.DataFrame({
    "Layer": ["General", "Enterprise", "Command"],
    "MarketShare(%)": [35, 43, 22],
    "CAGR(%)": [25, 45, 55],
    "Penetration(%)": [25, 55, 57],
})

df["PowerIndex"] = (
    df["MarketShare(%)"] * 0.4
    + df["CAGR(%)"] * 0.4
    + df["Penetration(%)"] * 0.2
).round(1)

# ────────────────────────────────
# 1. 막대그래프
# ────────────────────────────────
fig_bar = px.bar(
    df,
    x="Layer",
    y="PowerIndex",
    color="Layer",
    text="PowerIndex",
    title="AI Power Index by Layer (2030)",
    template="plotly_dark",
)
fig_bar.update_traces(textposition="outside")
st.plotly_chart(fig_bar, use_container_width=True)

# ────────────────────────────────
# 2. 레이더차트
# ────────────────────────────────
radar_data = pd.DataFrame({
    "Metric": ["MarketShare", "CAGR", "Penetration", "PowerIndex"],
    "General": [35, 25, 25, df.iloc[0, -1]],
    "Enterprise": [43, 45, 55, df.iloc[1, -1]],
    "Command": [22, 55, 57, df.iloc[2, -1]],
})
fig = go.Figure()
for col in ["General", "Enterprise", "Command"]:
    fig.add_trace(go.Scatterpolar(
        r=radar_data[col],
        theta=radar_data["Metric"],
        fill='toself',
        name=col
    ))
fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
    template="plotly_dark",
    title="AI Comparative Radar (2030)",
)
st.plotly_chart(fig, use_container_width=True)
