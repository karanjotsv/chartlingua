import sys
import json
import plotly.graph_objects as go
import pathlib

# This script requires a single command-line argument: the path to the JSON data file.
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])
output_image_path = json_file_path.with_suffix('.png')

# Load data and settings from the specified JSON file.
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_file_path}'")
    sys.exit(1)

# Extract data for plotting
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']
legend_labels = texts['legend_labels']

# Prepare data for Plotly traces
categories = [item['category'] for item in chart_data]
num_series = len(legend_labels)

# Create a figure object
fig = go.Figure()

# Add a bar trace for each data series
for i in range(num_series):
    series_values = [item['values'][i] for item in chart_data]
    fig.add_trace(go.Bar(
        x=categories,
        y=series_values,
        name=legend_labels[i],
        marker_color=colors[i]
    ))

# Construct the full title string
title_text = texts['title']
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Construct the caption string for source and note
caption_parts = []
if texts.get('source'):
    caption_parts.append(texts['source'])
if texts.get('note'):
    caption_parts.append(texts['note'])
caption_text = "<br>".join(caption_parts)

# Update layout for a professional and accurate appearance
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
        'title_text': texts['x_axis_title'],
        'tickfont': {'size': 12},
        'showgrid': False
    },
    yaxis={
        'title_text': texts['y_axis_title'],
        'range': [0, 180],
        'tickmode': 'linear',
        'dtick': 20,
        'showgrid': True,
        'gridcolor': 'lightgray'
    },
    legend={
        'orientation': 'h',
        'yanchor': 'top',
        'y': -0.15,
        'xanchor': 'center',
        'x': 0.5
    },
    font={
        'family': 'Arial',
        'size': 12
    },
    plot_bgcolor='white',
    margin={'t': 100, 'b': 100, 'l': 80, 'r': 40},
    annotations=[
        go.layout.Annotation(
            showarrow=False,
            text=caption_text,
            x=0,
            y=-0.25,
            xref='paper',
            yref='paper',
            xanchor='left',
            yanchor='bottom',
            align='left'
        )
    ]
)

# Generate and save the image file
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")