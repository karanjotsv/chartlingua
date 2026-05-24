import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read the JSON data from the file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data for the pie chart
labels = [item['label'] for item in chart_data['chart_data']]
values = [item['value'] for item in chart_data['chart_data']]
custom_labels = chart_data['texts']['data_labels']
colors = chart_data['colors']

# Create the pie chart figure
fig = go.Figure()

# Add the pie trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    text=custom_labels,
    textinfo='text',
    hoverinfo='label+percent',
    marker=dict(colors=colors),
    pull=[0, 0, 0.15],
    sort=False,  # This is crucial to preserve the original data order
    direction='clockwise'
))

# Update the layout of the figure
fig.update_layout(
    title_text=None,
    showlegend=False,
    paper_bgcolor='black',
    plot_bgcolor='black',
    font=dict(
        family="Arial",
        size=16,
        color="white"
    ),
    margin=dict(l=40, r=40, t=40, b=40)
)

# Update text font for the pie slices
fig.update_traces(
    textfont=dict(
        family="Arial",
        size=18,
        color='white'
    ),
    textposition='inside'
)

# Define the output image file name based on the JSON file name
output_filename = f"{json_file_path.stem}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")