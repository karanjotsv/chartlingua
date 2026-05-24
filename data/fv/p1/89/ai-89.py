import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get file path from command-line argument
json_path = Path(sys.argv[1])

# Check if the file exists
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Load data from JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for Plotly pie chart
labels = [f"{item['category']}<br>{item['percentage']}" for item in chart_data]
values = [item['value'] for item in chart_data]
text_values = [item['display_value'] if item['display_value'] is not None else '' for item in chart_data]

# Create the pie chart
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    text=text_values,
    textinfo='text',
    textposition='inside',
    insidetextfont=dict(family="Arial", size=16, color='white'),
    outsidetextfont=dict(family="Arial", size=12, color='black'),
    hoverinfo='skip',
    sort=False,
    direction='clockwise',
    rotation=100,
    pull=[0, 0, 0, 0, 0, 0] # Ensure no slices are pulled
)])

# Update layout
fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.05,
        xanchor='left'
    ),
    font=dict(family="Arial", size=14),
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(t=80, b=40, l=40, r=40)
)
# Use 'auto' text position for labels outside the pie, as Plotly handles this automatically.
# 'textposition' in the trace is set to 'inside' to control the numeric values.
# The 'labels' are automatically placed outside.
fig.update_traces(textposition='auto')


# Determine output filename and save the image
output_filename = json_path.with_suffix('.png')
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")