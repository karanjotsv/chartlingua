import sys
import json
import pathlib
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# Prepare data for Plotly pie chart, preserving order
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]
custom_text = [f"{item['label']} {item['value']}%" for item in chart_data]

# Create the pie chart figure
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors),
    text=custom_text,
    textinfo='text',
    textposition='outside',
    sort=False,  # This is crucial to preserve the original data order
    direction='clockwise',
    pull=[0.01] * len(values) # Slight pull for better label readability
))

# Configure the layout
title_text = texts.get("title") or ""
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

fig.update_layout(
    title_text=title_text,
    font=dict(
        family="Arial",
        size=12
    ),
    showlegend=False,
    margin=dict(l=80, r=80, t=80, b=80),  # Adjust margins to prevent label clipping
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Add source annotation if it exists
source_text = texts.get("source")
if source_text:
    fig.add_annotation(
        text=source_text,
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.99,
        y=0,
        xanchor='right',
        yanchor='bottom'
    )

# Define the output filename based on the input JSON filename
output_filename = pathlib.Path(json_path).stem + ".png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")