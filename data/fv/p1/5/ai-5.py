import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read the chart data and configuration from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_path}'")
    sys.exit(1)

# Extract data, texts, and colors from the JSON structure
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Prepare data for the Plotly pie chart, preserving order
labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart figure
# Note: The original image has a 3D effect which is not a standard feature in Plotly's 'go.Pie'.
# This recreation uses a standard 2D pie chart to accurately represent the data proportions.
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#000000', width=1)),
    textinfo='value',
    textfont=dict(size=12, color='black'),
    hoverinfo='label+percent',
    sort=False,  # This is crucial to preserve the original data order
    direction='clockwise'
)])

# Combine title and subtitle using HTML for rich text formatting
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update the layout for a professional and clean appearance
fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(size=24)
    ),
    font=dict(family="Arial"),
    legend=dict(
        orientation="v",
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=0.9  # Position legend to the right of the pie chart
    ),
    margin=dict(l=40, r=300, b=80, t=100), # Adjust margins to prevent clipping
    paper_bgcolor='white',
    plot_bgcolor='white',
    showlegend=True
)

# Add source/note as an annotation if it exists
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=0,
        xanchor='left',
        yanchor='bottom',
        font=dict(size=12)
    )

# Determine the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_image_path = f"{base_filename}.png"

# Save the generated chart as a high-resolution PNG image
fig.write_image(output_image_path, scale=2)

print(f"Chart successfully generated and saved to '{output_image_path}'")