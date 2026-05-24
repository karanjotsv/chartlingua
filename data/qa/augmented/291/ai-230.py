import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- 1. Load Data from Command-Line Argument ---
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])

with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# --- 2. Extract Data and Texts from JSON ---
data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in data]
values = [item['value'] for item in data]

# --- 3. Create the Chart ---
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    marker_color=colors,
    hoverinfo='none',
    cliponaxis=False, # Prevent text on high bars from being clipped
    texttemplate='%{text:.1f}'
))

# --- 4. Configure Layout and Styling ---
# Build title string (handles nulls)
title_text = texts.get('title')
subtitle_text = texts.get('subtitle')
full_title = ""
if title_text:
    full_title += f"<b>{title_text}</b>"
if subtitle_text:
    full_title += f"<br><sub>{subtitle_text}</sub>"

fig.update_layout(
    title_text=full_title,
    title_x=0.5,
    font=dict(family="Arial", size=12),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 500],
        tickvals=[0, 100, 200, 300, 400, 500],
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=True,
        showline=True,
        linecolor='black',
        tickfont=dict(size=11)
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=90, r=20, t=40, b=120)
)

# Add source annotation
source_text = texts.get('source')
if source_text:
    fig.add_annotation(
        text=source_text,
        xref="paper", yref="paper",
        x=0.99, y=-0.22,
        showarrow=False,
        xanchor='right',
        yanchor='top',
        align='right',
        font=dict(size=10, color="#808080")
    )

# --- 5. Output the Chart ---
output_filename = f"{json_file_path.stem}.png"
fig.write_image(output_filename, scale=2, width=900, height=600)

print(f"Chart saved to {output_filename}")