import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Get file path from command-line argument
json_file_path = Path(sys.argv[1])

# Read the JSON data
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data and settings from the JSON
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Prepare data for plotting
x_values = [d['year'] for d in chart_data]
y_values = [d['population'] for d in chart_data]

# Create the figure
fig = go.Figure()

# Add the primary line trace
fig.add_trace(go.Scatter(
    x=x_values,
    y=y_values,
    mode='lines+markers+text',
    line=dict(color=colors[0], width=2),
    marker=dict(
        symbol='square',
        color=colors[0],
        size=7,
        line=dict(color='#5A2A00', width=1.5)
    ),
    text=[f'{val}' for val in y_values],
    textposition='top center',
    textfont=dict(
        family="Arial",
        size=10,
        color='#333333'
    ),
    hoverinfo='skip'
))

# Build title string from JSON
title_text = texts.get('title') or ''
if texts.get('subtitle'):
    title_text += f'<br><sup>{texts["subtitle"]}</sup>'

# Build source/note string from JSON
source_text = ""
if texts.get('source'):
    source_text += f"Source: {texts['source']}"
if texts.get('note'):
    if source_text:
        source_text += "<br>"
    source_text += f"Note: {texts['note']}"

# Update layout for a professional appearance
fig.update_layout(
    font=dict(family="Arial"),
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left',
        font=dict(size=18)
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickmode='linear',
        tick0=1870,
        dtick=10,
        showgrid=True,
        gridcolor='#A9B2C3',
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 40000],
        dtick=5000,
        showgrid=True,
        gridcolor='#A9B2C3',
        zeroline=True,
        zerolinecolor='#A9B2C3',
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(t=60, b=80, l=60, r=40),
    annotations=[
        dict(
            showarrow=False,
            text=source_text,
            x=0,
            y=-0.18, # Positioned lower to avoid overlap with x-axis labels
            xref="paper",
            yref="paper",
            xanchor="left",
            yanchor="top",
            align="left"
        )
    ]
)

# Define output filename from the input JSON path
output_filename = json_file_path.stem + ".png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")