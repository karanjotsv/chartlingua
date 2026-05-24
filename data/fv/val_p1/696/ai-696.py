import sys
import json
import os
import plotly.graph_objects as go

# Check for required command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_path = sys.argv[1]

# Ensure the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Derive output filename from the JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Load data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_path}'")
    sys.exit(1)

# Extract data and settings from the loaded JSON
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Prepare data for Plotly
labels = [f"{item['category']}<br>{item['value']}%" for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the donut chart
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    hole=0.4,
    marker=dict(
        colors=colors,
        line=dict(color='#FFFFFF', width=2)
    ),
    textinfo='label',
    textposition='inside',
    insidetextfont=dict(family='Arial', size=20, color='black'),
    hoverinfo='none',
    sort=False,
    direction='clockwise'
))

# Combine title and subtitle
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Combine source and note for the annotation
source_text = texts.get('source', '')
if texts.get('note'):
    source_text += f"<br>{texts.get('note')}"

# Update layout for a clean and accurate appearance
fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(family="Arial", size=16)
    ),
    showlegend=False,
    font=dict(family="Arial", size=14, color="black"),
    margin=dict(l=40, r=40, t=100, b=80),
    paper_bgcolor='white',
    plot_bgcolor='white',
    annotations=[
        dict(
            showarrow=False,
            text=source_text,
            xref="paper",
            yref="paper",
            x=0,
            y=-0.12,
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(family="Arial", size=12)
        )
    ] if source_text else []
)

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")