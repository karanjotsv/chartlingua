import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- Script setup and data loading ---
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# --- Extract data from JSON ---
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# --- Chart creation ---
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#000000', width=1)),
    hoverinfo='label+percent',
    textinfo='percent',
    textfont=dict(family="Arial", size=12),
    textposition='auto',
    sort=False
))

# --- Layout and styling ---
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

source_text = texts.get('source', '')

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top',
        font=dict(size=20)
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    legend=dict(
        orientation="v",
        yanchor="top",
        y=0.9,
        xanchor="left",
        x=0.85,
        bgcolor='rgba(255,255,255,0.5)'
    ),
    margin=dict(l=40, r=40, t=100, b=80),
    paper_bgcolor='white',
    plot_bgcolor='white',
    annotations=[
        dict(
            showarrow=False,
            text=source_text,
            xref="paper",
            yref="paper",
            x=0.98,
            y=-0.1,
            xanchor='right',
            yanchor='top',
            font=dict(size=10)
        )
    ]
)

# --- Output generation ---
output_filename_base = json_file_path.stem
output_png_path = f"{output_filename_base}.png"

fig.write_image(output_png_path, scale=2)

print(f"Chart saved to {output_png_path}")