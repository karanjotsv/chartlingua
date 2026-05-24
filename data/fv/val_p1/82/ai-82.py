import sys
import json
import plotly.graph_objects as go
import pathlib

# This script requires a single command-line argument: the path to the JSON data file.
if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]
filename_base = pathlib.Path(json_file_path).stem

# Read and parse the JSON data file.
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_file_path}'")
    sys.exit(1)

# Extract data, texts, and colors from the JSON object.
data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for Plotly by extracting labels and values.
labels = [item['label'] for item in data]
values = [item['value'] for item in data]

# Create the figure object.
fig = go.Figure()

# Add the pie chart trace.
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors),
    texttemplate='%{value}%',
    textfont=dict(color='white', size=14),
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise'
))

# Configure the layout of the chart.
title_text = texts['title']
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.98,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(size=24)
    ),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=0.90,
        xanchor="left",
        x=0.05
    ),
    font=dict(
        family="Arial"
    ),
    margin=dict(l=40, r=40, t=120, b=40),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Generate and save the output image file.
output_filename = f"{filename_base}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")