# ai_power_index_streamlit.py
# 2030 AI Power Index Dashboard + Weighted & Clustered Network Map
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
# 기본 데이터
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

# ────────────────────────────────
# 1. Power Index Bar Chart
# ────────────────────────────────
fig_bar = px.bar(
    df, x="Layer", y="PowerIndex", color="Layer",
    text="PowerIndex", title="AI Power Index by Layer (2030)",
    template="plotly_dark"
)
fig_bar.update_traces(textposition="outside")
st.plotly_chart(fig_bar, use_container_width=True)

# ────────────────────────────────
# 2. Radar Chart
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

# ────────────────────────────────
# 3. Weighted & Clustered Network
# ────────────────────────────────
st.markdown("---")
st.markdown("### 🕸️ Global AI Influence Network by National Cluster (2025–2035)")

# 기업 데이터 (국가 + 파워 인덱스)
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

# 협력 관계 (weight)
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

# 네트워크 구성
G = nx.Graph()
for n, info in company_info.items():
    G.add_node(n, country=info["country"], power=info["power"])
for u, v, w in edges:
    G.add_edge(u, v, weight=w)

pos = nx.spring_layout(G, seed=42, k=0.6)

# 국가별 색상
country_colors = {
    "US": "#3b82f6",   # Blue
    "KR": "#22c55e",   # Green
    "EU": "#facc15",   # Yellow
    "CN": "#ef4444",   # Red
}

# Plotly 데이터 구성
edge_x, edge_y = [], []
for u, v in G.edges():
    x0, y0 = pos[u]
    x1, y1 = pos[v]
    edge_x += [x0, x1, None]
    edge_y += [y0, y1, None]

node_x, node_y, node_size, node_color, node_text = [], [], [], [], []
for node, data in G.nodes(data=True):
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    node_size.append(data["power"])
    node_color.append(country_colors.get(data["country"], "#9ca3af"))
    node_text.append(f"{node}<br>Country: {data['country']}<br>Power Index: {data['power']}")

# Plotly 그래프
fig_net = go.Figure()
fig_net.add_trace(go.Scatter(
    x=edge_x, y=edge_y,
    mode='lines', line=dict(color='gray', width=1.5),
    hoverinfo='none'
))
fig_net.add_trace(go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    text=list(G.nodes()),
    textposition='top center',
    hovertext=node_text,
    hoverinfo='text',
    marker=dict(
        size=[s / 1.3 for s in node_size],
        color=node_color,
        line=dict(width=1, color='white')
    ),
    textfont=dict(color='white', size=12)
))

fig_net.update_layout(
    template="plotly_dark",
    title="AI Influence Network by Country Cluster",
    xaxis=dict(visible=False),
    yaxis=dict(visible=False)
)
st.plotly_chart(fig_net, use_container_width=True)

# 범례
legend_colors = pd.DataFrame({
    "Country": ["United States (US)", "Korea (KR)", "Europe (EU)", "China (CN)"],
    "Color": ["#3b82f6", "#22c55e", "#facc15", "#ef4444"]
})
st.markdown("**국가별 클러스터 색상 안내**")
st.dataframe(legend_colors, hide_index=True)

st.markdown("""
**해석 가이드**
- 노드 크기 = 기업의 AI Power Index  
- 노드 색상 = 국가 클러스터  
- 연결선 굵기 = 협력 강도(weight)  
- 각 클러스터는 국가별 생태계 블록을 나타냄
""")

# ────────────────────────────────
# END
# ────────────────────────────────
st.caption("© 2030 AEON Communications · AI Economic Intelligence Lab")
