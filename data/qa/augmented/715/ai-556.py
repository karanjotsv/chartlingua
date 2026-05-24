import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = sys.argv[1]
p = pathlib.Path(json_file_path)
output_filename = p.with_suffix('.png')

# Load data from the specified JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data from the JSON object
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Create the figure
fig = go.Figure()

# Add traces to the figure
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series.get('x_values'),
        y=series.get('y_values'),
        marker_color=colors[i % len(colors)] if colors else None,
        text=[f"{y}%" for y in series.get('y_values', [])],
        textposition='outside',
        cliponaxis=False,
        textfont=dict(
            family="Arial",
            size=14,
            color='black'
        )
    ))

# Combine title and subtitle
title_text = texts.get('title')
subtitle_text = texts.get('subtitle')
full_title = ""
if title_text:
    full_title += title_text
if subtitle_text:
    full_title += f"<br><sub>{subtitle_text}</sub>"

# Update layout
fig.update_layout(
    title_text=full_title if full_title else None,
    yaxis_title_text=texts.get('y_axis_title'),
    xaxis_title_text=texts.get('x_axis_title'),
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=40, b=100),
    xaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        range=[0, 32],
        dtick=5,
        ticksuffix='%',
        showline=False,
        gridcolor='#e0e0e0',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        tickfont=dict(size=12)
    ),
    annotations=[
        dict(
            xref='paper', yref='paper',
            x=0.99, y=-0.20,
            xanchor='right', yanchor='bottom',
            text=texts.get('source'),
            showarrow=False,
            font=dict(size=12)
        )
    ]
)

# Write the image file
fig.write_image(str(output_filename), scale=2)

print(f"Chart saved to {output_filename}")