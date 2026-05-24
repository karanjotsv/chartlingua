import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- 1. Load Data from Command-Line Argument ---
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <path_to_json_file>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])

if not json_file_path.is_file():
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# --- 2. Extract Data and Texts from JSON ---
chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']
categories = chart_data['categories']
series = chart_data['series']

# --- 3. Create Figure and Add Traces ---
fig = go.Figure()

for i, s in enumerate(series):
    fig.add_trace(go.Bar(
        x=categories,
        y=s['data'],
        name=s['name'],
        marker_color=colors[i],
        text=[f'{y:.1f}%' if y is not None else '' for y in s['data']],
        textposition='outside',
        textfont=dict(family="Arial", size=12, color='black'),
        cliponaxis=False
    ))

# --- 4. Configure Layout, Axes, and Annotations ---
title_text = ""
if texts.get('title'):
    title_text += texts['title']
if texts.get('subtitle'):
    title_text += f"<br><sup>{texts['subtitle']}</sup>"

fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showline=False,
        showgrid=True,
        gridcolor='#E0E0E0',
        griddash='dot',
        gridwidth=1,
        tickvals=[0, 0.025, 0.05, 0.075, 0.1, 0.125],
        ticksuffix='%',
        range=[0, 0.135],
        tickfont=dict(size=12)
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5,
        font=dict(size=12),
        traceorder='normal'
    ),
    margin=dict(l=80, r=40, b=110, t=50),
    annotations=[
        dict(
            showarrow=False,
            text=texts.get('source', ''),
            xref="paper",
            yref="paper",
            x=1.0,
            y=-0.4,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(size=10, color='#7f7f7f')
        )
    ]
)

# --- 5. Generate and Save Image ---
output_filename = json_file_path.stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")