import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- 1. Load data from JSON file ---
if len(sys.argv) < 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_filepath = Path(sys.argv[1])
with open(json_filepath, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data from the JSON object
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])
chart_type = chart_info.get('chart_type')

# --- 2. Prepare data for Plotly ---
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# --- 3. Create the chart figure ---
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    texttemplate='%{text:.2f}',
    marker_color=colors[0] if colors else None,
    cliponaxis=False # Allows text to render outside the plot area
))

# --- 4. Configure layout and styling ---

# Combine title and subtitle
title_text = texts.get('title')
if texts.get('subtitle'):
    title_text = f"<b>{title_text}</b><br><sub>{texts.get('subtitle')}</sub>"

# Combine source and note for annotation
source_text = texts.get('source', '')
if texts.get('note'):
    source_text = f"{source_text}<br>{texts.get('note')}"

fig.update_layout(
    font_family="Arial",
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickangle=-45,
        showgrid=False,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 2000],
        tickmode='linear',
        tick0=0,
        dtick=500,
        gridcolor='#e0e0e0'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=150),
    annotations=[
        dict(
            text=source_text,
            showarrow=False,
            xref="paper", yref="paper",
            x=1.0, y=-0.3, # Positioned below the plot area
            xanchor='right', yanchor='top',
            align='right',
            font=dict(size=10)
        )
    ]
)

fig.update_yaxes(
    ticks='outside',
    ticklen=5,
    linecolor='black'
)
fig.update_xaxes(
    ticks='outside',
    ticklen=5,
    linecolor='black'
)


# --- 5. Save the chart as a PNG image ---
output_filepath = json_filepath.with_suffix('.png')
fig.write_image(output_filepath, scale=2)

print(f"Chart saved to {output_filepath}")