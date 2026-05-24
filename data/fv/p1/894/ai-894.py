import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# The script requires a single command-line argument: the path to the JSON file.
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>", file=sys.stderr)
    sys.exit(1)

json_path = sys.argv[1]

# Derive the output filename from the JSON filename.
try:
    output_filename_base = Path(json_path).stem
    output_png_path = f"{output_filename_base}.png"
except Exception as e:
    print(f"Error handling file path: {e}", file=sys.stderr)
    sys.exit(1)

# Read and parse the JSON file.
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'", file=sys.stderr)
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'", file=sys.stderr)
    sys.exit(1)

# Extract data and texts from the JSON structure.
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

labels = [item.get('label', '') for item in chart_data]
values = [item.get('value', 0) for item in chart_data]

# Initialize the Plotly figure.
fig = go.Figure()

# Add the pie chart trace.
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2)),
    textinfo='percent',
    texttemplate='%{value}%',
    hoverinfo='label+percent',
    textfont=dict(color='#FFFFFF', size=14),
    sort=False,  # This is crucial to preserve the original data order.
    direction='counterclockwise'
))

# Configure the layout, title, font, and legend.
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center',
        y=0.95,
        yanchor='top',
        font=dict(size=20)
    ),
    font=dict(
        family="Arial"
    ),
    legend=dict(
        orientation="v",
        yanchor="top",
        y=0.8,
        xanchor="left",
        x=1.02,
        traceorder='normal'  # Ensures legend items match the data order.
    ),
    margin=dict(l=40, r=40, t=100, b=40),
    paper_bgcolor='white',
    plot_bgcolor='white',
    showlegend=True,
    autosize=False,
    width=800,
    height=550
)

# Export the figure to a PNG image file.
try:
    fig.write_image(output_png_path, scale=2)
except ValueError as e:
    # Handles cases where kaleido/orca is not installed
    print(f"Error writing image file. Make sure you have 'kaleido' installed (`pip install kaleido`): {e}", file=sys.stderr)
    sys.exit(1)

print(f"Chart saved to {output_png_path}")