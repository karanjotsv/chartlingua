import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if a file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read the JSON data from the file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_file_path}")
    sys.exit(1)

# Extract data for plotting
chart_data = chart_details.get('chart_data', [])
texts = chart_details.get('texts', {})
colors = chart_details.get('colors', [])

# Create a new figure
fig = go.Figure()

# Add traces to the figure
for i, series in enumerate(chart_data):
    color = colors[i % len(colors)]
    trace_config = {
        'x': series.get('x'),
        'y': series.get('y'),
        'name': series.get('name'),
        'mode': series.get('mode', 'lines'),
    }

    if trace_config['mode'] == 'lines':
        trace_config['line'] = dict(color=color, width=1.5)
    elif trace_config['mode'] == 'markers':
        trace_config['marker'] = dict(
            color=color,
            symbol='circle-open',
            size=6,
            line=dict(width=1.5)
        )
    
    fig.add_trace(go.Scatter(**trace_config))

# Combine title and subtitle
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        range=[-0.02, 1.02],
        tickmode='linear',
        tick0=0,
        dtick=0.1,
        gridcolor='lightgray',
        griddash='dot',
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        ticks='inside'
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[-0.5, 5.1],
        tickmode='linear',
        tick0=0,
        dtick=0.5,
        gridcolor='lightgray',
        griddash='dot',
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        ticks='inside'
    ),
    font=dict(
        family="Arial"
    ),
    legend=dict(
        x=0.98,
        y=0.98,
        xanchor='right',
        yanchor='top',
        bgcolor='white',
        bordercolor='black',
        borderwidth=1
    ),
    plot_bgcolor='white',
    paper_bgcolor='rgb(240, 240, 240)',
    margin=dict(l=60, r=40, t=80, b=60)
)

# Generate the output filename from the input JSON filename
output_filename = json_file_path.with_suffix('.png')

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")