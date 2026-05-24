import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- Argument Handling ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

output_filename = json_file_path.with_suffix('.png')

# --- Data Loading ---
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# --- Chart Creation ---
fig = go.Figure()

# --- Add Traces ---
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        mode='lines+markers',
        name=series.get('name', ''),
        line=dict(color=colors[i % len(colors)]),
        marker=dict(
            color=colors[i % len(colors)],
            symbol='diamond',
            size=6
        )
    ))

# --- Layout Configuration ---
title_text = texts.get('title')
if title_text:
    title_text = f"<b>{title_text}</b>"

x_axis_title = texts.get('x_axis_title')
if x_axis_title:
    x_axis_title = f"<b>{x_axis_title}</b>"

y_axis_title = texts.get('y_axis_title')
if y_axis_title:
    y_axis_title = f"<b>{y_axis_title}</b>"

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(size=18)
    ),
    xaxis=dict(
        title=x_axis_title,
        range=[1889, 1951],
        tickmode='linear',
        dtick=10,
        showgrid=True,
        gridcolor='#D3D3D3',
        gridwidth=1,
        showline=True,
        linewidth=1.5,
        linecolor='black'
    ),
    yaxis=dict(
        title=y_axis_title,
        range=[400, 1600],
        tickmode='linear',
        dtick=200,
        showgrid=True,
        gridcolor='#D3D3D3',
        gridwidth=1,
        showline=True,
        linewidth=1.5,
        linecolor='black'
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=100, b=80)
)


# --- Output ---
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")