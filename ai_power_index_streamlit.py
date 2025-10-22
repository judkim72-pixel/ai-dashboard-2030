# ai_power_index_streamlit.py
# 2030 AI Power Index Dashboard + Conversational Insights
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
# 1️⃣ AI Power Index — Bar Chart
# ────────────────────────────────
df = pd.DataFrame({
    "Layer": ["General", "Enterprise", "Command"],
    "MarketShare(%)": [35, 43, 22],
    "CAGR(%)": [25, 45, 55],
    "Penetration(%)": [25, 55, 57],
})
df["PowerIndex"] = (
    df["MarketShare(%)"] * 0.4 +
    df["CAGR(%)"] * 0.4 +
    df["Penetration(%)"] * 0.2
).round(1)

fig_bar = px.bar(
    df, x="Layer", y="PowerIndex", color="Layer",
    text="PowerIndex", title="AI Power Index by Layer (2030)",
    template="plotly_dark"
)
fig_bar.update_traces(textposition="outside")
st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("""
🧩 **해석 요약**
- **General AI** → OpenAI, Google 등 ‘범용 대화형 AI’로, 지식·창작 중심 시장을 주도하지만 수익성은 한계에 도달.  
- **Enterprise AI** → Anthropic이 주도하는 기업형 AI 생태계로, **정책 일관성과 보안**을 중심으로 급성장 중.  
- **Command AI** → Palantir·LIG Nex1이 이끄는 **산업 지휘형 AI**로, 방산·에너지·인프라 영역에서 경제적 가치 급상승.  
→ **2030년 AI 시장의 무게중심은 Enterprise와 Command로 이동 중.**
""")

# ────────────────────────────────
# 2️⃣ Radar Chart — Comparative Strengths
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
    title="AI Comparative Radar (2030)"
)
st.plotly_chart(fig_radar, use_container_width=True)

st.markdown("""
📊 **해석 요약**
- Enterprise AI는 **CAGR(성장률)** 과 **시장 침투율**에서 모든 영역을 앞섬.  
- Command AI는 현재 점유율은 낮지만, **산업 의존도가 높고 성장 탄력성이 가장 큼**.  
- General AI는 여전히 대중적 영향력은 있으나 **경제적 파워는 점차 감소**.  
→ AI 시장은 “대중성 중심”에서 “산업 효율 중심”으로 전환 중.
""")

# ────────────────────────────────
# 3️⃣ Market Projection 2035 — Value Forecast
# ────────────────────────────────
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
        x=projection["Year"], y=projection[col],
        mode="lines+markers",
        name=col.replace("_", " "),
        line=dict(width=3, color=color)
    ))
fig_proj.update_layout(
    template="plotly_dark",
    title="Projected AI Economic Value Share (2025–2035)",
    xaxis_title="Year",
    yaxis_title="Market Value Index (Relative)"
)
st.plotly_chart(fig_proj, use_container_width=True)

st.markdown("""
📈 **해석 요약**
- **2031~2033년 사이 Command AI가 Enterprise AI 곡선을 교차** —  
  산업 통제 시스템(Defense, Infra, Energy) 중심의 **AI Command System 경제** 도래.  
- Enterprise AI는 조직 운영 중심으로 안정적 성장,  
  General AI는 포화 단계에 진입.  
→ **AI 경제의 가치 중심은 산업 레벨로 전이될 것.**
""")

# ────────────────────────────────
# 4️⃣ Weighted + Clustered Network Map
# ────────────────────────────────
st.markdown("---")
st.markdown("### 🕸️ Global AI Influence Network by National Cluster (2025–2035)")

company_info = {
    "OpenAI": {"country": "US", "power": 29},
    "Anthropic": {"country": "US", "power": 46},
    "Palantir": {"country": "US", "power": 42},
    "AWS": {"country": "US", "power": 38},
    "Google": {"country": "US", "power": 36},
    "Microsoft": {"country": "US", "power": 35},
    "NVIDIA": {"country": "US", "power": 33},
    "LIG Nex1": {"country": "KR", "power": 31},
    "Tencent AI": {"country": "CN", "power": 30},
    "Baidu AI": {"country": "CN", "power": 28},
    "SAP AI": {"country": "EU", "power": 27},
    "DeepMind": {"country": "EU", "power": 34},
}
edges = [
    ("OpenAI", "Microsoft", 0.9),
    ("Anthropic", "AWS", 0.85),
    ("Anthropic", "Google", 0.75),
    ("Palantir", "LIG Nex1", 0.8),
    ("OpenAI", "NVIDIA", 0.6),
    ("Google", "NVIDIA", 0.5),
    ("AWS", "Palantir", 0.7),
    ("OpenAI", "Anthropic", 0.4),
    ("Tencent AI", "Baidu AI", 0.85),
    ("SAP AI", "DeepMind", 0.6),
]
G = nx.Graph()
for n, info in company_info.items():
    G.add_node(n, country=info["country"], power=info["power"])
for u, v, w in edges:
    G.add_edge(u, v, weight=w)
pos = nx.spring_layout(G, seed=42, k=0.6)
country_colors = {"US": "#3b82f6", "KR": "#22c55e", "EU": "#facc15", "CN": "#ef4444"}

edge_x, edge_y = [], []
for u, v in G.edges():
    x0, y0 = pos[u]; x1, y1 = pos[v]
    edge_x += [x0, x1, None]; edge_y += [y0, y1, None]
node_x, node_y, node_size, node_color, node_text = [], [], [], [], []
for node, data in G.nodes(data=True):
    x, y = pos[node]
    node_x.append(x); node_y.append(y)
    node_size.append(data["power"])
    node_color.append(country_colors.get(data["country"], "#9ca3af"))
    node_text.append(f"{node}<br>Country: {data['country']}<br>Power Index: {data['power']}")
fig_net = go.Figure()
fig_net.add_trace(go.Scatter(x=edge_x, y=edge_y, mode='lines',
                             line=dict(color='gray', width=1.5), hoverinfo='none'))
fig_net.add_trace(go.Scatter(
    x=node_x, y=node_y, mode='markers+text',
    text=list(G.nodes()), textposition='top center',
    hovertext=node_text, hoverinfo='text',
    marker=dict(size=[s/1.3 for s in node_size],
                color=node_color, line=dict(width=1, color='white')),
    textfont=dict(color='white', size=12)
))
fig_net.update_layout(template="plotly_dark",
                      title="AI Influence Network by Country Cluster",
                      xaxis=dict(visible=False), yaxis=dict(visible=False))
st.plotly_chart(fig_net, use_container_width=True)

st.markdown("""
🌍 **해석 요약**
- 미국(US) 중심의 AI 생태계가 여전히 핵심이나,  
  **한국(KR)과 유럽(EU), 중국(CN)** 이 자국형 AI 모델과 산업 결합으로 **지역 블록화 추세**.  
- **LIG Nex1**은 방산 중심 Command AI 네트워크의 핵심 노드로 등장.  
- **Anthropic**은 AWS·Google과 다중 제휴, **신뢰성 기반 Enterprise Layer의 표준화**를 주도.  
→ 글로벌 AI 시장은 이제 ‘기술 경쟁’이 아닌 **‘생태계 동맹 구조’** 로 진화 중.
""")

# ────────────────────────────────
# END
# ────────────────────────────────
st.caption("© 2030 AEON Communications · AI Economic Intelligence Lab")
