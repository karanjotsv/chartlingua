import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# The script requires the path to the JSON file as a command-line argument.
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Derive the output filename from the input JSON filename.
output_path = json_path.with_suffix('.png')

# Load the chart configuration from the JSON file, ensuring UTF-8 encoding.
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data, texts, and colors from the loaded configuration.
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Prepare data for Plotly by extracting categories and values.
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# --- 2. Create Chart ---
# Initialize a Figure object.
fig = go.Figure()

# Add a bar trace using the data from the JSON file.
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    text=values,
    textposition='outside',
    textfont=dict(
        family="Arial",
        size=12,
        color='#A9A9A9'  # Light gray color for text above bars
    ),
    hoverinfo='none',
    cliponaxis=False # Ensures text labels are not clipped by the plot area
))

# --- 3. Configure Layout ---
# Update the layout of the figure to match the original image.
fig.update_layout(
    title=dict(
        text=texts['title'] if texts.get('title') else '',
        x=0.5,
        y=0.95,
        font=dict(family="Arial", size=20, color='black')
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickangle=-45,
        tickfont=dict(family="Arial", size=12, color='black'),
        showgrid=False,
        showline=True,
        linecolor='lightgrey',
        mirror=True  # Creates a box around the plot area
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 450],
        tickvals=[i * 50 for i in range(10)],
        tickfont=dict(family="Arial", size=12, color='dimgray'),
        showgrid=False,
        showline=True,
        linecolor='lightgrey',
        mirror=True  # Creates a box around the plot area
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial"),
    showlegend=False,
    margin=dict(l=60, r=40, t=100, b=120)  # Adjust margins for labels and title
)

# --- 4. Output Image ---
# Write the figure to a high-resolution PNG image file.
fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")