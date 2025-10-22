# -*- coding: utf-8 -*-
# AI Power Index Dashboard 2030
# Author: NamSeok Kim (AEON Communications / MASSAMASS)

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# ───────────────────────────────────────────────
# 1️⃣ 데이터 정의
# ───────────────────────────────────────────────
layers = ["General", "Enterprise", "Command"]
df_index = pd.DataFrame({
    "Layer": layers,
    "MarketShare(%)": [35, 43, 22],
    "CAGR(%)": [25, 45, 55],
    "AvgIndustryPenetration(%)": [25, 55, 57],
})

# AI Power Index 계산 공식
df_index["PowerIndex"] = round(
    (df_index["MarketShare(%)"] * 0.4) +
    (df_index["CAGR(%)"] * 0.4) +
    (df_index["AvgIndustryPenetration(%)"] * 0.2), 1
)

# 레이더 비교용
radar_data = pd.DataFrame({
    "Metric": ["MarketShare(%)", "CAGR(%)", "Industry Penetration(%)", "PowerIndex"],
    "General": [35, 25, 25, df_index.loc[0, "PowerIndex"]],
    "Enterprise": [43, 45, 55, df_index.loc[1, "PowerIndex"]],
    "Command": [22, 55, 57, df_index.loc[2, "PowerIndex"]],
})

# ───────────────────────────────────────────────
# 2️⃣ Dash 앱 구성
# ───────────────────────────────────────────────
app = Dash(__name__)
app.title = "AI Power Index Dashboard 2030"

app.layout = html.Div(style={'backgroundColor': '#0a0d14', 'padding': '20px'}, children=[
    html.H1("2030 AI Power Index Dashboard", style={'color': 'white'}),
    html.H4("AI Strength Scoring Model — AEON Communications", style={'color': '#9ca3af'}),
    
    # 필터 UI
    html.Div([
        html.Label("Select Weighting Model:", style={'color': '#fff'}),
        dcc.RadioItems(
            id='weight-model',
            options=[
                {'label': 'Balanced (40/40/20)', 'value': 'balanced'},
                {'label': 'Growth Focused (30/50/20)', 'value': 'growth'},
                {'label': 'Market Dominance (50/30/20)', 'value': 'market'}
            ],
            value='balanced',
            inline=True,
            style={'color': 'white', 'marginTop': '10px'}
        )
    ], style={'marginBottom': '30px'}),

    # 시각화 패널
    html.Div([
        html.Div([dcc.Graph(id='bar-index')], style={'width': '49%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='radar-index')], style={'width': '49%', 'display': 'inline-block'}),
    ]),
])

# ───────────────────────────────────────────────
# 3️⃣ 콜백 로직
# ───────────────────────────────────────────────
@app.callback(
    [Output('bar-index', 'figure'),
     Output('radar-index', 'figure')],
    [Input('weight-model', 'value')]
)
def update_dashboard(weight_model):
    # 가중치 조정
    weights = {
        'balanced': (0.4, 0.4, 0.2),
        'growth': (0.3, 0.5, 0.2),
        'market': (0.5, 0.3, 0.2)
    }[weight_model]

    df = df_index.copy()
    df["PowerIndex"] = round(
        (df["MarketShare(%)"] * weights[0]) +
        (df["CAGR(%)"] * weights[1]) +
        (df["AvgIndustryPenetration(%)"] * weights[2]), 1
    )

    # 막대그래프
    fig_bar = px.bar(
        df, x="Layer", y="PowerIndex", color="Layer",
        text="PowerIndex", title=f"AI Power Index by Layer — Weight Model: {weight_model.title()}",
        template="plotly_dark"
    )
    fig_bar.update_traces(textposition="outside")

    # 레이더 차트
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
        title="AI Comparative Radar (Market vs Growth vs Penetration)",
        template="plotly_dark"
    )

    return fig_bar, fig_radar

# ───────────────────────────────────────────────
# 4️⃣ 실행
# ───────────────────────────────────────────────
if __name__ == "__main__":
    app.run_server(debug=True, port=8052)
