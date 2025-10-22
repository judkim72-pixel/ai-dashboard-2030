# ai_power_index_streamlit.py
# 2030 AI Power Index Dashboard + 2035 Market Projection + AI Network Map
# Author: Jud (AEON Communications)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx

# ────────────────────────────────
# PAGE SETTINGS
# ────────────────────────────────
st.set_page_config(page_title="AI Power Index Dashboard 2030", layout="wide")
st.title("2030 AI Power Index Dashboard")
st.subheader("AEON Communications")
st.markdown("##### Power of Experience Design · AI Economic Foresight")

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
# 1. BAR CHART — AI Power Index
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
# 2. RADAR CHART — Layer Comparison
# ────────────────────────────────
radar_data = pd.DataFrame({
    "Metric": ["MarketShare", "CAGR", "Penetration", "PowerIndex"],
    "General": [35, 25, 25, df.iloc[0, -1]],
    "Enterprise": [43, 45, 55, df.iloc[1, -1]],
    "Command": [22, 55, 57, df.iloc[2, -1]],
})
fig_radar = go.Figure()
for col in ["General", "Enterprise", "Command"]:
    fig_radar.add_trace(go.Scatterpolar(
        r=radar_data[col],
        theta=radar_data["Metric"],
        fill='toself',
        name=col
    ))
fig_radar.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
    template="plotly_dark",
    title="AI Comparative Radar (2030)",
)
st.plotly_chart(fig_radar, use_container_width=True)

# ────────────────────────────────
# 3. INSIGHT SUMMARY
# ────────────────────────────────
st.markdown("---")
st.markdown("### 🔍 AI Power Index Insights Summary")

col1, col2 = st.columns([0.65, 0.35])

with col1:
    st.markdown("""
    **1️⃣ 시장 패러다임 전환**
    - 범용 AI(General)는 개인·크리에이터 중심 시장을 주도하지만,  
      2030년 이후 경제적 무게중심은 **Enterprise 및 Command AI로 이동**.
    - AI는 더 이상 ‘지식의 도구’가 아니라, **조직과 산업을 운영하는 운영체계(Operating System)** 로 진화.

    **2️⃣ Anthropic과 Enterprise AI의 부상**
    - Anthropic은 ‘Constitutional AI’를 기반으로 **신뢰·안전·정책 일관성** 중심의 기업형 AI 시장에서 급부상.
    - 기업은 OpenAI 같은 범용모델보다, **도메인 맞춤형·보안 내재형 AI**를 선호.

    **3️⃣ 시장 가치 이동**
    - 범용 AI → 기업형 AI → 산업형 Command AI 순으로 **경제적 가치 흐름이 우측으로 이동**.
    - Enterprise + Command Layer가 2030년 AI 경제 가치의 약 **70% 이상 점유** 예상.
    """)

with col2:
    st.markdown("""
    **4️⃣ 주요 플레이어 포지션**
    - **OpenAI** → 인간 인터페이스 표준 (창의·언어 중심)
    - **Anthropic** → 조직 운영체계 (보안·정책 중심)
    - **Palantir / LIG Nex1** → 산업 지휘 체계 (Command System 중심)

    **5️⃣ 전략적 시사점**
    - 기업은 범용 AI 의존에서 벗어나 **Enterprise AI 내재화 전략**을 구축해야 함.
    - UX 관점에서는 ‘대화형 효율’보다 ‘조직 행동·의사결정 최적화’를 설계해야 함.
    """)

st.markdown("---")
st.markdown("""
> **결론 요약**  
> - 2030년 AI 시장의 주도권은 **Enterprise Layer**가 확보하고,  
>   이후 **Command Layer**가 산업 인프라 수준으로 확장될 가능성이 높음.  
> - **AI는 경제의 신경망이며, 인간-조직-산업이 한 체계로 융합되는 전환점**에 도달함.
""")

# ────────────────────────────────
# 4. MARKET PROJECTION 2035
# ────────────────────────────────
st.markdown("---")
st.markdown("### 📈 AI Market Projection 2035 — Value Transition Forecast")

projection = pd.DataFrame({
    "Year": [2025, 2027, 2029, 2031, 2033, 2035],
    "General_AI": [35, 30, 25, 22, 20, 18],
    "Enterprise_AI": [40, 46, 50, 52, 50, 48],
    "Command_AI": [25, 24, 25, 30, 38, 45],
})
fig_proj = go.Figure()
for col, color in zip(["General_AI", "Enterprise_AI", "Command_AI"],
                      ["#3b82f6", "#22c55e", "#facc15"]):
    fig_proj.add_trace(go.Scatter(
        x=projection["Year"],
        y=projection[col],
        mode="lines+markers",
        name=col.replace("_", " "),
        line=dict(width=3, color=color)
    ))
fig_proj.update_layout(
    template="plotly_dark",
    title="Projected AI Economic Value Share (2025–2035)",
    xaxis_title="Year",
    yaxis_title="Market Value Index (Relative)",
)
st.plotly_chart(fig_proj, use_container_width=True)

st.markdown("""
**예측 해석**
- 2031~2033년 사이, **Command AI가 Enterprise AI의 성장 곡선을 교차**.  
- 방산·에너지·인프라 영역에서 **AI Command System**이 경제적 가치를 주도하게 됨.  
- Enterprise AI는 여전히 조직 운영의 중심이지만, **산업 레벨 통제 계층**이 새 주도권을 형성.
""")

# ────────────────────────────────
# 5. AI 기업별 영향력 네트워크 맵
# ────────────────────────────────
st.markdown("---")
st.markdown("### 🕸️ Global AI Ecosystem Influence Map (2025–2035)")

# 네트워크 관계 정의
edges = [
    ("OpenAI", "Microsoft"),
    ("Anthropic", "AWS"),
    ("Anthropic", "Google"),
    ("Palantir", "LIG Nex1"),
    ("OpenAI", "NVIDIA"),
    ("Google", "DeepMind"),
    ("AWS", "Palantir"),
]
G = nx.Graph()
G.add_edges_from(edges)
pos = nx.spring_layout(G, seed=42)

# Plotly 네트워크 그래프
edge_x, edge_y = [], []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x += [x0, x1, None]
    edge_y += [y0, y1, None]

node_x, node_y = zip(*[pos[node] for node in G.nodes()])
fig_net = go.Figure()
fig_net.add_trace(go.Scatter(
    x=edge_x, y=edge_y,
    mode='lines', line=dict(color='gray', width=1),
    hoverinfo='none'
))
fig_net.add_trace(go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    text=list(G.nodes()),
    textposition='top center',
    marker=dict(size=20, color='#22c55e', line=dict(width=1, color='white')),
    textfont=dict(color='white', size=12)
))
fig_net.update_layout(
    title="AI Corporate Influence Network",
    template="plotly_dark",
    xaxis=dict(visible=False),
    yaxis=dict(visible=False),
)
st.plotly_chart(fig_net, use_container_width=True)

# ────────────────────────────────
# END
# ────────────────────────────────
st.caption("© 2030 AEON Communications · AI Economic Intelligence Lab")
