import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])

# Derive the output image filename from the JSON filename
output_filename = json_file_path.with_suffix('.png')

# Read the JSON data file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data and texts from the loaded JSON
data_series = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add traces to the figure by iterating through the data series
for i, series in enumerate(data_series):
    fig.add_trace(go.Bar(
        x=series.get('values'),
        y=series.get('categories'),
        name=series.get('series_name'),
        orientation='h',
        marker=dict(
            color=colors[i % len(colors)] if colors else '#1f77b4',
            line=dict(color='black', width=1.5)
        )
    ))

# Combine title and subtitle if available
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Update layout with styling, titles, and fonts
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        font=dict(size=18)
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#FFFFFF',
        gridwidth=1,
        zeroline=False,
        range=[0, 3000],
        tickvals=[0, 500, 1000, 1500, 2000, 2500, 3000]
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#FFFFFF',
        gridwidth=1,
        zeroline=False
        # The order is determined by the data input order for categorical axes
    ),
    plot_bgcolor='#466547',
    paper_bgcolor='#466547',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    legend=dict(
        x=0.98,
        y=0.98,
        xanchor='right',
        yanchor='top',
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(0,0,0,0)'
    ),
    margin=dict(l=100, r=40, t=80, b=80),
    showlegend=True
)

# Save the figure to a PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")