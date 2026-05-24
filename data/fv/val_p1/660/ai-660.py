import sys
import json
import pathlib
import plotly.graph_objects as go

# Check if the path to the JSON file is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Load the data from the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data_json = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_file_path}'")
    sys.exit(1)

# Extract data for the chart
chart_data = chart_data_json.get('chart_data', [])
texts = chart_data_json.get('texts', {})
colors = chart_data_json.get('colors', [])

# Prepare data for Plotly
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    hoverinfo='label+percent',
    textinfo='value',
    texttemplate='%{value}%',
    textposition='inside',
    textfont=dict(family="Arial", color='black', size=16),
    sort=False,  # Preserve the original order
    direction='clockwise',
    rotation=90,  # Start the first slice at the top (12 o'clock)
    domain=dict(x=[0.35, 1.0]) # Allocate space on the left for the legend
)

# Create the figure
fig = go.Figure(data=[pie_trace])

# --- Layout Configuration ---
# Build title string
title_text = ""
if texts.get("title"):
    title_text += f'<b>{texts["title"]}</b>'
if texts.get("subtitle"):
    title_text += f'<br><sub>{texts["subtitle"]}</sub>'

# Build source/note annotation string
source_text = ""
if texts.get("source"):
    source_text += f'Source: {texts["source"]}'
if texts.get("note"):
    if source_text:
        source_text += "<br>"
    source_text += f'Note: {texts["note"]}'

fig.update_layout(
    title_text=title_text if title_text else None,
    title_x=0.5,
    title_xanchor='center',
    showlegend=True,
    legend=dict(
        orientation="v",
        yanchor="top",
        y=0.9,
        xanchor="left",
        x=0.01
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=50, r=50, t=60 if title_text else 30, b=60 if source_text else 30),
    annotations=[
        dict(
            showarrow=False,
            text=source_text,
            x=0,
            y=-0.1,
            xref="paper",
            yref="paper",
            xanchor="left",
            yanchor="top",
            align="left"
        )
    ] if source_text else []
)

# --- Output ---
# Derive the output filename from the input JSON filename
output_filename = f"{json_file_path.stem}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")