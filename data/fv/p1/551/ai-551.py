import sys
import json
import os
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_file_path):
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read data from the specified JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for the chart
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# Prepare data for Plotly
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors),
    sort=False,  # Preserve the original order from the JSON
    direction='clockwise',
    rotation=92, # Rotate to position the small slices at the top-left
    textinfo='none',
    hoverinfo='label+percent'
)

# Create the figure
fig = go.Figure(data=[pie_trace])

# Combine title and subtitle if they exist
title_text = ""
if texts.get("title"):
    title_text += texts["title"]
if texts.get("subtitle"):
    title_text += f'<br><sub>{texts["subtitle"]}</sub>'

# Add source/note as an annotation if it exists
annotations = []
if texts.get("source"):
    annotations.append(
        go.layout.Annotation(
            text=texts["source"],
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.1,
            xanchor='left',
            yanchor='top'
        )
    )

# Update the layout of the chart
fig.update_layout(
    title_text=title_text,
    font=dict(family="Arial", size=12),
    showlegend=True,
    legend=dict(
        x=0.8,
        y=0.5,
        xanchor='left',
        yanchor='middle',
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=40, r=150, t=40, b=40),
    annotations=annotations
)

# Determine the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a PNG file and print a confirmation message
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")