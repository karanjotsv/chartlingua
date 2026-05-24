import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Get file paths from argument
json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

output_filename = json_path.with_suffix('.png')

# Load data from JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Create figure
fig = go.Figure()

# Add traces from JSON data
for i, series in enumerate(chart_data):
    color = colors[i % len(colors)] if colors else None
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name'),
        mode='lines',
        line=dict(color=color, width=2)
    ))

# Update layout
title_text = f"<b>{texts.get('title', '')}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='#D3D3D3',
    paper_bgcolor='white',
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        tickmode='linear',
        tick0=1900,
        dtick=10,
        range=[1899, 2009]
    ),
    yaxis=dict(
        showgrid=True,
        gridwidth=1,
        gridcolor='white',
        zeroline=False,
        range=[0, 3.5],
        tickmode='linear',
        tick0=0,
        dtick=0.5
    ),
    legend=dict(
        x=1.01,
        y=0.5,
        xanchor='left',
        yanchor='middle',
        bgcolor='rgba(255,255,255,0.8)',
        bordercolor='black',
        borderwidth=1
    ),
    margin=dict(l=80, r=120, b=80, t=80)
)

# Save the figure to a file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")