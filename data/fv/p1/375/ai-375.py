import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    sys.exit(1)

json_file_path = sys.argv[1]

# Load chart configuration from the specified JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data, texts, and colors from the configuration
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Prepare data for the Plotly pie chart
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart figure
# Note: The original image has a 3D effect which is not a standard feature in
# Plotly's 2D charts. This script creates an accurate 2D data representation.
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='#FFFFFF', width=2)
    ),
    sort=False,  # Preserve the original data order
    direction='clockwise'
)])

# Configure the chart layout, fonts, and styling
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(size=20)
    ),
    font=dict(
        family="Arial",
        size=14,
        color="black"
    ),
    legend=dict(
        title_text=texts.get('legend_title'),
        orientation="v",
        yanchor="top",
        y=0.85,
        xanchor="left",
        x=1.02
    ),
    margin=dict(t=100, b=40, l=40, r=120),  # Adjust right margin for legend
    paper_bgcolor='white',
    plot_bgcolor='white',
    showlegend=True
)

# Derive the output filename from the input JSON file path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

# Save the chart as a high-resolution PNG image
fig.write_image(output_image_path, scale=2)