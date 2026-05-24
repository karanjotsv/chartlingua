import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_file_path = Path(sys.argv[1])

# Read and parse the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

# Extract data from the JSON structure
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add traces to the figure
for i, series in enumerate(chart_data):
    # Format text labels for data points
    text_labels = [f"{y:.1f}%".replace(".0%", "%") for y in series.get('y', [])]
    
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        mode='lines+markers+text',
        name=series.get('name', ''),
        line=dict(color=colors[i % len(colors)], width=2.5),
        marker=dict(color=colors[i % len(colors)], size=8),
        text=text_labels,
        textposition='top center',
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        ),
        hoverinfo='none'
    ))

# Combine title and subtitle
title_text = texts.get('title') or ''
subtitle_text = texts.get('subtitle') or ''
if subtitle_text:
    title_text = f"{title_text}<br><sup>{subtitle_text}</sup>"

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title=dict(text=title_text, x=0.05, xanchor='left'),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        type='category',
        showgrid=True,
        gridcolor='#f0f0f0',
        gridwidth=1,
        showline=False,
        zeroline=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[3, 10.5],
        tickvals=[3, 4, 5, 6, 7, 8, 9, 10],
        ticktext=[f"{v}%" for v in [3, 4, 5, 6, 7, 8, 9, 10]],
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        showline=False,
        zeroline=False,
        title_standoff=10
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=70, r=30, t=40, b=100),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper', yref='paper',
            x=0.99, y=-0.18,
            xanchor='right', yanchor='top',
            align='right',
            font=dict(size=12)
        )
    ]
)

# Define output filename from the input JSON filename
output_filename = f"{json_file_path.stem}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")