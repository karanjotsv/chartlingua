import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts from the JSON object
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']
categories = data['categories']
series = data['series']

# Initialize the figure
fig = go.Figure()

# Add a trace for each data series
for i, s in enumerate(series):
    fig.add_trace(go.Bar(
        y=categories,
        x=s['values'],
        name=s['name'],
        orientation='h',
        marker=dict(color=colors[i]),
        text=s['values'],
        textposition='outside',
        texttemplate='%{x}',
        cliponaxis=False  # Allow text to be drawn outside the plot area
    ))

# Combine title and subtitle if they exist
title_text = ""
if texts.get("title"):
    title_text += f"<b>{texts['title']}</b>"
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Combine source and note for annotations
source_text = ""
if texts.get("source"):
    source_text += texts["source"]
if texts.get("note"):
    source_text += f"<br>{texts['note']}"

# Update layout for a clean, professional look
fig.update_layout(
    barmode='group',
    font=dict(family="Arial", size=12),
    title=dict(text=title_text, x=0.05, y=0.95),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False,
        showline=False,
        range=[0, 750]  # Set range to prevent data label clipping
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        autorange='reversed',  # Ensure categories are displayed from top to bottom
        showgrid=False,
        zeroline=False,
        showline=False
    ),
    legend=dict(
        orientation='h',
        yanchor='top',
        y=-0.15,
        xanchor='center',
        x=0.5
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=220, r=40, t=50, b=120),  # Adjust margins to fit labels and source
    annotations=[
        dict(
            showarrow=False,
            text=source_text,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.22,
            xanchor='right',
            yanchor='top',
            align='right'
        )
    ]
)

# Generate output filename from the input JSON path
base_filename = Path(json_path).stem
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")