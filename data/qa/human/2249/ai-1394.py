import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Failed to decode JSON from '{json_path}'.")
    sys.exit(1)

# Extract data and texts from the JSON object
chart_data = chart_config.get('chart_data', {})
chart_texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])
categories = chart_data.get('categories', [])
series_data = chart_data.get('series', [])

# Create a new figure
fig = go.Figure()

# Add a bar trace for each data series
for i, series in enumerate(series_data):
    fig.add_trace(go.Bar(
        x=categories,
        y=series.get('values', []),
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)],
        text=series.get('values', []),
        texttemplate='%{y}%',
        textposition='outside',
        textfont=dict(family="Arial", size=12, color='black'),
        hoverinfo='none'
    ))

# Combine title and subtitle
title_text = chart_texts.get('title')
subtitle_text = chart_texts.get('subtitle')
full_title = ""
if title_text:
    full_title = f"<b>{title_text}</b>"
    if subtitle_text:
        full_title += f"<br><sub>{subtitle_text}</sub>"

# Update layout for a professional look
fig.update_layout(
    barmode='group',
    title={
        'text': full_title,
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis={
        'title_text': chart_texts.get('x_axis_title'),
        'tickfont': {'family': "Arial", 'size': 12},
        'showgrid': False,
        'showline': True,
        'linecolor': '#333333'
    },
    yaxis={
        'title_text': chart_texts.get('y_axis_title'),
        'title_font': {'family': "Arial", 'size': 14},
        'tickfont': {'family': "Arial", 'size': 12},
        'range': [0, 105],
        'ticksuffix': '%',
        'gridcolor': '#e0e0e0',
        'showline': False
    },
    legend={
        'orientation': 'h',
        'yanchor': 'bottom',
        'y': -0.3,
        'xanchor': 'center',
        'x': 0.5,
        'font': {'family': "Arial", 'size': 12}
    },
    plot_bgcolor='white',
    font_family="Arial",
    margin=dict(l=80, r=40, t=50, b=120),
    annotations=[
        dict(
            text=chart_texts.get('source', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.35,
            xanchor='right',
            yanchor='bottom',
            font=dict(family="Arial", size=12, color='#666666')
        )
    ]
)

# Set the cliponaxis to False to prevent the text labels from being clipped
for trace in fig.data:
    if isinstance(trace, go.Bar):
        trace.cliponaxis = False

# Generate the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")