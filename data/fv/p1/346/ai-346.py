import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load Data ---
# Ensure a command-line argument is provided
if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Read the JSON data file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data and text from the loaded JSON
chart_data = chart_info.get('chart_data', {})
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])
categories = chart_data.get('categories', [])
series_list = chart_data.get('series', [])

# --- 2. Create Chart ---
# Initialize the figure
fig = go.Figure()

# Add a bar trace for each series in the data
for i, series in enumerate(series_list):
    fig.add_trace(go.Bar(
        x=categories,
        y=series.get('values', []),
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)] if colors else None
    ))

# --- 3. Configure Layout ---
# Combine title and subtitle
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Combine source and note for the annotation
source_parts = []
if texts.get('source'):
    source_parts.append(f"Source: {texts.get('source')}")
if texts.get('note'):
    source_parts.append(f"Note: {texts.get('note')}")
source_text = "<br>".join(source_parts)

# Update the figure layout
fig.update_layout(
    font={
        'family': "Arial",
        'size': 12,
        'color': "black"
    },
    title={
        'text': title_text,
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis_title=texts.get('x_axis_title', ''),
    yaxis_title=texts.get('y_axis_title', ''),
    xaxis={
        'showgrid': False,
        'linecolor': 'black',
        'linewidth': 1,
        'ticks': 'outside',
        'zeroline': False
    },
    yaxis={
        'range': [0, 100],
        'tickvals': [0, 20, 40, 60, 80, 100],
        'showgrid': False,
        'linecolor': 'black',
        'linewidth': 1,
        'ticks': 'outside',
        'zeroline': False
    },
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=100, b=80),
)

# Add source/note annotation if it exists
if source_text:
    fig.add_annotation(
        text=source_text,
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.2,
        xanchor='left',
        yanchor='top',
        align='left'
    )

# --- 4. Output Image ---
# Derive the output filename from the input JSON file's base name
output_filename = json_file_path.stem + ".png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved successfully to {output_filename}")