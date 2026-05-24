import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data for plotting
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add traces from chart_data
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)] if colors else None,
        width=0.8 # To match bar width in the image
    ))

# Construct title and source strings safely
title_text = texts.get('title') or ''
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

source_text = texts.get('source') or ''

# Update layout
fig.update_layout(
    title={
        'text': title_text if title_text else None,
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis={
        'title_text': texts.get('x_axis_title'),
        'showgrid': False,
        'showline': True,
        'linewidth': 2,
        'linecolor': 'black',
        'mirror': True,
        'range': [-0.7, 20.5],
        'tickvals': [0, 5, 10, 15, 20],
        'zeroline': False
    },
    yaxis={
        'title_text': texts.get('y_axis_title'),
        'showgrid': False,
        'showline': True,
        'linewidth': 2,
        'linecolor': 'black',
        'mirror': True,
        'range': [0, 0.145],
        'tickvals': [0.00, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.14],
        'ticktext': ['0,00', '0,02', '0,04', '0,06', '0,08', '0,10', '0,12', '0,14'], # Manual formatting for comma decimal
        'zeroline': False
    },
    plot_bgcolor='white',
    paper_bgcolor='white',
    font={
        'family': 'Arial',
        'size': 14,
        'color': 'black'
    },
    showlegend=False,
    bargap=0.1,
    margin={'l': 60, 'r': 20, 't': 40, 'b': 40}
)

# Add source annotation if it exists
if source_text:
    fig.add_annotation(
        text=source_text,
        xref="paper", yref="paper",
        x=0, y=-0.15,
        showarrow=False,
        align="left",
        xanchor='left',
        yanchor='top'
    )

# Determine output filename from the input JSON path
output_filename_base = pathlib.Path(json_path).stem
output_image_path = f"{output_filename_base}.png"

# Save the figure as a PNG image
fig.write_image(output_image_path, scale=2)

print(f"Chart saved as {output_image_path}")