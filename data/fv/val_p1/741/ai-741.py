import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for required command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <path_to_json_file>")
    sys.exit(1)

# Read the JSON file from the provided path
json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data, texts, and colors from the JSON structure
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Prepare data for Plotly trace
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='#000000', width=1)
    ),
    textinfo='percent',
    texttemplate='%{value}%',
    textposition='outside',
    textfont=dict(family="Arial", size=14, color='black'),
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise'
)

# Initialize the figure
fig = go.Figure(data=[pie_trace])

# Combine title and subtitle
title_text = f"<b>{texts.get('title', '')}</b><br>{texts.get('subtitle', '')}"

# Update layout for accurate replication
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top',
        font=dict(family="Arial", size=18, color='black')
    ),
    legend=dict(
        orientation="v",
        yanchor="top",
        y=0.7,
        xanchor="left",
        x=0.75,
        traceorder='normal',
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='black',
        borderwidth=1,
        font=dict(family="Arial", size=12, color='black')
    ),
    font=dict(family="Arial", size=12, color='black'),
    margin=dict(t=100, b=40, l=40, r=40),
    paper_bgcolor='white',
    plot_bgcolor='white',
    width=700,
    height=500
)

# Generate and save the output image
output_path = json_path.with_suffix('.png')
fig.write_image(output_path, scale=2)

print(f"Chart successfully generated and saved to '{output_path}'")