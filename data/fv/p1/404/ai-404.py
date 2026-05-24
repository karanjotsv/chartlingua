import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data from the JSON structure
chart_data = chart_details.get('chart_data', [])
texts = chart_details.get('texts', {})
colors = chart_details.get('colors', [])

# Prepare data for Plotly pie chart
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    hole=0,
    marker=dict(
        colors=colors,
        line=dict(color='white', width=2)
    ),
    texttemplate='%{label}<br>%{value}%',
    textposition='inside',
    insidetextorientation='horizontal',
    textfont=dict(
        family="Arial",
        size=14,
        color="black"
    ),
    hoverinfo='label+percent',
    sort=False,  # This is crucial to preserve the original order
    direction='clockwise',
    rotation=90  # Sets the start of the first slice to the 12 o'clock position
))

# Configure the layout
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(family="Arial", size=22, color='black')
    ),
    showlegend=False,
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    margin=dict(l=40, r=40, t=100, b=40),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Add source text annotation if present
source_text = texts.get('source')
if source_text:
    fig.add_annotation(
        text=source_text,
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.1,
        xanchor='left',
        yanchor='top',
        font=dict(family="Arial", size=10, color="gray")
    )


# Generate the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")