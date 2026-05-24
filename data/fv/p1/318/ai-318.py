import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# The script must be called with the path to the JSON file as an argument.
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# The path to the JSON file is taken from the first command-line argument.
json_file_path = Path(sys.argv[1])

# Verify that the provided JSON file exists.
if not json_file_path.is_file():
    print(f"Error: The file {json_file_path} was not found.")
    sys.exit(1)

# Load the chart data and configuration from the specified JSON file.
with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data, texts, and colors from the loaded configuration.
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Prepare data for the Plotly pie chart.
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Initialize a Figure object.
fig = go.Figure()

# Add the pie chart trace to the figure.
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors),
    hoverinfo='label+percent',
    textinfo='value',
    texttemplate='%{value}%',
    textposition='outside',
    sort=False,  # This is crucial to preserve the original data order.
    direction='clockwise',
    # Rotation is adjusted to align the chart with the source image.
    # The first slice (51.5%) ends at the ~9 o'clock position (180 degrees).
    # Its sweep is 51.5% of 360 = 185.4 degrees.
    # Start angle = 180 + 185.4 = 365.4, which is 5.4 degrees.
    rotation=5.4
))

# Format the title by combining the main title and subtitle.
title_text = f"<b>{texts['title']}</b><br>{texts['subtitle']}"

# Update the figure's layout.
fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2, # Position legend below the chart.
        xanchor="center",
        x=0.5
    ),
    font=dict(
        family="Arial", # Set the global font family as specified.
        size=14
    ),
    paper_bgcolor="#F2F2FF", # Set a background color similar to the source image.
    plot_bgcolor="#F2F2FF",
    margin=dict(t=100, b=120, l=40, r=40) # Adjust margins to prevent clipping.
)

# Set the font size for the percentage labels on the chart.
fig.update_traces(textfont_size=14)

# Determine the output image filename from the input JSON filename.
output_image_path = json_file_path.with_suffix('.png')

# Save the figure as a high-resolution PNG image.
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")