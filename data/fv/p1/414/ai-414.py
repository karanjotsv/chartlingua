import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- 1. Load Data from Command-Line Argument ---
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_filepath = Path(sys.argv[1])
if not json_filepath.is_file():
    print(f"Error: JSON file not found at '{json_filepath}'")
    sys.exit(1)

with open(json_filepath, 'r', encoding='utf-8') as f:
    config = json.load(f)

# --- 2. Extract Data and Texts from JSON ---
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])
insidetextfont_colors = config.get('insidetextfont_colors', ['#000000'] * len(chart_data))

labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]

# --- 3. Create the Plotly Figure ---
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='#000000', width=1)
    ),
    texttemplate='%{label}<br>%{value}%',
    textposition='auto',
    insidetextfont=dict(
        family="Arial",
        color=insidetextfont_colors
    ),
    outsidetextfont=dict(
        family="Arial",
        color="#000000"
    ),
    hole=0.0,
    sort=False,
    direction='clockwise',
    rotation=-84
))

# --- 4. Configure Layout ---
title_text = f"<b>{texts.get('title', '')}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    title_font=dict(size=24),
    font=dict(
        family="Arial",
        size=12
    ),
    showlegend=False,
    margin=dict(t=120, b=50, l=50, r=50),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# --- 5. Save the Output Image ---
output_filepath = json_filepath.with_suffix('.png')
fig.write_image(output_filepath, scale=2)

print(f"Chart successfully generated at: {output_filepath}")