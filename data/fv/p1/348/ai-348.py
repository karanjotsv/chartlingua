import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_spec = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_file_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_file_path}' contains invalid JSON.")
    sys.exit(1)

# Extract data and settings from the JSON structure
chart_data = chart_spec['chart_data']
texts = chart_spec['texts']
colors = chart_spec['colors']

# Prepare data for Plotly
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Initialize the figure
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    sort=False,  # Preserve the original order from the JSON file
    direction='clockwise',
    textinfo='none',
    hoverinfo='label+percent'
))

# Construct the title string, combining title and subtitle if available
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Construct the source string, combining source and note if available
source_parts = []
if texts.get('source'):
    source_parts.append(texts['source'])
if texts.get('note'):
    source_parts.append(texts['note'])
source_text = "<br>".join(source_parts)

# Apply layout settings to match the original chart's appearance
fig.update_layout(
    title={
        'text': title_text,
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    font={
        'family': "Arial",
        'size': 12,
        'color': "#CCCCCC"  # Light font color for readability on a dark background
    },
    showlegend=True,
    legend={
        'yanchor': "middle",
        'y': 0.5,
        'xanchor': "left",
        'x': 1.0,
        'traceorder': 'normal'
    },
    paper_bgcolor='#000000',  # Replicate the black background
    plot_bgcolor='#000000',
    margin=dict(l=40, r=200, t=100, b=80),  # Adjust margins for legend and source text
    annotations=[
        dict(
            text=source_text,
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0,
            y=-0.1,
            xanchor='left',
            yanchor='top',
            align='left'
        )
    ] if source_text else []
)

# Determine the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved as '{output_filename}'")