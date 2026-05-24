import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

# Extract data and texts from the config
chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

# Create the figure
fig = go.Figure()

# Add bar trace from the data, preserving order
bar_data = chart_data[0]
fig.add_trace(go.Bar(
    x=bar_data['x_values'],
    y=bar_data['y_values'],
    marker_color=colors[0],
    name='' # Use empty name to prevent legend item
))

# Build combined title string
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text = f"<b>{title_text}</b><br>{texts['subtitle']}"

# Build combined source/note string for annotation
source_note_text = []
if texts.get('source'):
    source_note_text.append(texts['source'])
if texts.get('note'):
    source_note_text.append(texts['note'])
caption_text = "<br>".join(source_note_text)


# Update layout for a professional appearance
fig.update_layout(
    title={
        'text': title_text,
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis={
        'title_text': texts.get('x_axis_title'),
        'type': 'category',
        'showgrid': False,
        'linecolor': 'black',
        'ticks': 'outside'
    },
    yaxis={
        'title_text': texts.get('y_axis_title'),
        'range': [0, 6],
        'showgrid': True,
        'gridcolor': 'grey',
        'gridwidth': 1,
        'zeroline': False,
        'linecolor': 'black'
    },
    font={
        'family': "Arial",
        'size': 12
    },
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=80, b=80),
)

if caption_text:
    fig.add_annotation(
        text=caption_text,
        xref="paper", yref="paper",
        x=0, y=-0.15,  # Adjust y to be below the x-axis title
        showarrow=False,
        align="left",
        xanchor="left",
        yanchor="top"
    )

# Derive output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)