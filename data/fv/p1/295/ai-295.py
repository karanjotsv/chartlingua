import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Derive the output filename from the JSON filename
output_filename_base = json_path.stem

# Load data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for the chart
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='black', width=1)
    ),
    textinfo='percent',
    textposition='outside',
    sort=False,  # Preserve the order from the JSON file
    direction='clockwise',
    rotation=90, # Start the first slice at the 12 o'clock position
    insidetextorientation='radial'
)

# Create the figure
fig = go.Figure(data=[pie_trace])

# Combine title and subtitle
title_text = f"<b>{texts.get('title', '')}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        font=dict(size=18)
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    showlegend=True,
    legend=dict(
        x=0.85,
        y=0.7,
        traceorder='normal',
        font=dict(
            family='Arial',
            size=12
        ),
        bgcolor='rgba(255,255,255,0.5)'
    ),
    margin=dict(l=40, r=40, t=80, b=80),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Add source annotation
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.95,
        y=0.05,
        font=dict(
            family="Arial",
            size=10
        )
    )

# Write the output image
output_image_path = f"{output_filename_base}.png"
fig.write_image(output_image_path, scale=2)

print(f"Chart saved as {output_image_path}")