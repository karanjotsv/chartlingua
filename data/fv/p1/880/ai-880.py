import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- 1. Load data from JSON file ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# --- 2. Extract data and texts ---
chart_data = chart_info.get('chart_data', {})
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])
categories = chart_data.get('categories', [])
series = chart_data.get('series', [])

# --- 3. Create the chart figure ---
fig = go.Figure()

# Add bar traces
for i, s in enumerate(series):
    fig.add_trace(go.Bar(
        x=categories,
        y=s.get('data', []),
        name=s.get('name', ''),
        marker_color=colors[i % len(colors)],
        text=s.get('data', []),
        textposition='outside',
        textfont=dict(family="Arial", size=16, color='black'),
        cliponaxis=False
    ))

# --- 4. Configure layout and styling ---
# Combine title and subtitle
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Combine source and note
source_text = ""
if texts.get('source'):
    source_text += f"Source: {texts.get('source')}"
if texts.get('note'):
    if source_text:
        source_text += "<br>"
    source_text += f"Note: {texts.get('note')}"

fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(size=18)
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickvals=[cat for i, cat in enumerate(categories) if i % 2 == 0],
        ticktext=[cat for i, cat in enumerate(categories) if i % 2 == 0],
        tickangle=-45,
        showgrid=False,
        showline=False,
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[40, 165],
        tickvals=[40, 60, 80, 100, 120, 140, 160],
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False,
        showline=False
    ),
    plot_bgcolor='white',
    showlegend=False,
    bargap=0.2,
    margin=dict(l=40, r=20, t=100, b=80),
    annotations=[
        dict(
            text=source_text,
            showarrow=False,
            xref='paper', yref='paper',
            x=0, y=-0.2, # Adjust y to position below x-axis
            xanchor='left', yanchor='top',
            align='left'
        )
    ] if source_text else []
)

# --- 5. Save the chart as a PNG image ---
output_path = json_path.with_suffix(".png")
fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")