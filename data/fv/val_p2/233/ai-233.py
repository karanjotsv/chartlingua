import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Ensure the JSON file exists
if not os.path.exists(json_file_path):
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read data from the specified JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for the chart
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly
labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2)),
    sort=False,
    direction='clockwise',
    rotation=122,
    textposition='outside',
    texttemplate='%{label}: %{value}%',
    hoverinfo='label+percent',
    insidetextorientation='radial'
))

# Combine title and subtitle
title_text = f"<b>{texts.get('title', '')}</b><br>{texts.get('subtitle', '')}"

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top'
    ),
    showlegend=False,
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    margin=dict(t=120, b=100, l=100, r=100),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Add source annotation
fig.add_annotation(
    text=texts.get('source', ''),
    align='left',
    showarrow=False,
    xref='paper',
    yref='paper',
    x=0,
    y=-0.1,
    xanchor='left',
    yanchor='top'
)

# Generate output filename from the input JSON filename
base_name = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_name}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")