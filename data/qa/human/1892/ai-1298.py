import sys
import json
import pathlib
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read the chart data and configuration from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_path}' is not a valid JSON file.")
    sys.exit(1)

# Initialize a Figure object
fig = go.Figure()

# Extract text and color information from the JSON data
texts = chart_data['texts']
colors = chart_data['colors']

# Iterate over each data series in the JSON and add it to the figure
for i, series in enumerate(chart_data['chart_data']):
    color = colors[i % len(colors)]
    text_labels = [f"{y}%" for y in series['y']]
    
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines+markers+text',
        name=series.get('name', ''),
        line=dict(color=color, width=3),
        marker=dict(color=color, size=8),
        text=text_labels,
        textposition=series.get('text_positions'),
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        )
    ))

# Build title string, handling null values
title_text = texts.get('title') or ''
subtitle_text = texts.get('subtitle') or ''
if subtitle_text:
    title_text = f"{title_text}<br><sup>{subtitle_text}</sup>"

# Update layout for a professional and accurate appearance
fig.update_layout(
    title_text=title_text,
    yaxis_title=texts.get('y_axis_title'),
    xaxis_title=texts.get('x_axis_title'),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=100),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False,
        range=[0.5, 1.25],
        dtick=0.1,
        ticksuffix='%'
    ),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref="paper", yref="paper",
            x=1, y=-0.2,
            xanchor='right', yanchor='bottom',
            font=dict(family="Arial", size=10, color="gray")
        )
    ]
)

# Determine the output filename from the input JSON path
base_filename = pathlib.Path(json_path).stem
output_filename = f"{base_filename}.png"

# Save the figure to a PNG file with a high resolution
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")