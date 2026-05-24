import sys
import json
import plotly.graph_objects as go
import os

# Ensure a command-line argument is provided
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Load data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and settings from the JSON structure
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']
x_values = chart_data['x']
series_data = chart_data['series']

# Initialize the figure
fig = go.Figure()

# Add a trace for each data series, iterating in order
for i, series in enumerate(series_data):
    fig.add_trace(go.Scatter(
        x=x_values,
        y=series['y'],
        name=series['name'],
        mode='lines',
        line=dict(color=colors[i], width=3)
    ))

# Combine title and subtitle using HTML for formatting
title_text = ""
if texts.get('title'):
    title_text += texts['title']
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Combine source and note using HTML for formatting
source_text = ""
if texts.get('source'):
    source_text += texts['source']
if texts.get('note'):
    source_text += f"<br>{texts['note']}"

# Apply layout settings to the figure
fig.update_layout(
    font=dict(family="Arial", size=12),
    title=dict(
        text=title_text if title_text else None,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickvals=x_values,
        ticktext=x_values,
        tickangle=-45,
        showgrid=False,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 1.0],
        dtick=0.1,
        tickformat='.0%',
        gridcolor='#CCCCCC',
        linecolor='black'
    ),
    legend=dict(
        title_text=texts.get('legend_title'),
        traceorder='normal',
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=1.02,
        bgcolor='rgba(0,0,0,0)'
    ),
    plot_bgcolor='white',
    margin=dict(l=60, r=120, t=60, b=80),
    annotations=[
        dict(
            text=source_text if source_text else None,
            showarrow=False,
            xref='paper', yref='paper',
            x=0, y=-0.25,
            xanchor='left', yanchor='top',
            align='left'
        )
    ]
)

# Determine the output filename from the input JSON path
base_filename, _ = os.path.splitext(os.path.basename(json_path))
output_filename = f"{base_filename}.png"


# Save the figure to a PNG file with high resolution
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")