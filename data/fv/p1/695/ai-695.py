import sys
import json
import plotly.graph_objects as go
import os

# --- 1. Load Data from JSON ---
# The script expects the JSON file path as the sole command-line argument.
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data and texts from the loaded JSON
chart_data = chart_info.get('chart_data', {})
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])
categories = chart_data.get('categories', [])
series_list = chart_data.get('series', [])

# --- 2. Create the Plotly Figure ---
# While the original is a 3D bar chart, this format is not natively supported for
# grouped bars in Plotly and is often poor for data comparison.
# A 2D grouped bar chart is the standard, robust, and more readable representation.
fig = go.Figure()

# Add a trace for each data series, iterating in order
for i, series in enumerate(series_list):
    fig.add_trace(go.Bar(
        name=series.get('name'),
        x=categories,
        y=series.get('data'),
        marker_color=colors[i % len(colors)] if colors else None
    ))

# --- 3. Configure Layout and Styling ---
# Combine title and subtitle if both exist
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Combine source and note for an annotation
source_note_list = []
if texts.get('source'):
    source_note_list.append(texts['source'])
if texts.get('note'):
    source_note_list.append(texts['note'])
source_note_text = "<br>".join(source_note_list)

fig.update_layout(
    barmode='group',
    title={
        'text': title_text,
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis={
        'title_text': texts.get('x_axis_title'),
        'tickangle': 0
    },
    yaxis={
        'title_text': texts.get('y_axis_title'),
        'gridcolor': '#A9A9A9',
        'zerolinecolor': '#A9A9A9'
    },
    legend={
        'x': 0.99,
        'y': 0.85,
        'xanchor': 'right',
        'yanchor': 'top',
        'bgcolor': 'rgba(255, 255, 255, 0.5)',
        'bordercolor': 'rgba(0, 0, 0, 0)'
    },
    font={
        'family': "Arial",
        'size': 12
    },
    paper_bgcolor='#E0E0E0',
    plot_bgcolor='#E0E0E0',
    margin={'t': 90, 'b': 80 if source_note_text else 50, 'l': 80, 'r': 40},
    annotations=[
        dict(
            showarrow=False,
            text=source_note_text,
            xref="paper",
            yref="paper",
            x=0,
            y=-0.15 if source_note_text else -0.1,  # Adjust position based on content
            xanchor='left',
            yanchor='top',
            align='left'
        )
    ] if source_note_text else []
)

# --- 4. Save the Output Image ---
# Derive the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")