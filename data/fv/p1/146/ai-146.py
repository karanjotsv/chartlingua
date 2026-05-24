import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: The file at {json_path} was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print("Error: The JSON file is not well-formed.")
    sys.exit(1)

fig = go.Figure()

data_series = chart_info.get('chart_data', [])
colors = chart_info.get('colors', [])

for i, series_data in enumerate(data_series):
    color = colors[i % len(colors)] if colors else '#1f77b4'
    fig.add_trace(go.Scatter(
        x=series_data.get('x'),
        y=series_data.get('y'),
        name=series_data.get('name', ''),
        mode=series_data.get('mode', 'lines+markers'),
        line=dict(
            color=color,
            shape=series_data.get('line_shape', 'linear')
        ),
        marker=dict(
            color=color,
            symbol=series_data.get('marker_symbol', 'circle'),
            size=8
        )
    ))

texts = chart_info.get('texts', {})
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

fig.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font=dict(
        family="Arial",
        color="white"
    ),
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center',
        font=dict(size=16)
    ),
    xaxis=dict(
        visible=False,
        showgrid=False
    ),
    yaxis=dict(
        visible=False,
        showgrid=False
    ),
    showlegend=True,
    legend=dict(
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(0,0,0,0)',
        x=0.95,
        y=0.1,
        xanchor='right',
        yanchor='bottom'
    ),
    margin=dict(t=100, b=80, l=40, r=40)
)

source_text = texts.get('source')
if source_text:
    fig.add_annotation(
        text=source_text,
        xref="paper",
        yref="paper",
        x=0.5,
        y=-0.1,
        showarrow=False,
        xanchor='center',
        yanchor='top',
        font=dict(
            size=12,
            color="#CCCCCC"
        )
    )

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)