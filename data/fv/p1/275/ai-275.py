import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Ensure the JSON file exists
if not os.path.exists(json_file_path):
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for the chart
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# Prepare data for Plotly
labels = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors),
    textinfo='percent',
    textposition='outside',
    hoverinfo='label+percent',
    sort=False,  # Preserve the order from the JSON file
    pull=[0.01] * len(values) # Add a tiny pull for visual separation
)

# Create the figure
fig = go.Figure(data=[pie_trace])

# Combine title and subtitle
title_text = ""
if texts.get("title"):
    title_text += f"<b>{texts['title']}</b>"
if texts.get("subtitle"):
    if title_text:
        title_text += "<br>"
    title_text += texts['subtitle']

# Update layout
fig.update_layout(
    title={
        'text': title_text,
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    font=dict(
        family="Arial",
        size=14
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.15,
        xanchor="center",
        x=0.5
    ),
    margin=dict(t=100, b=120, l=40, r=40),
    plot_bgcolor='#F0F0FF',
    paper_bgcolor='#F0F0FF',
    showlegend=True
)

fig.update_traces(
    textfont_size=14,
    insidetextorientation='radial'
)


# Determine the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")