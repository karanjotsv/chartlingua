import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- 1. Load data from JSON file ---
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])
chart_type = chart_config.get('chart_type')

# --- 2. Create the Plotly figure ---
fig = go.Figure()

# Add data series to the chart
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)] if colors else None,
        text=series.get('y'),
        texttemplate='%{text:.2f}',
        textposition='outside',
        textfont=dict(family="Arial", size=12, color='black'),
        cliponaxis=False
    ))

# --- 3. Configure the layout ---
title_text = texts.get('title') or ''
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

annotations = []
if texts.get('note'):
    annotations.append(
        dict(
            text=texts['note'],
            showarrow=False,
            xref='paper', yref='paper',
            x=0, y=-0.15,
            xanchor='left', yanchor='top',
            font=dict(family="Arial", size=12)
        )
    )

if texts.get('source'):
    annotations.append(
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper', yref='paper',
            x=1, y=-0.15,
            xanchor='right', yanchor='top',
            font=dict(family="Arial", size=12)
        )
    )

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=True,
        zerolinecolor='#cccccc',
        zerolinewidth=1
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        gridcolor='#e0e0e0',
        zeroline=False,
        range=[0, 1800]
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    font=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    margin=dict(l=80, r=40, t=50, b=120),
    annotations=annotations
)

# --- 4. Output the image ---
output_path = Path(json_path).with_suffix('.png')
fig.write_image(str(output_path), scale=2)

print(f"Chart saved to {output_path}")